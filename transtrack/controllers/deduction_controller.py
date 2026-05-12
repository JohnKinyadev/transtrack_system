from datetime import datetime

from transtrack.controllers.base_controller import BaseController


class DeductionController(BaseController):
    collection_name = "deductions"
    module_name = "deductions"
    id_prefix = "N"
    reference_fields = {
        "owner_id": {"collection": "owners", "label": "Owner ID"},
    }
    not_future_date_fields = {"date": "Deduction date"}

    def add_deduction(self, owner_id, deduction_type, amount, reason):
        return self.create(
            {
                "owner_id": owner_id,
                "type": deduction_type,
                "amount": float(amount),
                "date": datetime.now(),
                "reason": reason,
            }
        )

    def total_for_owner(self, owner_id):
        rows = self.collection.aggregate(
            [
                {"$match": {"owner_id": owner_id}},
                {"$group": {"_id": "$owner_id", "total": {"$sum": "$amount"}}},
            ]
        )
        row = next(rows, None)
        return row["total"] if row else 0
