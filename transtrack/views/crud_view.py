import tkinter as tk
from tkinter import messagebox

from transtrack.views import styles
from transtrack.views.lookups import display_value, public_id_from_label
from transtrack.utils.validators import is_due_soon
from transtrack.views.widgets import entry_value, labeled_combo, labeled_date_entry, labeled_entry, make_table


class CrudView(tk.Frame):
    def __init__(self, master, controller, title, fields, columns):
        super().__init__(master, bg=styles.WHITE)
        self.controller = controller
        self.title = title
        self.fields = fields
        self.columns = columns
        self.inputs = {}
        self.build()
        self.load()

    def build(self):
        form = tk.Frame(self, bg=styles.WHITE)
        form.pack(fill="x", pady=(0, 16))
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        for index, field in enumerate(self.fields):
            row = index // 2
            column_offset = 0 if index % 2 == 0 else 2
            key = field["key"]
            if field.get("type") == "select":
                values = field["values"]() if callable(field["values"]) else field["values"]
                widget = labeled_combo(form, field["label"], row, values, column_offset=column_offset)
            elif field.get("type") == "date":
                widget = labeled_date_entry(
                    form,
                    field["label"],
                    row,
                    placeholder=field.get("placeholder", "YYYY-MM-DD"),
                    column_offset=column_offset,
                )
            else:
                widget = labeled_entry(form, field["label"], row, placeholder=field.get("placeholder", ""), column_offset=column_offset)
            self.inputs[key] = widget

        button_row = (len(self.fields) + 1) // 2
        tk.Button(
            form,
            text=f"Save {self.title}",
            command=self.save,
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        ).grid(row=button_row, column=3, sticky="e", padx=8, pady=10)

        table_frame = tk.Frame(self, bg=styles.WHITE)
        table_frame.pack(fill="both", expand=True)
        self.table = make_table(table_frame, self.columns)

    def values(self):
        data = {}
        for field in self.fields:
            key = field["key"]
            value = entry_value(self.inputs[key])
            if field.get("relation"):
                value = public_id_from_label(value)
            data[key] = value
        return data

    def save(self):
        data = self.values()
        missing = [
            field["label"]
            for field in self.fields
            if not field.get("optional") and data.get(field["key"], "") == ""
        ]
        if missing:
            messagebox.showwarning("Missing information", "Please fill in all fields.")
            return
        try:
            self.controller.create(data)
            self.clear()
            self.load()
            messagebox.showinfo("Saved", f"{self.title} saved successfully.")
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc))

    def clear(self):
        for key, widget in self.inputs.items():
            if hasattr(widget, "delete"):
                widget.delete(0, tk.END)
            field = next((item for item in self.fields if item["key"] == key), {})
            if getattr(widget, "placeholder", None):
                widget.insert(0, widget.placeholder)
                widget.configure(fg=styles.MUTED)
            elif field.get("type") == "select" and widget["values"]:
                widget.current(0)

    def load(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for document in self.controller.list_all(sort=[("created_at", -1)]):
            values = []
            for column in self.columns:
                if column == "id":
                    values.append(document.get("public_id") or str(document.get("_id"))[-6:])
                else:
                    values.append(display_value(column, document.get(column, "")))
            self.table.insert("", "end", values=values)
            for field, label in getattr(self.controller, "future_date_fields", {}).items():
                value = document.get(field)
                if value and is_due_soon(value):
                    warning = ["" for _column in self.columns]
                    if len(warning) > 1:
                        warning[1] = f"{label} for {document.get('public_id')} is almost due"
                    self.table.insert("", "end", values=warning)
