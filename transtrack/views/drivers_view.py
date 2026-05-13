from transtrack.controllers.driver_controller import DriverController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import vehicle_options


class DriversView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "full_name", "label": "Full Name"},
            {"key": "license_no", "label": "License No"},
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
        detail_columns = (
            "id",
            "full_name",
            "license_no",
            "contact",
            "assigned_vehicle",
        )
        columns = ("id", "full_name", "license_no", "contact", "assigned_vehicle")
        super().__init__(master, DriverController(), "Driver", fields, columns, detail_columns)
