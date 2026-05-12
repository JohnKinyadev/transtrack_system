import tkinter as tk
from tkinter import ttk
from datetime import datetime

from transtrack.views import styles


def clear_frame(frame):
    for child in frame.winfo_children():
        child.destroy()


def labeled_entry(parent, label, row, value="", placeholder="", column_offset=0):
    tk.Label(parent, text=label, bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_BODY).grid(
        row=row, column=column_offset, sticky="w", padx=8, pady=6
    )
    entry = tk.Entry(parent, font=styles.FONT_BODY)
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
    return entry


def labeled_combo(parent, label, row, values, value="", column_offset=0):
    tk.Label(parent, text=label, bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_BODY).grid(
        row=row, column=column_offset, sticky="w", padx=8, pady=6
    )
    combo = ttk.Combobox(parent, values=values, state="readonly", font=styles.FONT_BODY)
    if value:
        combo.set(value)
    elif values:
        combo.current(0)
    combo.grid(row=row, column=column_offset + 1, sticky="ew", padx=8, pady=6)
    return combo


def labeled_date_entry(parent, label, row, value="", placeholder="YYYY-MM-DD", column_offset=0):
    wrapper = tk.Frame(parent, bg=styles.WHITE)
    wrapper.grid(row=row, column=column_offset + 1, sticky="ew", padx=8, pady=6)
    wrapper.columnconfigure(0, weight=1)
    tk.Label(parent, text=label, bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_BODY).grid(
        row=row, column=column_offset, sticky="w", padx=8, pady=6
    )
    entry = tk.Entry(wrapper, font=styles.FONT_BODY)
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
    tk.Button(wrapper, text="Today", command=use_today, padx=8, relief="groove").grid(row=0, column=1, padx=(8, 0))
    return entry


def make_table(parent, columns):
    table = ttk.Treeview(parent, columns=columns, show="headings", height=12)
    for column in columns:
        table.heading(column, text=column.replace("_", " ").title())
        table.column(column, width=130, anchor="w")
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return table


def format_id(document):
    return document.get("public_id") or str(document.get("_id", ""))[-6:]


def entry_value(widget):
    value = widget.get().strip()
    if getattr(widget, "placeholder", None) == value:
        return ""
    return value
