from transtrack.controllers.driver_controller import DriverController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import vehicle_options


class DriversView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "full_name", "label": "Full Name"},
            {"key": "license_no", "label": "License No"},
            {"key": "license_expiry", "label": "License Expiry", "type": "date"},
            {"key": "contact", "label": "Contact"},
            {
                "key": "assigned_vehicle",
                "label": "Assigned Vehicle",
                "type": "select",
                "values": vehicle_options,
                "relation": True,
                "optional": True,
            },
            {"key": "cars_owned_count", "label": "Number of Cars Owned"},
            {"key": "owned_car_registrations", "label": "Owned Car Registrations"},
        ]
        columns = (
            "id",
            "full_name",
            "license_no",
            "license_expiry",
            "contact",
            "assigned_vehicle",
            "cars_owned_count",
            "owned_car_registrations",
        )
        super().__init__(master, DriverController(), "Driver", fields, columns)
