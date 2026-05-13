from transtrack.db.connection import get_db


DISPLAY_FIELDS = {
    "owners": ("full_name",),
    "vehicles": ("plate", "make", "model"),
    "drivers": ("full_name",),
    "conductors": ("full_name",),
    "routes": ("name",),
    "trips": ("date", "status"),
}


def document_label(document, *name_fields):
    public_id = document.get("public_id") or str(document.get("_id"))
    label_bits = [str(document.get(field, "")) for field in name_fields if document.get(field)]
    if label_bits:
        return f"{public_id} - {' '.join(label_bits)}"
    return public_id


def public_id_from_label(value):
    return value.split(" - ", 1)[0].strip() if value else ""


def options(collection_name, *name_fields):
    rows = get_db()[collection_name].find({}).sort("public_id", 1)
    return [document_label(row, *name_fields) for row in rows]


def label_for(collection_name, public_id):
    if not public_id:
        return ""
    document = get_db()[collection_name].find_one({"public_id": public_id})
    if not document:
        return public_id
    return document_label(document, *DISPLAY_FIELDS.get(collection_name, ()))


def display_value(column, value):
    collection_name = relation_collection(column)
    if collection_name:
        return label_for(collection_name, value)
    return value


def relation_collection(column):
    relation_map = {
        "owner_id": "owners",
        "vehicle_id": "vehicles",
        "assigned_vehicle": "vehicles",
        "driver_id": "drivers",
        "conductor_id": "conductors",
        "route_id": "routes",
        "trip_id": "trips",
    }
    return relation_map.get(column)


def owner_options():
    return options("owners", "full_name")


def vehicle_options():
    return options("vehicles", "plate", "make", "model")


def driver_options():
    return options("drivers", "full_name")


def conductor_options():
    return options("conductors", "full_name")


def route_options():
    return options("routes", "name")


def trip_options():
    return options("trips", "date", "status")
