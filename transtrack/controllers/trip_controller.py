from transtrack.config import TRIP_STATUSES
from transtrack.controllers.base_controller import BaseController
from transtrack.utils.audit import log_action
from transtrack.utils.relations import reference_query
from transtrack.utils.session import get_current_user


class TripController(BaseController):
    collection_name = "trips"
    module_name = "trips"
    id_prefix = "T"
    reference_fields = {
        "vehicle_id": {"collection": "vehicles", "label": "Vehicle ID"},
        "driver_id": {"collection": "drivers", "label": "Driver ID"},
        "conductor_id": {"collection": "conductors", "label": "Conductor ID"},
        "route_id": {"collection": "routes", "label": "Route ID"},
        "stage_manager_id": {"collection": "stage_managers", "label": "Stage Manager ID"},
    }
    future_date_fields = {"date": "Trip date"}

    def create(self, data):
        user = get_current_user() or {}
        if user.get("role") == "stage_manager" and user.get("linked_id"):
            data = dict(data)
            data["stage_manager_id"] = user.get("linked_id")
        return super().create(data)

    def list_for_driver(self, driver_id):
        return self.list_all(reference_query("driver_id", "drivers", driver_id), [("date", -1)])

    def list_for_conductor(self, conductor_id):
        return self.list_all(reference_query("conductor_id", "conductors", conductor_id), [("date", -1)])

    def list_for_vehicle(self, vehicle_id):
        return self.list_all(reference_query("vehicle_id", "vehicles", vehicle_id), [("date", -1)])

    def update_status(self, trip_id, status):
        if status not in TRIP_STATUSES:
            raise ValueError("Invalid trip status")
        changed = self.update(trip_id, {"status": status})
        log_action("status_update", "trips", {"trip_id": str(trip_id), "status": status})
        return changed
