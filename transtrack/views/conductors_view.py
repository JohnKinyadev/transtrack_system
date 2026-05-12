from transtrack.controllers.conductor_controller import ConductorController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import vehicle_options


class ConductorsView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "full_name", "label": "Full Name"},
            {"key": "contact", "label": "Contact"},
            {
                "key": "assigned_vehicle",
                "label": "Assigned Vehicle",
                "type": "select",
                "values": vehicle_options,
                "relation": True,
                "optional": True,
            },
        ]
        columns = ("id", "full_name", "contact", "assigned_vehicle")
        super().__init__(master, ConductorController(), "Conductor", fields, columns)
