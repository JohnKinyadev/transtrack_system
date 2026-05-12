"""Application configuration."""

import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "TransTrack"
MONGO_URI = os.getenv("TRANSTRACK_MONGO_URI", "mongodb://localhost:27017/")
MONGO_TIMEOUT_MS = int(os.getenv("TRANSTRACK_MONGO_TIMEOUT_MS", "10000"))
DATABASE_NAME = "transtrack_db"

ROLES = {
    "admin": "Company Admin",
    "operations": "Operations Manager",
    "owner": "Vehicle Owner",
    "driver": "Driver",
    "conductor": "Conductor",
}

TRIP_STATUSES = ("Scheduled", "Departed", "In Transit", "Completed")
VEHICLE_STATUSES = ("Active", "Inactive", "Maintenance")
OWNER_STATUSES = ("Active", "Inactive")
