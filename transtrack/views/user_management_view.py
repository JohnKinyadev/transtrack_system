from transtrack.controllers.auth_controller import AuthController
from transtrack.db.connection import get_db
from transtrack.models.base import to_object_id, with_timestamps
from transtrack.utils.relations import document_query
from transtrack.utils.security import hash_password
from transtrack.views.crud_view import CrudView, linked_collection_for_id, role_for_collection


class UserManagementView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "linked_id", "label": "Owner/Driver/Conductor/Stage Manager ID"},
            {"key": "linked_name", "label": "Linked Name", "readonly": True, "optional": True},
            {"key": "role", "label": "Role", "readonly": True, "optional": True},
            {"key": "username", "label": "Username"},
            {"key": "password", "label": "Password", "optional_on_update": True},
        ]
        detail_columns = ("id", "full_name", "username", "role", "linked_id", "status")
        columns = ("id", "full_name", "username", "role", "status")
        autofill_rules = [
            {
                "trigger": "linked_id",
                "mode": "linked_user",
                "name_target": "linked_name",
                "role_target": "role",
            }
        ]
        super().__init__(master, AuthControllerAdapter(), "User", fields, columns, detail_columns, autofill_rules)


class AuthControllerAdapter:
    id_prefix = "U"

    def __init__(self):
        self.auth = AuthController()
        self.collection = self.auth.users

    def create(self, data):
        linked = resolve_linked_user(data.get("linked_id"))
        return self.auth.create_user(
            linked["full_name"], data["username"], data["password"], linked["role"], data.get("linked_id")
        )

    def list_all(self, query=None, sort=None):
        cursor = self.collection.find(query or {}, {"password": 0})
        if sort:
            cursor = cursor.sort(sort)
        return list(cursor)

    def id_filter(self, document_id):
        text_id = str(document_id)
        if text_id.startswith(self.id_prefix):
            return {"public_id": text_id}
        return {"_id": to_object_id(document_id)}

    def get(self, document_id):
        return self.collection.find_one(self.id_filter(document_id), {"password": 0})

    def update(self, document_id, data):
        payload = dict(data)
        payload.pop("linked_name", None)
        if payload.get("linked_id"):
            linked = resolve_linked_user(payload.get("linked_id"))
            payload["full_name"] = linked["full_name"]
            payload["role"] = linked["role"]
        if payload.get("password"):
            payload["password"] = hash_password(payload["password"])
        else:
            payload.pop("password", None)
        if payload.get("username"):
            payload["username"] = payload["username"].strip().lower()
        return self.collection.update_one(self.id_filter(document_id), {"$set": with_timestamps(payload, is_new=False)}).modified_count

    def delete(self, document_id):
        return self.collection.delete_one(self.id_filter(document_id)).deleted_count


def resolve_linked_user(linked_id):
    collection_name = linked_collection_for_id(linked_id)
    if not collection_name:
        raise ValueError("Linked ID must start with O, D, C, or S.")
    document = get_db()[collection_name].find_one(document_query(linked_id))
    if not document:
        raise ValueError(f"No owner, driver, conductor, or stage manager found for ID '{linked_id}'.")
    return {"full_name": document.get("full_name", ""), "role": role_for_collection(collection_name)}
