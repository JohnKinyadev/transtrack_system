from transtrack.models.base import with_timestamps
from transtrack.utils.numbers import to_float


def deduction_document(owner_id, deduction_type, amount, date, reason):
    return with_timestamps(
        {
            "owner_id": str(owner_id),
            "type": deduction_type,
            "amount": to_float(amount),
            "date": date,
            "reason": reason,
        }
    )
