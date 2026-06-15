def make_decision(risk):
    if risk == "Low Risk":
        return "Approved"
    elif risk == "Medium Risk":
        return "Needs Review"
    else:
        return "Rejected"