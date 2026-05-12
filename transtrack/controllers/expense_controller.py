from datetime import datetime

from transtrack.controllers.base_controller import BaseController
from transtrack.utils.session import get_current_user


class ExpenseController(BaseController):
    collection_name = "expenses"
    module_name = "expenses"
    id_prefix = "E"
    reference_fields = {
        "trip_id": {"collection": "trips", "label": "Trip ID"},
        "vehicle_id": {"collection": "vehicles", "label": "Vehicle ID"},
    }
    not_future_date_fields = {"date": "Expense date"}

    def log_expense(self, trip_id, vehicle_id, expense_type, amount):
        user = get_current_user()
        return self.create(
            {
                "trip_id": trip_id,
                "vehicle_id": vehicle_id,
                "type": expense_type,
                "amount": float(amount),
                "logged_by": str(user.get("_id")) if user else None,
                "date": datetime.now(),
            }
        )

    def total_for_vehicle(self, vehicle_id):
        rows = self.collection.aggregate(
            [
                {"$match": {"vehicle_id": vehicle_id}},
                {"$group": {"_id": "$vehicle_id", "total": {"$sum": "$amount"}}},
            ]
        )
        row = next(rows, None)
        return row["total"] if row else 0
