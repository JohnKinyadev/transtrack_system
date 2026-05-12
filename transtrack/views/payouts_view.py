import tkinter as tk
from tkinter import messagebox

from transtrack.controllers.payout_controller import PayoutController
from transtrack.views import styles
from transtrack.views.lookups import driver_options, owner_options, public_id_from_label
from transtrack.views.widgets import entry_value, labeled_combo, labeled_entry, make_table


class PayoutsView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=styles.WHITE)
        self.controller = PayoutController()
        self.build()
        self.load()

    def build(self):
        form = tk.Frame(self, bg=styles.WHITE)
        form.pack(fill="x", pady=(0, 16))
        form.columnconfigure(1, weight=1)
        self.owner_id = labeled_combo(form, "Owner", 0, owner_options())
        self.driver_id = labeled_combo(form, "Driver", 1, driver_options())
        self.period = labeled_entry(form, "Period", 2, placeholder="YYYY-MM")
        self.interest_percent = labeled_entry(form, "Interest Percent", 3, placeholder="0")
        tk.Button(
            form,
            text="Calculate & Record Payout",
            command=self.record,
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        ).grid(row=4, column=1, sticky="e", padx=8, pady=10)

        table_frame = tk.Frame(self, bg=styles.WHITE)
        table_frame.pack(fill="both", expand=True)
        self.table = make_table(
            table_frame,
            (
                "id",
                "owner_id",
                "driver_id",
                "period",
                "gross_earnings",
                "interest_percent",
                "interest_amount",
                "total_deductions",
                "net_payout",
                "date",
            ),
        )

    def record(self):
        try:
            self.controller.record_payout(
                public_id_from_label(entry_value(self.owner_id)),
                entry_value(self.period),
                public_id_from_label(entry_value(self.driver_id)),
                entry_value(self.interest_percent),
            )
            self.load()
            messagebox.showinfo("Payout recorded", "Owner payout has been calculated and recorded.")
        except Exception as exc:
            messagebox.showerror("Payout failed", str(exc))

    def load(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for document in self.controller.list_all(sort=[("created_at", -1)]):
            self.table.insert(
                "",
                "end",
                values=(
                    document.get("public_id") or str(document.get("_id"))[-6:],
                    document.get("owner_id", ""),
                    document.get("driver_id", ""),
                    document.get("period", ""),
                    document.get("gross_earnings", 0),
                    document.get("interest_percent", 0),
                    document.get("interest_amount", 0),
                    document.get("total_deductions", 0),
                    document.get("net_payout", 0),
                    document.get("date", ""),
                ),
            )
