from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from transtrack.controllers.payout_controller import PayoutController
from transtrack.utils.numbers import to_float
from transtrack.views import styles
from transtrack.views.lookups import owner_options, public_id_from_label
from transtrack.views.widgets import entry_value, labeled_combo, labeled_entry, make_table


class PayoutsView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=styles.WHITE)
        self.controller = PayoutController()
        self.build()
        self.load()

    def build(self):
        form = tk.LabelFrame(
            self,
            text="Payout calculation",
            bg=styles.WHITE,
            fg=styles.TEXT,
            font=styles.FONT_HEADING,
            padx=12,
            pady=10,
            bd=1,
            relief="solid",
        )
        form.pack(fill="x", pady=(0, 16))
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)
        self.owner_id = labeled_combo(form, "Owner", 0, owner_options())
        self.period_year = labeled_entry(form, "Year", 0, value=str(datetime.now().year), column_offset=2)
        self.dividend_percent = labeled_entry(form, "Dividend %", 1, value="0")

        summary = tk.Frame(self, bg=styles.SURFACE_SOFT, padx=12, pady=10, highlightthickness=1, highlightbackground=styles.BORDER)
        summary.pack(fill="x", pady=(0, 12))
        self.summary_labels = {}
        for index, key in enumerate(
            ("period", "shares", "dividend_percent", "annual_dividend", "net_payout")
        ):
            summary.columnconfigure(index, weight=1)
            tk.Label(
                summary,
                text=key.replace("_", " ").title(),
                bg=styles.SURFACE_SOFT,
                fg=styles.MUTED,
                font=styles.FONT_SMALL,
            ).grid(row=0, column=index, sticky="w", padx=6)
            value = tk.Label(summary, text="-", bg=styles.SURFACE_SOFT, fg=styles.TEXT, font=styles.FONT_HEADING)
            value.grid(row=1, column=index, sticky="w", padx=6, pady=(2, 0))
            self.summary_labels[key] = value

        actions = tk.Frame(self, bg=styles.WHITE)
        actions.pack(fill="x", pady=(0, 8))
        tk.Button(
            actions,
            text="Preview Calculation",
            command=self.preview,
            bg=styles.SECONDARY,
            fg=styles.TEXT,
            activebackground=styles.BORDER,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        ).pack(side="left", padx=(0, 8))
        tk.Button(
            actions,
            text="Calculate & Record Payout",
            command=self.record,
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            activebackground=styles.PRIMARY_HOVER,
            activeforeground=styles.WHITE,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        ).pack(side="left")

        tk.Label(self, text="Recorded payouts", bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_HEADING).pack(
            anchor="w", pady=(4, 8)
        )
        table_frame = tk.Frame(self, bg=styles.WHITE, highlightthickness=1, highlightbackground=styles.BORDER)
        table_frame.pack(fill="both", expand=True)
        self.table = make_table(
            table_frame,
            (
                "id",
                "owner_id",
                "period",
                "shares",
                "dividend_percent",
                "annual_dividend",
                "net_payout",
                "date",
            ),
        )

    def payout_inputs(self):
        return (
            public_id_from_label(entry_value(self.owner_id)),
            entry_value(self.period_year),
            entry_value(self.dividend_percent),
        )

    def preview(self):
        try:
            data = self.controller.calculate_owner_payout(*self.payout_inputs())
            self.show_summary(data)
        except Exception as exc:
            messagebox.showerror("Payout preview failed", str(exc))

    def record(self):
        try:
            data = self.controller.calculate_owner_payout(*self.payout_inputs())
            self.controller.create(data)
            self.show_summary(data)
            self.load()
            messagebox.showinfo("Payout recorded", f"Net payout: {data['net_payout']:,.2f}")
        except Exception as exc:
            messagebox.showerror("Payout failed", str(exc))

    def show_summary(self, data):
        for key, label in self.summary_labels.items():
            value = data.get(key, "-")
            if isinstance(value, float):
                value = f"{value:,.2f}"
            label.configure(text=value)

    def load(self):
        for item in self.table.get_children():
            self.table.delete(item)
        row_index = 0
        for document in self.controller.list_all(sort=[("created_at", -1)]):
            self.table.insert(
                "",
                "end",
                values=(
                    document.get("public_id") or str(document.get("_id")),
                    document.get("owner_id", ""),
                    document.get("period", ""),
                    f"{to_float(document.get('shares')):,.2f}",
                    f"{to_float(document.get('dividend_percent')):,.2f}",
                    f"{to_float(document.get('annual_dividend')):,.2f}",
                    f"{to_float(document.get('net_payout')):,.2f}",
                    document.get("date", ""),
                ),
                tags=("even" if row_index % 2 else "odd",),
            )
            row_index += 1
