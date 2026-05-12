from transtrack.db.connection import check_connection, create_indexes, get_db
from transtrack.utils.id_generator import next_public_id

ENTITY_PREFIXES = {
    "users": "U",
    "owners": "O",
    "vehicles": "V",
    "drivers": "D",
    "conductors": "C",
    "routes": "R",
    "trips": "T",
    "collections": "L",
    "expenses": "E",
    "deductions": "N",
    "payouts": "P",
}


def migrate():
    ok, message = check_connection()
    if not ok:
        print(message)
        return
    create_indexes()
    db = get_db()
    total = 0
    for collection_name, prefix in ENTITY_PREFIXES.items():
        collection = db[collection_name]
        for document in collection.find({"public_id": {"$exists": False}}):
            public_id = next_public_id(collection_name, prefix)
            collection.update_one({"_id": document["_id"]}, {"$set": {"public_id": public_id}})
            print(f"{collection_name}: {document['_id']} -> {public_id}")
            total += 1
    print(f"Migration complete. Updated {total} records.")


if __name__ == "__main__":
    migrate()
