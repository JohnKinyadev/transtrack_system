from datetime import datetime

from transtrack.controllers.base_controller import BaseController
from transtrack.utils.numbers import to_float
from transtrack.utils.relations import resolve_document
from transtrack.utils.validators import require_existing_public_id, validate_numeric


class PayoutController(BaseController):
    collection_name = "payouts"
    module_name = "payouts"
    id_prefix = "P"
    reference_fields = {
        "owner_id": {"collection": "owners", "label": "Owner ID"},
    }

    def calculate_owner_payout(self, owner_id, year, dividend_percent):
        if not owner_id:
            raise ValueError("Owner is required.")
        require_existing_public_id("owners", owner_id, "Owner ID")
        owner = resolve_document("owners", owner_id)
        if not owner:
            raise ValueError("Owner does not exist.")
        period_year = str(year or datetime.now().year).strip()
        numeric_year = validate_numeric(period_year, "Year", allow_zero=False)
        if numeric_year != int(numeric_year):
            raise ValueError("Year must be a whole number.")
        dividend_percent = validate_numeric(str(dividend_percent or 0), "Dividend percent")
        shares = to_float(owner.get("shares"))
        annual_dividend = dividend_percent * shares
        return {
            "owner_id": owner_id,
            "period": str(int(numeric_year)),
            "period_year": str(int(numeric_year)),
            "shares": shares,
            "dividend_percent": dividend_percent,
            "annual_dividend": annual_dividend,
            "gross_earnings": annual_dividend,
            "total_deductions": 0,
            "net_payout": annual_dividend,
            "date": datetime.now(),
        }

    def record_payout(self, owner_id, year, dividend_percent):
        return self.create(self.calculate_owner_payout(owner_id, year, dividend_percent))
