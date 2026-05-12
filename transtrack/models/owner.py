from transtrack.models.base import with_timestamps


def owner_document(full_name, contact, email, national_id, shares, status="Active"):
    return with_timestamps(
        {
            "full_name": full_name,
            "contact": contact,
            "email": email,
            "national_id": national_id,
            "shares": shares,
            "join_date": None,
            "status": status,
        }
    )
