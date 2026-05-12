from transtrack.controllers.base_controller import BaseController
from transtrack.models.base import to_object_id


class VehicleController(BaseController):
    collection_name = "vehicles"
    module_name = "vehicles"
    id_prefix = "V"
    reference_fields = {
        "owner_id": {"collection": "owners", "label": "Owner ID"},
        "route_id": {"collection": "routes", "label": "Route ID"},
    }
    future_date_fields = {
        "insurance_expiry": "Insurance expiry",
        "inspection_expiry": "Inspection expiry",
    }

    def list_for_owner(self, owner_id):
        return self.list_all({"owner_id": owner_id})
