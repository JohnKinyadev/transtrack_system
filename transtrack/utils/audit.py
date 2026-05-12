from datetime import datetime

from transtrack.db.connection import get_db
from transtrack.utils.session import get_current_user


def log_action(action, module, details=None):
    user = get_current_user()
    get_db().audit_logs.insert_one(
        {
            "user_id": str(user.get("_id")) if user else None,
            "username": user.get("username") if user else "system",
            "action": action,
            "module": module,
            "timestamp": datetime.now(),
            "details": details or {},
        }
    )
