from transtrack.models.base import with_timestamps


def conductor_document(full_name, contact, assigned_vehicle=None):
    return with_timestamps(
        {
            "full_name": full_name,
            "contact": contact,
            "assigned_vehicle": str(assigned_vehicle) if assigned_vehicle else None,
        }
    )
