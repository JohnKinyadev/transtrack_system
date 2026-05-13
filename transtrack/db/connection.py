import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConfigurationError, OperationFailure, PyMongoError, ServerSelectionTimeoutError

from transtrack.config import DATABASE_NAME, MONGO_TIMEOUT_MS, MONGO_URI

_client = None
_db = None


def _uses_tls(uri):
    normalized = uri.lower()
    return (
        normalized.startswith("mongodb+srv://")
        or "tls=true" in normalized
        or "ssl=true" in normalized
    )


def get_client():
    global _client
    if _client is None:
        options = {
            "serverSelectionTimeoutMS": MONGO_TIMEOUT_MS,
            "connectTimeoutMS": MONGO_TIMEOUT_MS,
            "socketTimeoutMS": MONGO_TIMEOUT_MS,
        }
        if _uses_tls(MONGO_URI):
            options["tlsCAFile"] = certifi.where()
            options["server_api"] = ServerApi("1")

        _client = MongoClient(
            MONGO_URI,
            **options,
        )
    return _client


def get_db():
    global _db
    if _db is None:
        _db = get_client()[DATABASE_NAME]
    return _db


def check_connection():
    global _client, _db
    try:
        get_client().admin.command("ping")
        return True, "Connected to MongoDB"
    except OperationFailure as exc:
        return False, f"MongoDB authentication failed: {exc}"
    except ConfigurationError as exc:
        if "resolution lifetime expired" in str(exc).lower():
            return False, f"MongoDB DNS lookup timed out: {exc}"
        return False, f"MongoDB connection string is invalid: {exc}"
    except ServerSelectionTimeoutError as exc:
        return False, f"MongoDB connection failed: {exc}"
    except PyMongoError as exc:
        return False, f"MongoDB error: {exc}"
    finally:
        if _client is not None:
            _client.close()
            _client = None
            _db = None


def create_indexes():
    db = get_db()
    db.users.create_index("username", unique=True)
    db.users.create_index("public_id", unique=True, sparse=True)
    db.owners.create_index("national_id", unique=True, sparse=True)
    db.owners.create_index("public_id", unique=True, sparse=True)
    db.vehicles.create_index("plate", unique=True)
    db.vehicles.create_index("public_id", unique=True, sparse=True)
    db.drivers.create_index("license_no", unique=True, sparse=True)
    db.drivers.create_index("public_id", unique=True, sparse=True)
    db.conductors.create_index("public_id", unique=True, sparse=True)
    db.routes.create_index("public_id", unique=True, sparse=True)
    db.trips.create_index("public_id", unique=True, sparse=True)
    db.collections.create_index("public_id", unique=True, sparse=True)
    db.expenses.create_index("public_id", unique=True, sparse=True)
    db.deductions.create_index("public_id", unique=True, sparse=True)
    db.payouts.create_index("public_id", unique=True, sparse=True)
    db.trips.create_index([("vehicle_id", 1), ("date", -1)])
    db.collections.create_index("trip_id")
    db.expenses.create_index("trip_id")
