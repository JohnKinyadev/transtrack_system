from datetime import datetime

from bson import ObjectId


def now():
    return datetime.now()


def with_timestamps(data, is_new=True):
    payload = dict(data)
    payload["updated_at"] = now()
    if is_new:
        payload["created_at"] = now()
    return payload


def to_object_id(value):
    if isinstance(value, ObjectId):
        return value
    if value in (None, ""):
        return None
    return ObjectId(value)
