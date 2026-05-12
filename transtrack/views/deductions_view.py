from transtrack.controllers.deduction_controller import DeductionController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import owner_options


class DeductionsView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "owner_id", "label": "Owner", "type": "select", "values": owner_options, "relation": True},
            {"key": "type", "label": "Type", "type": "select", "values": ("SACCO_fee", "fine", "levy")},
            {"key": "amount", "label": "Amount"},
            {"key": "date", "label": "Date", "type": "date"},
            {"key": "reason", "label": "Reason"},
        ]
        columns = ("id", "owner_id", "type", "amount", "date", "reason")
        super().__init__(master, DeductionController(), "Deduction", fields, columns)
