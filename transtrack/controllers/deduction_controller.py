from datetime import datetime

from transtrack.controllers.base_controller import BaseController
from transtrack.utils.validators import parse_date


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

    def total_for_owner(self, owner_id, start_date=None, end_date=None):
        total = 0
        for row in self.collection.find({"owner_id": owner_id}):
            if not _in_date_range(row.get("date"), start_date, end_date):
                continue
            total += float(row.get("amount") or 0)
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
