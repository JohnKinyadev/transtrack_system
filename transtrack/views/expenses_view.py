from transtrack.controllers.expense_controller import ExpenseController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import trip_options, vehicle_options


class ExpensesView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "trip_id", "label": "Trip", "type": "select", "values": trip_options, "relation": True},
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
