from transtrack.models.base import with_timestamps


def collection_document(trip_id, vehicle_id, conductor_id, amount_collected, date):
    return with_timestamps(
        {
            "trip_id": str(trip_id),
            "vehicle_id": str(vehicle_id),
            "conductor_id": str(conductor_id),
            "amount_collected": float(amount_collected),
            "date": date,
        }
    )
