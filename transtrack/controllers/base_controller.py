from transtrack.db.connection import get_db
from transtrack.models.base import with_timestamps
from transtrack.utils.audit import log_action
from transtrack.utils.id_generator import next_public_id
from transtrack.utils.relations import document_query
from transtrack.utils.validators import (
    require_existing_public_id,
    validate_date_format,
    validate_future_date,
    validate_not_future_date,
)


class BaseController:
    collection_name = ""
    module_name = ""
    id_prefix = ""
    reference_fields = {}
    date_fields = {}
    future_date_fields = {}
    not_future_date_fields = {}

    def __init__(self):
        self.collection = get_db()[self.collection_name]

    def list_all(self, query=None, sort=None):
        cursor = self.collection.find(query or {})
        if sort:
            cursor = cursor.sort(sort)
        return list(cursor)

    def id_filter(self, document_id):
        return document_query(document_id)

    def get(self, document_id):
        return self.collection.find_one(self.id_filter(document_id))

    def create(self, data):
        self.validate(data)
        if self.id_prefix and not data.get("public_id"):
            data["public_id"] = next_public_id(self.collection_name, self.id_prefix)
        result = self.collection.insert_one(with_timestamps(data))
        log_action("create", self.module_name, {"id": str(result.inserted_id), "public_id": data.get("public_id")})
        return result.inserted_id

    def update(self, document_id, data):
        self.validate(data)
        result = self.collection.update_one(
            self.id_filter(document_id),
            {"$set": with_timestamps(data, is_new=False)},
        )
        log_action("update", self.module_name, {"id": str(document_id)})
        return result.modified_count

    def delete(self, document_id):
        result = self.collection.delete_one(self.id_filter(document_id))
        log_action("delete", self.module_name, {"id": str(document_id)})
        return result.deleted_count

    def deactivate(self, document_id):
        return self.update(document_id, {"status": "Inactive"})

    def validate(self, data):
        for field, rule in self.reference_fields.items():
            value = data.get(field)
            if value:
                require_existing_public_id(rule["collection"], value, rule["label"])
        for field, label in self.date_fields.items():
            value = data.get(field)
            if value:
                validate_date_format(value, label)
        for field, label in self.future_date_fields.items():
            value = data.get(field)
            if value:
                validate_future_date(value, label)
        for field, label in self.not_future_date_fields.items():
            value = data.get(field)
            if value:
                validate_not_future_date(value, label)
