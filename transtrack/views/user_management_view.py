from transtrack.config import ROLES
from transtrack.controllers.auth_controller import AuthController
from transtrack.models.base import to_object_id, with_timestamps
from transtrack.utils.security import hash_password
from transtrack.views.crud_view import CrudView


class UserManagementView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "full_name", "label": "Full Name"},
            {"key": "username", "label": "Username"},
            {"key": "password", "label": "Password", "optional_on_update": True},
            {"key": "role", "label": "Role", "type": "select", "values": tuple(ROLES.keys())},
            {"key": "linked_id", "label": "Linked Owner/Driver/Conductor ID"},
        ]
        detail_columns = ("id", "full_name", "username", "role", "linked_id", "status")
        columns = ("id", "full_name", "username", "role", "status")
        super().__init__(master, AuthControllerAdapter(), "User", fields, columns, detail_columns)


class AuthControllerAdapter:
    id_prefix = "U"

    def __init__(self):
        self.auth = AuthController()
        self.collection = self.auth.users

    def create(self, data):
        return self.auth.create_user(
            data["full_name"], data["username"], data["password"], data["role"], data.get("linked_id")
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
        if payload.get("password"):
            payload["password"] = hash_password(payload["password"])
        else:
            payload.pop("password", None)
        if payload.get("username"):
            payload["username"] = payload["username"].strip().lower()
        return self.collection.update_one(self.id_filter(document_id), {"$set": with_timestamps(payload, is_new=False)}).modified_count

    def delete(self, document_id):
        return self.collection.delete_one(self.id_filter(document_id)).deleted_count
