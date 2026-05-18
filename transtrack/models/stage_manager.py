from transtrack.models.base import with_timestamps


def stage_manager_document(full_name, contact, stage_name=""):
    return with_timestamps(
        {
            "full_name": full_name,
            "contact": contact,
            "stage_name": stage_name,
        }
    )
