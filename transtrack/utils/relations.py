from bson import ObjectId

from transtrack.db.connection import get_db


def document_query(document_id):
    text_id = str(document_id or "").strip()
    if not text_id:
        return {"_id": None}
    if ObjectId.is_valid(text_id):
        return {"$or": [{"public_id": text_id}, {"_id": ObjectId(text_id)}]}
    return {"public_id": text_id}


def resolve_document(collection_name, document_id):
    if not document_id:
        return None
    return get_db()[collection_name].find_one(document_query(document_id))


def reference_values(collection_name, document_id):
    values = set()
    text_id = str(document_id or "").strip()
    if text_id:
        values.add(text_id)

    document = resolve_document(collection_name, document_id)
    if document:
        if document.get("public_id"):
            values.add(str(document.get("public_id")))
        if document.get("_id"):
            values.add(str(document.get("_id")))

    return list(values)


def reference_query(field, collection_name, document_id):
    return {field: {"$in": reference_values(collection_name, document_id)}}
