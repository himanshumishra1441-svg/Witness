import json
import random
from uuid import uuid4
from sqlalchemy import text
from database import engine
from models import LoanRequest
from repositories.event_repository import save_event

def create_loan(request: LoanRequest):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT aggregate_id
                FROM events
                WHERE request_id = :request_id
                LIMIT 1
            """),
            {"request_id": request.request_id}
        ).fetchone()

        if result:
            return {
                "loan_id": result[0],
                "status": "already_processed"
            }
        
        loan_id = str(uuid4())
        event_id = str(uuid4())
        save_event(
            event_id,
            loan_id,
            "LoanApplied",
            '{"amount":100000}',
            request.request_id
        )

        conn.execute(
            text("""
                 INSERT INTO loan_projection
                 (loan_id, status)
                 VALUES
                 (:loan_id, :status)
            """),
            {
                  "loan_id": loan_id,
                  "status": "APPLIED"
            }
        )

        conn.commit()
    
    return {
        "loan_id": loan_id,
        "status": "created"
    }

def verify_income(loan_id: str):

    monthly_income = random.randint(10000, 150000)

    with engine.connect() as conn:

        event_id = str(uuid4())

        save_event(
             event_id,
             loan_id,
             "IncomeVerified",
             json.dumps({"monthly_income": monthly_income}),
             str(uuid4())
       )


    return {
        "loan_id": loan_id,
        "event": "IncomeVerified",
        "monthly_income": monthly_income
    }

def fetch_credit_score(loan_id: str):

    event_id = str(uuid4())

    credit_score = random.randint(300, 850)

    with engine.connect()as conn:
        
        save_event(
            event_id,
            loan_id,
            "CreditScoreFetched",
            json.dumps({"credit_score": credit_score}),
            str(uuid4())

        )


    return {
        "loan_id": loan_id,
        "event": "CreditScoreFetched",
        "credit_score": credit_score
    }