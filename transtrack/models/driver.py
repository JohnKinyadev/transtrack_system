from transtrack.models.base import with_timestamps


def driver_document(full_name, license_no, license_expiry, contact, assigned_vehicle=None):
    return with_timestamps(
        {
            "full_name": full_name,
            "license_no": license_no,
            "license_expiry": license_expiry,
            "contact": contact,
            "assigned_vehicle": str(assigned_vehicle) if assigned_vehicle else None,
        }
    )
