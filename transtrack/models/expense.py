from transtrack.models.base import with_timestamps
from transtrack.utils.numbers import to_float


def expense_document(trip_id, vehicle_id, expense_type, amount, logged_by, date):
    return with_timestamps(
        {
            "trip_id": str(trip_id),
            "vehicle_id": str(vehicle_id),
            "type": expense_type,
            "amount": to_float(amount),
            "logged_by": str(logged_by),
            "date": date,
        }
    )
