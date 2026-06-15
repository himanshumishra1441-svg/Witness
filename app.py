import json
from uuid import uuid4
from sqlalchemy import create_engine, text
from database import engine
from models import LoanRequest
import random
from services.risk_service import calculate_risk as calculate_risk_service
from services.decision_service import make_decision as make_decision_service
from services.snapshot_service import(create_snapshot as create_snapshot_service,
                                       replay_from_snapshot as replay_from_snapshot_service)
from services.loan_service import (create_loan as create_loan_service,
                                   verify_income as verify_income_service, 
                                   fetch_credit_score as fetch_credit_score_service)
from repositories.projection_repository import (get_credit_score_and_income, get_risk, get_projection)
from repositories.event_repository import save_event, get_events, decision_already_exists
from projections.rebuild_projections import rebuild_projections
from fastapi import FastAPI
from services.event_service import get_loan_history_service
from services.dashboard_service import dashboard_summary
from repositories.statistics_repository import get_statistics
app = FastAPI()

event_store = []

@app.get("/")
def home():
    return {"message": "WITNESS is running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/version")
def version():
    return {"version": "0.1"}

@app.get("/events")
def get_events():
    
        rows = get_events()

        events = []

        for row in rows:
            events.append(
                {
                    "id": str(row[0]),
                    "aggregate_id": str(row[1]),
                    "event_type": row[2],
                    "payload": row[3],
                    "request_id": row[4],
                    "created_at": str(row[5])
                }
            )

        return {"events": events}

@app.post("/loans")
def create_loan(request: LoanRequest):

    return create_loan_service(request)

@app.get("/loans/{loan_id}/income")
def verify_income(loan_id: str):

    return verify_income_service(loan_id)

@app.get("/loans/{loan_id}/credit-score")
def fetch_credit_score(loan_id: str):

    return fetch_credit_score_service(loan_id)

@app.get("/loans/{loan_id}/decision")
def make_decision_route(loan_id: str):

        row = get_risk(loan_id)

        if not row:
            return {"error": "Loan not found"}

        risk = row.risk

        if risk is None:
            return {
                "error": "Risk must be calculated first"
            }
        
        if decision_already_exists(loan_id):
            return{
                "error": "Decision already made"
            }

        decision = make_decision_service(risk)

        if decision == "Approved":

            save_event(
                str(uuid4()),
                loan_id,
                "LoanApproved",
                json.dumps({"approved_by": "system"}),
                str(uuid4())
            )

        else:

            save_event(
                str(uuid4()),
                loan_id,
                "LoanRejected",
                json.dumps({"rejected_by": "system"}),
                str(uuid4())
            )


        return {
        "loan_id": loan_id,
        "decision": decision
    }

@app.get("/loans/{loan_id}/risk")
def calculate_risk_route(loan_id: str):

    event_id = str(uuid4())

    row = get_credit_score_and_income(loan_id)

    if not row:
        return {"error": "Loan not found"}

    score = row.credit_score
    income = row.monthly_income

    if score is None or income is None:
        return {
            "error": "Credit score and income must be verified first"
        }

    risk = calculate_risk_service(score, income)

    save_event(
        event_id,
        loan_id,
        "RiskCalculated",
        json.dumps({"risk": risk}),
        str(uuid4())
    )


    return {
        "loan_id": loan_id,
        "event": "RiskCalculated",
        "credit_score": score,
        "monthly_income": income,
        "risk": risk
    }


@app.get("/loans/{loan_id}")
def get_loan(loan_id: str):

    with engine.connect() as conn:

        row = get_projection(loan_id)

        if not row:
            return {"error": "Loan not found"}

        return {
            "loan_id": str(row.loan_id),
            "status": row.status,
            "credit_score": row.credit_score,
            "risk": row.risk
        }

@app.post("/loans/{loan_id}/approve")
def approve_loan(loan_id: str):

    event_id = str(uuid4())

    with engine.connect() as conn:

        save_event(
             event_id,
             loan_id,
             "LoanApproved",
             '{"approved_by":"system"}',
             str(uuid4())
        )

    return {
        "loan_id": loan_id,
        "event": "LoanApproved"
    }


@app.post("/rebuild-projections")
def rebuild_projections_route():

    return rebuild_projections()

@app.get("/Loans/{Loan_id}/snapshot")
def create_snapshot_route(loan_id: str):

    return create_snapshot_service(loan_id)

@app.get("/loans/{loan_id}/replay-from-snapshot")
def replay_from_snapshot_route(loan_id: str):

    return replay_from_snapshot_service(loan_id)

@app.get("/loans/{loan_id}/history")
def get_loan_history_route(loan_id: str):

    return get_loan_history_service(loan_id)

@app.get("/dashboard")
def get_dashboard():

    return dashboard_summary()

@app.get("/statistics")
def statistics():

    return get_statistics()