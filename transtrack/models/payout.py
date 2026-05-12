from transtrack.models.base import with_timestamps


def payout_document(owner_id, period, gross_earnings, total_deductions, net_payout, date):
    return with_timestamps(
        {
            "owner_id": str(owner_id),
            "period": period,
            "gross_earnings": float(gross_earnings),
            "total_deductions": float(total_deductions),
            "net_payout": float(net_payout),
            "date": date,
        }
    )
