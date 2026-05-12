from transtrack.models.base import with_timestamps


def vehicle_document(plate, make, model, capacity, owner_id, route_id=None, status="Active"):
    return with_timestamps(
        {
            "plate": plate,
            "make": make,
            "model": model,
            "capacity": capacity,
            "owner_id": str(owner_id),
            "route_id": str(route_id) if route_id else None,
            "status": status,
            "insurance_expiry": None,
            "inspection_expiry": None,
        }
    )
