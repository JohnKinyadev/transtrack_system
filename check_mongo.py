from transtrack.db.connection import check_connection
from transtrack.config import MONGO_URI


def masked_uri(uri):
    if "://" not in uri or "@" not in uri:
        return uri
    scheme, rest = uri.split("://", 1)
    credentials, host = rest.split("@", 1)
    username = credentials.split(":", 1)[0]
    return f"{scheme}://{username}:***@{host}"


if __name__ == "__main__":
    print("Mongo URI:", masked_uri(MONGO_URI))
    ok, message = check_connection()
    print("Status:", "OK" if ok else "FAILED")
    print(message)
