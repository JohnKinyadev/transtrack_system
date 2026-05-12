from transtrack.models.base import with_timestamps


def route_document(name, origin, destination, stages, fare_structure, expected_revenue=0):
    return with_timestamps(
        {
            "name": name,
            "origin": origin,
            "destination": destination,
            "stages": stages,
            "fare_structure": fare_structure,
            "expected_revenue": float(expected_revenue or 0),
        }
    )
