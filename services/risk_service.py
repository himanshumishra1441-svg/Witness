import json
from uuid import uuid4

from repositories.event_repository import save_event
from repositories.projection_repository import get_credit_score_and_income


def calculate_risk(score, income):

    if score >= 700 and income >= 50000:
        return "Low Risk"

    elif score >= 600 and income >= 30000:
        return "Medium Risk"

    else:
        return "High Risk"


def calculate_risk_for_loan(loan_id: str):

    print("Starting risk calculation")

    row = get_credit_score_and_income(loan_id)

    print("Row:", row)

    if not row:
        print("No row found")
        return

    score = row.credit_score
    income = row.monthly_income

    if score is None or income is None:

        print("Score or income is missing")
        return

    risk = calculate_risk(
        score,
        income
    )

    save_event(
        str(uuid4()),
        loan_id,
        "RiskCalculated",
        json.dumps(
            {
                "risk": risk
            }
        ),
        str(uuid4())
    )

    print("RiskCalculated event saved")

    return risk