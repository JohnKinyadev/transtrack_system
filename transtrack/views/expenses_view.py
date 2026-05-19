from tkinter import messagebox

from transtrack.controllers.expense_controller import ExpenseController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import trip_options, vehicle_options
from transtrack.views.widgets import entry_value


class ExpensesView(CrudView):
    def __init__(self, master, trip_only_for_fuel=False):
        self.trip_only_for_fuel = trip_only_for_fuel
        fields = [
            {
                "key": "trip_id",
                "label": "Trip",
                "type": "select",
                "values": trip_options,
                "relation": True,
                "optional": trip_only_for_fuel,
            },
            {"key": "vehicle_id", "label": "Vehicle", "type": "select", "values": vehicle_options, "relation": True},
            {"key": "type", "label": "Type", "type": "select", "values": ("fuel", "toll", "allowance", "repair", "service")},
            {"key": "amount", "label": "Amount"},
            {"key": "date", "label": "Date", "type": "date"},
        ]
        detail_columns = ("id", "trip_id", "vehicle_id", "type", "amount", "date", "logged_by")
        columns = ("id", "vehicle_id", "type", "amount", "date")
        autofill_rules = [
            {"trigger": "trip_id", "mode": "copy", "collection": "trips", "fields": {"vehicle_id": "vehicle_id"}},
        ]
        super().__init__(master, ExpenseController(), "Expense", fields, columns, detail_columns, autofill_rules)
        if self.trip_only_for_fuel:
            self.bind_trip_visibility()
            self.sync_trip_visibility()

    def bind_trip_visibility(self):
        type_input = self.inputs.get("type")
        if type_input:
            type_input.bind("<<ComboboxSelected>>", lambda _event: self.sync_trip_visibility(), add="+")
            type_input.bind("<FocusOut>", lambda _event: self.sync_trip_visibility(), add="+")

    def sync_trip_visibility(self):
        trip_input = self.inputs.get("trip_id")
        type_input = self.inputs.get("type")
        if not trip_input or not type_input:
            return
        show_trip = entry_value(type_input).lower() == "fuel"
        label = getattr(trip_input, "label_widget", None)
        widget = getattr(trip_input, "grid_widget", trip_input)
        if show_trip:
            if label:
                label.grid()
            widget.grid()
            return
        if label:
            label.grid_remove()
        widget.grid_remove()
        previous_state = trip_input.cget("state") if hasattr(trip_input, "cget") else None
        if previous_state == "readonly":
            trip_input.configure(state="normal")
        if hasattr(trip_input, "delete"):
            trip_input.delete(0, "end")
        if previous_state == "readonly":
            trip_input.configure(state="readonly")

    def values(self):
        data = super().values()
        if self.trip_only_for_fuel and data.get("type", "").lower() != "fuel":
            data["trip_id"] = ""
        return data

    def save(self):
        if self.trip_only_for_fuel:
            self.sync_trip_visibility()
            if entry_value(self.inputs["type"]).lower() == "fuel" and not entry_value(self.inputs["trip_id"]):
                messagebox.showwarning("Missing information", "Please select a trip for fuel expenses.")
                return
        super().save()
        if self.trip_only_for_fuel:
            self.sync_trip_visibility()
