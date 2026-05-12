from transtrack.config import ROLES
from transtrack.controllers.auth_controller import AuthController
from transtrack.views.crud_view import CrudView


class UserManagementView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "full_name", "label": "Full Name"},
            {"key": "username", "label": "Username"},
            {"key": "password", "label": "Password"},
            {"key": "role", "label": "Role", "type": "select", "values": tuple(ROLES.keys())},
            {"key": "linked_id", "label": "Linked Owner/Driver/Conductor ID"},
        ]
        columns = ("id", "full_name", "username", "role", "linked_id", "status")
        super().__init__(master, AuthControllerAdapter(), "User", fields, columns)


class AuthControllerAdapter:
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
