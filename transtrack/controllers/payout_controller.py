from datetime import datetime

from transtrack.controllers.collection_controller import CollectionController
from transtrack.controllers.deduction_controller import DeductionController
from transtrack.controllers.expense_controller import ExpenseController
from transtrack.controllers.base_controller import BaseController
from transtrack.utils.validators import require_existing_public_id, validate_numeric, validate_period


class PayoutController(BaseController):
    collection_name = "payouts"
    module_name = "payouts"
    id_prefix = "P"
    reference_fields = {
        "owner_id": {"collection": "owners", "label": "Owner ID"},
        "driver_id": {"collection": "drivers", "label": "Driver ID"},
    }

    def calculate_owner_payout(self, owner_id, period, driver_id="", interest_percent=0):
        require_existing_public_id("owners", owner_id, "Owner ID")
        if driver_id:
            require_existing_public_id("drivers", driver_id, "Driver ID")
        validate_period(period)
        interest_percent = validate_numeric(str(interest_percent or 0), "Interest percent")
        vehicles = list(self.db_vehicles().find({"owner_id": owner_id}))
        gross = 0
        expenses = 0
        collections = CollectionController()
        expense_controller = ExpenseController()
        for vehicle in vehicles:
            gross += collections.total_for_vehicle(vehicle["public_id"])
            expenses += expense_controller.total_for_vehicle(vehicle["public_id"])
        deductions = DeductionController().total_for_owner(owner_id)
        interest_amount = gross * (interest_percent / 100)
        total_deductions = expenses + deductions
        net = gross + interest_amount - total_deductions
        return {
            "owner_id": owner_id,
            "driver_id": driver_id,
            "period": period,
            "gross_earnings": gross,
            "interest_percent": interest_percent,
            "interest_amount": interest_amount,
            "total_deductions": total_deductions,
            "net_payout": net,
            "date": datetime.now(),
        }

    def record_payout(self, owner_id, period, driver_id="", interest_percent=0):
        return self.create(self.calculate_owner_payout(owner_id, period, driver_id, interest_percent))

    def db_vehicles(self):
        from transtrack.db.connection import get_db

        return get_db().vehicles
