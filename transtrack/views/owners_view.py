from transtrack.controllers.owner_controller import OwnerController
from transtrack.config import OWNER_STATUSES
from transtrack.views.crud_view import CrudView


class OwnersView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "full_name", "label": "Full Name"},
            {"key": "contact", "label": "Contact"},
            {"key": "email", "label": "Email"},
            {"key": "national_id", "label": "National ID"},
            {"key": "shares", "label": "Shares"},
            {"key": "status", "label": "Status", "type": "select", "values": OWNER_STATUSES},
        ]
        detail_columns = ("id", "full_name", "contact", "email", "national_id", "shares", "status")
        columns = ("id", "full_name", "contact", "status")
        super().__init__(master, OwnerController(), "Owner", fields, columns, detail_columns)
