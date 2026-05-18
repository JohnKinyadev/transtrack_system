from transtrack.models.base import with_timestamps
from transtrack.utils.numbers import to_float


def payout_document(owner_id, period, gross_earnings, total_deductions, net_payout, date):
    return with_timestamps(
        {
            "owner_id": str(owner_id),
            "period": period,
            "gross_earnings": to_float(gross_earnings),
            "total_deductions": to_float(total_deductions),
            "net_payout": to_float(net_payout),
            "date": date,
        }
    )
