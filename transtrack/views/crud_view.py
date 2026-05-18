import tkinter as tk
from tkinter import messagebox

from transtrack.db.connection import get_db
from transtrack.views import styles
from transtrack.views.lookups import display_value, label_for, public_id_from_label, relation_collection
from transtrack.utils.relations import document_query, reference_values
from transtrack.utils.validators import is_due_soon
from transtrack.views.widgets import entry_value, labeled_combo, labeled_date_entry, labeled_entry, make_table


class CrudView(tk.Frame):
    def __init__(self, master, controller, title, fields, columns, detail_columns=None, autofill_rules=None):
        super().__init__(master, bg=styles.WHITE)
        self.controller = controller
        self.title = title
        self.fields = fields
        self.columns = columns
        self.detail_columns = detail_columns or columns
        self.autofill_rules = autofill_rules or []
        self.inputs = {}
        self.editing_id = None
        self.build()
        self.load()

    def build(self):
        form = tk.LabelFrame(
            self,
            text=f"{self.title} information",
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

        for index, field in enumerate(self.fields):
            row = index // 2
            column_offset = 0 if index % 2 == 0 else 2
            key = field["key"]
            if field.get("type") == "select":
                values = field["values"]() if callable(field["values"]) else field["values"]
                widget = labeled_combo(form, field["label"], row, values, value=field.get("value", ""), column_offset=column_offset)
                if field.get("relation"):
                    widget.configure(state="normal")
            elif field.get("type") == "date":
                widget = labeled_date_entry(
                    form,
                    field["label"],
                    row,
                    value=field.get("value", ""),
                    placeholder=field.get("placeholder", "YYYY-MM-DD"),
                    column_offset=column_offset,
                )
            else:
                widget = labeled_entry(
                    form,
                    field["label"],
                    row,
                    value=field.get("value", ""),
                    placeholder=field.get("placeholder", ""),
                    column_offset=column_offset,
                )
            if field.get("readonly"):
                widget.configure(state="readonly")
            self.inputs[key] = widget

        self.bind_autofill()

        button_row = (len(self.fields) + 1) // 2
        self.save_button = tk.Button(
            form,
            text=f"Save {self.title}",
            command=self.save,
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            activebackground=styles.PRIMARY_HOVER,
            activeforeground=styles.WHITE,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        )
        self.save_button.grid(row=button_row, column=1, sticky="e", padx=8, pady=10)

        tk.Button(
            form,
            text="Clear",
            command=self.clear,
            bg=styles.SECONDARY,
            fg=styles.TEXT,
            activebackground=styles.BORDER,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        ).grid(row=button_row, column=0, sticky="w", padx=8, pady=10)

        actions = tk.Frame(self, bg=styles.WHITE)
        actions.pack(fill="x", pady=(0, 8))
        for label, command in (
            ("View Details", self.view_details),
            ("Edit Selected", self.edit_selected),
            ("Delete Selected", self.delete_selected),
        ):
            tk.Button(
                actions,
                text=label,
                command=command,
                bg=styles.SURFACE_SOFT,
                fg=styles.TEXT,
                activebackground=styles.SECONDARY,
                relief="solid",
                bd=1,
                padx=12,
                pady=6,
                cursor="hand2",
            ).pack(side="left", padx=(0, 8))

        tk.Label(
            self,
            text=f"{self.title} records",
            bg=styles.WHITE,
            fg=styles.TEXT,
            font=styles.FONT_HEADING,
        ).pack(anchor="w", pady=(4, 8))

        table_frame = tk.Frame(self, bg=styles.WHITE, highlightthickness=1, highlightbackground=styles.BORDER)
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

    def selected_id(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("No selection", f"Select a {self.title.lower()} first.")
            return None
        values = self.table.item(selected[0], "values")
        return values[0] if values else None

    def save(self):
        for rule in self.autofill_rules:
            self.apply_autofill(rule)
        data = self.values()
        missing = [
            field["label"]
            for field in self.fields
            if not field.get("optional")
            and not (self.editing_id and field.get("optional_on_update"))
            and data.get(field["key"], "") == ""
        ]
        if missing:
            messagebox.showwarning("Missing information", "Please fill in all fields.")
            return
        try:
            if self.editing_id:
                self.controller.update(self.editing_id, data)
            else:
                self.controller.create(data)
            self.clear()
            self.load()
            messagebox.showinfo("Saved", f"{self.title} saved successfully.")
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc))

    def clear(self):
        self.editing_id = None
        self.save_button.configure(text=f"Save {self.title}")
        for key, widget in self.inputs.items():
            previous_state = widget.cget("state") if hasattr(widget, "cget") else None
            if previous_state == "readonly":
                widget.configure(state="normal")
            if hasattr(widget, "delete"):
                widget.delete(0, tk.END)
            field = next((item for item in self.fields if item["key"] == key), {})
            if getattr(widget, "placeholder", None):
                widget.insert(0, widget.placeholder)
                widget.configure(fg=styles.MUTED)
            elif field.get("type") == "select" and widget["values"]:
                if field.get("value"):
                    widget.set(field.get("value"))
                else:
                    widget.current(0)
            if previous_state == "readonly":
                widget.configure(state="readonly")

    def set_input(self, key, value):
        widget = self.inputs.get(key)
        if not widget:
            return
        field = next((item for item in self.fields if item["key"] == key), {})
        previous_state = widget.cget("state") if hasattr(widget, "cget") else None
        if previous_state == "readonly":
            widget.configure(state="normal")
        if hasattr(widget, "delete"):
            widget.delete(0, tk.END)
        if field.get("type") == "select":
            display = value
            if field.get("relation"):
                collection_name = relation_collection(key)
                display = label_for(collection_name, value) if collection_name else value
            widget.set(display or "")
            if previous_state == "readonly":
                widget.configure(state="readonly")
            return
        widget.configure(fg=styles.TEXT)
        widget.insert(0, "" if value is None else value)
        if previous_state == "readonly":
            widget.configure(state="readonly")

    def bind_autofill(self):
        for rule in self.autofill_rules:
            widget = self.inputs.get(rule.get("trigger"))
            if widget:
                widget.bind("<<ComboboxSelected>>", lambda _event, item=rule: self.apply_autofill(item), add="+")
                widget.bind("<FocusOut>", lambda _event, item=rule: self.apply_autofill(item), add="+")
                widget.bind("<Return>", lambda _event, item=rule: self.apply_autofill(item), add="+")

    def apply_autofill(self, rule):
        trigger_key = rule.get("trigger")
        trigger_value = public_id_from_label(entry_value(self.inputs[trigger_key]))
        if not trigger_value:
            return
        db = get_db()
        if rule.get("mode") == "copy":
            document = db[rule["collection"]].find_one(document_query(trigger_value))
            if not document:
                return
            for source, target in rule.get("fields", {}).items():
                self.set_input(target, document.get(source, ""))
        elif rule.get("mode") == "lookup":
            document = db[rule["collection"]].find_one(
                {rule["match_field"]: {"$in": reference_values(relation_collection(trigger_key), trigger_value)}}
            )
            if document:
                self.set_input(rule["target"], document.get("public_id") or str(document.get("_id")))
        elif rule.get("mode") == "linked_user":
            collection_name = linked_collection_for_id(trigger_value)
            if not collection_name:
                self.set_input(rule["name_target"], "")
                self.set_input(rule["role_target"], "")
                return
            document = db[collection_name].find_one(document_query(trigger_value))
            self.set_input(rule["name_target"], document.get("full_name", "") if document else "")
            self.set_input(rule["role_target"], role_for_collection(collection_name) if document else "")

    def current_document(self):
        document_id = self.selected_id()
        if not document_id:
            return None
        document = self.controller.get(document_id)
        if not document:
            messagebox.showerror("Not found", f"Could not find {self.title.lower()} {document_id}.")
            return None
        return document

    def edit_selected(self):
        document = self.current_document()
        if not document:
            return
        self.editing_id = document.get("public_id") or str(document.get("_id"))
        self.save_button.configure(text=f"Update {self.title}")
        for field in self.fields:
            value = "" if field.get("optional_on_update") else document.get(field["key"], "")
            self.set_input(field["key"], value)
        for rule in self.autofill_rules:
            self.apply_autofill(rule)

    def delete_selected(self):
        document_id = self.selected_id()
        if not document_id:
            return
        confirmed = messagebox.askyesno("Delete record", f"Delete {self.title.lower()} {document_id}?")
        if not confirmed:
            return
        try:
            self.controller.delete(document_id)
            self.clear()
            self.load()
        except Exception as exc:
            messagebox.showerror("Delete failed", str(exc))

    def view_details(self):
        document = self.current_document()
        if not document:
            return
        window = tk.Toplevel(self)
        window.title(f"{self.title} details")
        window.geometry("560x520")
        body = tk.Frame(window, bg=styles.WHITE, padx=16, pady=16)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        keys = [key for key in self.detail_columns if key != "password"]
        for key in document.keys():
            if key not in keys and key not in ("_id", "password"):
                keys.append(key)
        for row, key in enumerate(keys):
            value = document.get(key, "")
            if key == "id":
                value = document.get("public_id") or str(document.get("_id"))
            else:
                value = display_value(key, value)
            tk.Label(body, text=key.replace("_", " ").title(), bg=styles.WHITE, fg=styles.MUTED).grid(
                row=row, column=0, sticky="nw", padx=(0, 12), pady=4
            )
            tk.Label(body, text=str(value), bg=styles.WHITE, fg=styles.TEXT, wraplength=360, justify="left").grid(
                row=row, column=1, sticky="nw", pady=4
            )

    def load(self):
        for item in self.table.get_children():
            self.table.delete(item)
        row_index = 0
        for document in self.controller.list_all(sort=[("created_at", -1)]):
            values = []
            for column in self.columns:
                if column == "id":
                    values.append(document.get("public_id") or str(document.get("_id")))
                else:
                    values.append(display_value(column, document.get(column, "")))
            tag = "even" if row_index % 2 else "odd"
            self.table.insert("", "end", values=values, tags=(tag,))
            row_index += 1
            for field, label in getattr(self.controller, "future_date_fields", {}).items():
                value = document.get(field)
                if value and is_due_soon(value):
                    warning = ["" for _column in self.columns]
                    if len(warning) > 1:
                        warning[1] = f"{label} for {document.get('public_id')} is almost due"
                    self.table.insert("", "end", values=warning, tags=("warning",))
                    row_index += 1


def linked_collection_for_id(value):
    prefix = str(value).strip().upper()[:1]
    return {"O": "owners", "D": "drivers", "C": "conductors", "S": "stage_managers"}.get(prefix)


def role_for_collection(collection_name):
    return {
        "owners": "owner",
        "drivers": "driver",
        "conductors": "conductor",
        "stage_managers": "stage_manager",
    }.get(collection_name, "")
