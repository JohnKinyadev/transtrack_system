from transtrack.models.base import with_timestamps


def trip_document(vehicle_id, driver_id, conductor_id, route_id, date, status="Scheduled"):
    return with_timestamps(
        {
            "vehicle_id": str(vehicle_id),
            "driver_id": str(driver_id),
            "conductor_id": str(conductor_id),
            "route_id": str(route_id),
            "date": date,
            "status": status,
            "departure_time": None,
            "arrival_time": None,
        }
    )
