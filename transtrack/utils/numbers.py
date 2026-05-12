def to_float(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0
