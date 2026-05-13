from datetime import datetime, timedelta

from transtrack.controllers.collection_controller import CollectionController
from transtrack.controllers.deduction_controller import DeductionController
from transtrack.controllers.expense_controller import ExpenseController
from transtrack.controllers.base_controller import BaseController
from transtrack.utils.validators import parse_date, require_existing_public_id, validate_numeric


class PayoutController(BaseController):
    collection_name = "payouts"
    module_name = "payouts"
    id_prefix = "P"
    reference_fields = {
        "owner_id": {"collection": "owners", "label": "Owner ID"},
        "driver_id": {"collection": "drivers", "label": "Driver ID"},
    }

    def calculate_owner_payout(self, owner_id, period_start, period_days, driver_id="", interest_percent=0):
        if not owner_id:
            raise ValueError("Owner is required.")
        require_existing_public_id("owners", owner_id, "Owner ID")
        if driver_id:
            require_existing_public_id("drivers", driver_id, "Driver ID")
        start_date = parse_date(period_start, "Period start")
        numeric_days = validate_numeric(str(period_days), "Period days", allow_zero=False)
        if numeric_days != int(numeric_days):
            raise ValueError("Period days must be a whole number.")
        days = int(numeric_days)
        end_date = start_date + timedelta(days=days - 1)
        interest_percent = validate_numeric(str(interest_percent or 0), "Interest percent")
        vehicles = list(self.db_vehicles().find({"owner_id": owner_id}))
        gross = 0
        vehicle_expenses = 0
        collections = CollectionController()
        expense_controller = ExpenseController()
        for vehicle in vehicles:
            gross += collections.total_for_vehicle(vehicle["public_id"], start_date, end_date)
            vehicle_expenses += expense_controller.total_for_vehicle(vehicle["public_id"], start_date, end_date)
        owner_deductions = DeductionController().total_for_owner(owner_id, start_date, end_date)
        interest_amount = gross * (interest_percent / 100)
        total_deductions = vehicle_expenses + owner_deductions
        net = gross + interest_amount - total_deductions
        return {
            "owner_id": owner_id,
            "driver_id": driver_id,
            "period": f"{start_date:%Y-%m-%d} to {end_date:%Y-%m-%d}",
            "period_start": start_date.strftime("%Y-%m-%d"),
            "period_end": end_date.strftime("%Y-%m-%d"),
            "period_days": days,
            "gross_earnings": gross,
            "interest_percent": interest_percent,
            "interest_amount": interest_amount,
            "vehicle_expenses": vehicle_expenses,
            "owner_deductions": owner_deductions,
            "total_deductions": total_deductions,
            "net_payout": net,
            "date": datetime.now(),
        }

    def record_payout(self, owner_id, period_start, period_days, driver_id="", interest_percent=0):
        return self.create(
            self.calculate_owner_payout(owner_id, period_start, period_days, driver_id, interest_percent)
        )

    def db_vehicles(self):
        from transtrack.db.connection import get_db

        return get_db().vehicles
