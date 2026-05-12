from transtrack.config import TRIP_STATUSES
from transtrack.controllers.base_controller import BaseController
from transtrack.models.base import to_object_id
from transtrack.utils.audit import log_action


class TripController(BaseController):
    collection_name = "trips"
    module_name = "trips"
    id_prefix = "T"
    reference_fields = {
        "vehicle_id": {"collection": "vehicles", "label": "Vehicle ID"},
        "driver_id": {"collection": "drivers", "label": "Driver ID"},
        "conductor_id": {"collection": "conductors", "label": "Conductor ID"},
        "route_id": {"collection": "routes", "label": "Route ID"},
    }
    future_date_fields = {"date": "Trip date"}

    def list_for_driver(self, driver_id):
        return self.list_all({"driver_id": driver_id}, [("date", -1)])

    def list_for_conductor(self, conductor_id):
        return self.list_all({"conductor_id": conductor_id}, [("date", -1)])

    def list_for_vehicle(self, vehicle_id):
        return self.list_all({"vehicle_id": vehicle_id}, [("date", -1)])

    def update_status(self, trip_id, status):
        if status not in TRIP_STATUSES:
            raise ValueError("Invalid trip status")
        changed = self.update(trip_id, {"status": status})
        log_action("status_update", "trips", {"trip_id": str(trip_id), "status": status})
        return changed
