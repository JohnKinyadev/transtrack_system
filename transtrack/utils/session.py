current_user = None


def login_user(user):
    global current_user
    current_user = user


def logout_user():
    global current_user
    current_user = None


def get_current_user():
    return current_user


def has_role(*roles):
    return current_user is not None and current_user.get("role") in roles
