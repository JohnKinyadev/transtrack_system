from pymongo import ReturnDocument

from transtrack.db.connection import get_db


def next_public_id(sequence_name, prefix):
    counter = get_db().counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return f"{prefix}{counter['value']:04d}"
