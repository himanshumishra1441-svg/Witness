import json
from uuid import uuid4

from repositories.projection_repository import get_risk
from repositories.event_repository import (
    save_event,
    decision_already_exists
)
from repositories.outbox_repository import save_outbox_message

def make_decision(risk):
    if risk == "Low Risk":
        return "Approved"
    elif risk == "Medium Risk":
        return "Needs Review"
    else:
        return "Rejected"


def make_decision_for_loan(loan_id: str):

    row = get_risk(loan_id)

    if not row:
        return

    risk = row.risk

    if risk is None:
        return

    if decision_already_exists(loan_id):
        return

    if risk == "Low Risk":

        save_event(
            str(uuid4()),
            loan_id,
            "LoanApproved",
            json.dumps(
                {
                    "approved_by": "system"
                }
            ),
            str(uuid4())
        )

        save_outbox_message(
            str(uuid4()),
            "LoanApproved",
            loan_id,
            json.dumps(
                {
                    "approved_by": "system"
                }
            )
        )

        return "Approved"

    else:

        save_event(
            str(uuid4()),
            loan_id,
            "LoanRejected",
            json.dumps(
                {
                    "rejected_by": "system"
                }
            ),
            str(uuid4())
        )

        save_outbox_message(
            str(uuid4()),
            "LoanRejected",
            loan_id,
            json.dumps(
                {
                    "rejected_by": "system"
                }
            )
        )

        return "Rejected"