from transtrack.models.base import with_timestamps


def deduction_document(owner_id, deduction_type, amount, date, reason):
    return with_timestamps(
        {
            "owner_id": str(owner_id),
            "type": deduction_type,
            "amount": float(amount),
            "date": date,
            "reason": reason,
        }
    )
