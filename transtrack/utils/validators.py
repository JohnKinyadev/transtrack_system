from datetime import date, datetime, timedelta

from transtrack.db.connection import get_db
from transtrack.utils.relations import document_query

DATE_FORMAT = "%Y-%m-%d"
PERIOD_FORMAT = "%Y-%m"


def parse_date(value, field_name="Date"):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(value, DATE_FORMAT).date()
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format.") from exc


def validate_future_date(value, field_name):
    parsed = parse_date(value, field_name)
    if parsed < datetime.now().date():
        raise ValueError(f"{field_name} cannot be in the past.")
    return parsed


def validate_not_future_date(value, field_name):
    parsed = parse_date(value, field_name)
    if parsed > datetime.now().date():
        raise ValueError(f"{field_name} cannot be in the future.")
    return parsed


def validate_date_format(value, field_name):
    return parse_date(value, field_name)


def validate_period(value):
    try:
        datetime.strptime(value, PERIOD_FORMAT)
    except ValueError as exc:
        raise ValueError("Period must use YYYY-MM format, for example 2026-05.") from exc


def is_due_soon(value, days=30):
    try:
        parsed = parse_date(value)
    except ValueError:
        return False
    today = datetime.now().date()
    return today <= parsed <= today + timedelta(days=days)


def require_existing_public_id(collection_name, public_id, label):
    if public_id in (None, ""):
        return
    exists = get_db()[collection_name].find_one(document_query(public_id))
    if not exists:
        raise ValueError(f"{label} '{public_id}' does not exist.")


def validate_numeric(value, field_name, allow_zero=True):
    try:
        number = float(str(value or 0).replace(",", "").strip())
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a number.") from exc
    if allow_zero and number < 0:
        raise ValueError(f"{field_name} cannot be negative.")
    if not allow_zero and number <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")
    return number
