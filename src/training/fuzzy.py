def fuzzy_decision(prob):

    if prob > 0.8:
        return "High Risk Attack"
    elif prob > 0.4:
        return "Medium Risk"
    else:
        return "Normal Traffic"
