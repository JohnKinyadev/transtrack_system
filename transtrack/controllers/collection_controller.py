from datetime import datetime

from transtrack.controllers.base_controller import BaseController
from transtrack.utils.numbers import to_float
from transtrack.utils.relations import reference_query
from transtrack.utils.validators import parse_date


class CollectionController(BaseController):
    collection_name = "collections"
    module_name = "collections"
    id_prefix = "L"
    reference_fields = {
        "trip_id": {"collection": "trips", "label": "Trip ID"},
        "vehicle_id": {"collection": "vehicles", "label": "Vehicle ID"},
        "conductor_id": {"collection": "conductors", "label": "Conductor ID"},
    }
    not_future_date_fields = {"date": "Collection date"}

    def log_collection(self, trip_id, vehicle_id, conductor_id, amount):
        return self.create(
            {
                "trip_id": trip_id,
                "vehicle_id": vehicle_id,
                "conductor_id": conductor_id,
                "amount_collected": to_float(amount),
                "date": datetime.now(),
            }
        )

    def total_for_vehicle(self, vehicle_id, start_date=None, end_date=None):
        total = 0
        for row in self.collection.find(reference_query("vehicle_id", "vehicles", vehicle_id)):
            if not _in_date_range(row.get("date"), start_date, end_date):
                continue
            total += to_float(row.get("amount_collected"))
        return total


def _in_date_range(value, start_date=None, end_date=None):
    if not start_date and not end_date:
        return True
    try:
        parsed = parse_date(value)
    except ValueError:
        return False
    if start_date and parsed < start_date:
        return False
    if end_date and parsed > end_date:
        return False
    return True
