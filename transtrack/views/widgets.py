import tkinter as tk
from tkinter import ttk
from datetime import datetime

from transtrack.views import styles

_TABLE_STYLE_READY = False

COLUMN_LABELS = {
    "id": "Record ID",
    "full_name": "Full Name",
    "username": "Username",
    "role": "Role",
    "linked_id": "Linked Record",
    "status": "Status",
    "plate": "Plate No.",
    "make": "Make",
    "model": "Model",
    "owner_id": "Owner",
    "vehicle_id": "Vehicle",
    "driver_id": "Driver",
    "driver_contact": "Driver Contact",
    "driver_license": "Driver License",
    "conductor_id": "Conductor",
    "conductor_contact": "Conductor Contact",
    "stage_manager_id": "Stage Manager",
    "route_id": "Route",
    "trip_id": "Trip",
    "trips_today": "Trips Today",
    "assigned_vehicle": "Assigned Vehicle",
    "license_no": "License No.",
    "contact": "Contact",
    "email": "Email",
    "national_id": "National ID",
    "shares": "Shares",
    "origin": "Origin",
    "destination": "Destination",
    "expected_revenue": "Expected Revenue",
    "amount": "Amount",
    "amount_collected": "Collected",
    "gross_earnings": "Gross Earnings",
    "interest_percent": "Interest %",
    "interest_amount": "Interest Amount",
    "dividend_percent": "Dividend %",
    "annual_dividend": "Annual Dividend",
    "vehicle_expenses": "Vehicle Expenses",
    "owner_deductions": "Owner Deductions",
    "total_deductions": "Total Deductions",
    "net_payout": "Net Payout",
    "period": "Period",
    "period_start": "Start Date",
    "period_end": "End Date",
    "period_days": "Days",
    "date": "Date",
    "type": "Type",
    "logged_by": "Logged By",
}

COLUMN_WIDTHS = {
    "id": 130,
    "full_name": 180,
    "username": 150,
    "role": 160,
    "status": 120,
    "plate": 110,
    "make": 120,
    "model": 120,
    "owner_id": 180,
    "vehicle_id": 160,
    "driver_id": 170,
    "driver_contact": 140,
    "driver_license": 140,
    "conductor_id": 170,
    "conductor_contact": 140,
    "stage_manager_id": 180,
    "route_id": 170,
    "trip_id": 170,
    "trips_today": 115,
    "assigned_vehicle": 180,
    "license_no": 140,
    "contact": 140,
    "email": 210,
    "origin": 150,
    "destination": 150,
    "expected_revenue": 150,
    "amount": 120,
    "amount_collected": 130,
    "gross_earnings": 145,
    "interest_percent": 115,
    "interest_amount": 145,
    "dividend_percent": 130,
    "annual_dividend": 150,
    "vehicle_expenses": 145,
    "owner_deductions": 150,
    "total_deductions": 150,
    "net_payout": 135,
    "period": 205,
    "period_start": 120,
    "period_end": 120,
    "period_days": 95,
    "date": 115,
}

NUMERIC_COLUMNS = {
    "amount",
    "amount_collected",
    "expected_revenue",
    "shares",
    "gross_earnings",
    "interest_percent",
    "interest_amount",
    "dividend_percent",
    "annual_dividend",
    "vehicle_expenses",
    "owner_deductions",
    "total_deductions",
    "net_payout",
    "period_days",
    "trips_today",
}


def clear_frame(frame):
    for child in frame.winfo_children():
        child.destroy()


def column_title(column):
    return COLUMN_LABELS.get(column, column.replace("_", " ").title())


def configure_ttk_styles():
    global _TABLE_STYLE_READY
    if _TABLE_STYLE_READY:
        return

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TransTrack.Treeview",
        background=styles.WHITE,
        foreground=styles.TEXT,
        fieldbackground=styles.WHITE,
        rowheight=34,
        borderwidth=0,
        font=styles.FONT_BODY,
    )
    style.configure(
        "TransTrack.Treeview.Heading",
        background=styles.SIDEBAR,
        foreground=styles.WHITE,
        relief="flat",
        borderwidth=1,
        font=("Segoe UI", 10, "bold"),
        padding=(8, 8),
    )
    style.map(
        "TransTrack.Treeview",
        background=[("selected", styles.ROW_SELECTED)],
        foreground=[("selected", styles.TEXT)],
    )
    style.map(
        "TransTrack.Treeview.Heading",
        background=[("active", styles.SIDEBAR_HOVER)],
    )
    style.configure("TransTrack.Vertical.TScrollbar", gripcount=0, width=13)
    style.configure("TransTrack.TCombobox", padding=5, arrowsize=14)
    _TABLE_STYLE_READY = True


def labeled_entry(parent, label, row, value="", placeholder="", column_offset=0):
    label_widget = tk.Label(parent, text=label, bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_BODY)
    label_widget.grid(
        row=row, column=column_offset, sticky="w", padx=8, pady=6
    )
    entry = tk.Entry(
        parent,
        font=styles.FONT_BODY,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=styles.BORDER,
        highlightcolor=styles.PRIMARY,
    )
    if value:
        entry.insert(0, value)
    elif placeholder:
        entry.insert(0, placeholder)
        entry.configure(fg=styles.MUTED)

        def focus_in(_event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(fg=styles.TEXT)

        def focus_out(_event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(fg=styles.MUTED)

        entry.bind("<FocusIn>", focus_in)
        entry.bind("<FocusOut>", focus_out)
        entry.placeholder = placeholder
    entry.grid(row=row, column=column_offset + 1, sticky="ew", padx=8, pady=6)
    entry.label_widget = label_widget
    entry.grid_widget = entry
    return entry


def labeled_combo(parent, label, row, values, value="", column_offset=0):
    configure_ttk_styles()
    label_widget = tk.Label(parent, text=label, bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_BODY)
    label_widget.grid(
        row=row, column=column_offset, sticky="w", padx=8, pady=6
    )
    combo = ttk.Combobox(parent, values=values, state="readonly", font=styles.FONT_BODY, style="TransTrack.TCombobox")
    if value:
        combo.set(value)
    elif values:
        combo.current(0)
    combo.grid(row=row, column=column_offset + 1, sticky="ew", padx=8, pady=6)
    combo.label_widget = label_widget
    combo.grid_widget = combo
    return combo


def labeled_date_entry(parent, label, row, value="", placeholder="YYYY-MM-DD", column_offset=0):
    wrapper = tk.Frame(parent, bg=styles.WHITE)
    wrapper.grid(row=row, column=column_offset + 1, sticky="ew", padx=8, pady=6)
    wrapper.columnconfigure(0, weight=1)
    label_widget = tk.Label(parent, text=label, bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_BODY)
    label_widget.grid(
        row=row, column=column_offset, sticky="w", padx=8, pady=6
    )
    entry = tk.Entry(
        wrapper,
        font=styles.FONT_BODY,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=styles.BORDER,
        highlightcolor=styles.PRIMARY,
    )
    entry.grid(row=0, column=0, sticky="ew")
    if value:
        entry.insert(0, value)
    else:
        entry.insert(0, placeholder)
        entry.configure(fg=styles.MUTED)

    def focus_in(_event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(fg=styles.TEXT)

    def focus_out(_event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(fg=styles.MUTED)

    def use_today():
        entry.configure(fg=styles.TEXT)
        entry.delete(0, tk.END)
        entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    entry.bind("<FocusIn>", focus_in)
    entry.bind("<FocusOut>", focus_out)
    entry.placeholder = placeholder
    entry.label_widget = label_widget
    entry.grid_widget = wrapper
    tk.Button(
        wrapper,
        text="Today",
        command=use_today,
        padx=10,
        relief="flat",
        bg=styles.SECONDARY,
        fg=styles.TEXT,
        cursor="hand2",
    ).grid(row=0, column=1, padx=(8, 0))
    return entry


def make_table(parent, columns):
    configure_ttk_styles()
    parent.configure(bg=styles.WHITE)
    parent.columnconfigure(0, weight=1)
    parent.rowconfigure(0, weight=1)

    table = ttk.Treeview(parent, columns=columns, show="headings", height=13, style="TransTrack.Treeview")
    for column in columns:
        table.heading(column, text=column_title(column), anchor="w")
        anchor = "e" if column in NUMERIC_COLUMNS else "w"
        width = COLUMN_WIDTHS.get(column, 135)
        table.column(column, width=width, minwidth=90, anchor=anchor, stretch=True)

    y_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=table.yview, style="TransTrack.Vertical.TScrollbar")
    x_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=table.xview)
    table.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    table.tag_configure("odd", background=styles.WHITE)
    table.tag_configure("even", background=styles.ROW_ALT)
    table.tag_configure("warning", background=styles.WARNING_BG, foreground=styles.WARNING_FG)
    table.grid(row=0, column=0, sticky="nsew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    x_scrollbar.grid(row=1, column=0, sticky="ew")

    def scroll_with_wheel(event):
        table.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    table.bind("<MouseWheel>", scroll_with_wheel)
    table.bind("<Button-4>", lambda _event: table.yview_scroll(-1, "units"))
    table.bind("<Button-5>", lambda _event: table.yview_scroll(1, "units"))
    return table


def metric_card(parent, label, value, bg=None, fg=None):
    bg = bg or styles.SUCCESS_BG
    fg = fg or styles.TEXT
    card = tk.Frame(parent, bg=bg, padx=18, pady=14, highlightthickness=1, highlightbackground=styles.BORDER)
    tk.Label(card, text=label, bg=bg, fg=styles.MUTED, font=styles.FONT_SMALL).pack(anchor="w")
    tk.Label(card, text=str(value), bg=bg, fg=fg, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(4, 0))
    return card


def format_id(document):
    return document.get("public_id") or str(document.get("_id", ""))[-6:]


def entry_value(widget):
    value = widget.get().strip()
    if getattr(widget, "placeholder", None) == value:
        return ""
    return value
