def fuzzy_decision(prob: float) -> str:
    """
    Convert ANN probability → risk level
    """

    if prob < 0.30:
        return "LOW"

    elif prob < 0.60:
        return "MEDIUM"

    elif prob < 0.85:
        return "HIGH"

    else:
        return "CRITICAL"
