from datetime import datetime

from transtrack.controllers.base_controller import BaseController


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
                "amount_collected": float(amount),
                "date": datetime.now(),
            }
        )

    def total_for_vehicle(self, vehicle_id):
        rows = self.collection.aggregate(
            [
                {"$match": {"vehicle_id": vehicle_id}},
                {"$group": {"_id": "$vehicle_id", "total": {"$sum": "$amount_collected"}}},
            ]
        )
        row = next(rows, None)
        return row["total"] if row else 0
