def calculate_risk(score, income):
    if score >= 700 and income >= 50000:
        return "Low Risk"
    elif score >= 600 and income >= 30000:
        return "Medium Risk"
    else:
        return "High Risk"