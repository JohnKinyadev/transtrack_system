from transtrack.models.base import with_timestamps
from transtrack.utils.security import hash_password


def user_document(full_name, username, password, role, linked_id=None):
    return with_timestamps(
        {
            "full_name": full_name,
            "username": username.strip().lower(),
            "password": hash_password(password),
            "role": role,
            "permissions": [],
            "linked_id": str(linked_id) if linked_id else None,
            "status": "Active",
        }
    )
