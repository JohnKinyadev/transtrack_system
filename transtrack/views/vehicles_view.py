from transtrack.config import VEHICLE_STATUSES
from transtrack.controllers.vehicle_controller import VehicleController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import owner_options, route_options


class VehiclesView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "plate", "label": "Plate"},
            {"key": "make", "label": "Make"},
            {"key": "model", "label": "Model"},
            {"key": "capacity", "label": "Capacity"},
            {"key": "owner_id", "label": "Owner", "type": "select", "values": owner_options, "relation": True},
            {"key": "route_id", "label": "Route", "type": "select", "values": route_options, "relation": True, "optional": True},
            {"key": "insurance_expiry", "label": "Insurance Expiry", "type": "date"},
            {"key": "inspection_expiry", "label": "Inspection Expiry", "type": "date"},
            {"key": "status", "label": "Status", "type": "select", "values": VEHICLE_STATUSES},
        ]
        detail_columns = (
            "id",
            "plate",
            "make",
            "model",
            "capacity",
            "owner_id",
            "route_id",
            "insurance_expiry",
            "inspection_expiry",
            "status",
        )
        columns = ("id", "plate", "make", "model", "owner_id", "status")
        super().__init__(master, VehicleController(), "Vehicle", fields, columns, detail_columns)
