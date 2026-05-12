from transtrack.config import ROLES
from transtrack.db.connection import get_db
from transtrack.models.base import with_timestamps
from transtrack.utils.audit import log_action
from transtrack.utils.id_generator import next_public_id
from transtrack.utils.security import hash_password, verify_password
from transtrack.utils.session import login_user, logout_user


class AuthController:
    def __init__(self):
        self.users = get_db().users

    def login(self, username, password):
        user = self.users.find_one({"username": username.strip().lower(), "status": "Active"})
        if user and verify_password(password, user.get("password", "")):
            login_user(user)
            log_action("login", "auth", {"username": username})
            return True, user
        return False, None

    def logout(self):
        log_action("logout", "auth")
        logout_user()

    def create_user(self, full_name, username, password, role, linked_id=None):
        if role not in ROLES:
            raise ValueError("Invalid role selected")
        payload = with_timestamps(
            {
                "full_name": full_name,
                "public_id": next_public_id("users", "U"),
                "username": username.strip().lower(),
                "password": hash_password(password),
                "role": role,
                "linked_id": str(linked_id) if linked_id else None,
                "permissions": [],
                "status": "Active",
            }
        )
        result = self.users.insert_one(payload)
        log_action("create", "users", {"id": str(result.inserted_id), "role": role})
        return result.inserted_id

    def ensure_seed_admin(self):
        if self.users.count_documents({}) == 0:
            return self.create_user("System Admin", "admin", "admin123", "admin")
        return None
