from sqlalchemy import text
from database import engine

def get_projection(loan_id):

    with engine.connect() as conn:

        return conn.execute(
            text("""
                SELECT
                    loan_id,
                    status,
                    credit_score,
                    risk
                FROM loan_projection
                WHERE loan_id = :loan_id
            """),
            {"loan_id": loan_id}
        ).fetchone()


def update_credit_score(loan_id, credit_score):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE loan_projection
                SET credit_score = :credit_score
                WHERE loan_id = :loan_id
            """),
            {
                "loan_id": loan_id,
                "credit_score": credit_score
            }
        )

    

def update_monthly_income(loan_id, monthly_income):
    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE loan_projection
                SET monthly_income = :income
                WHERE loan_id = :loan_id
            """),
            {
                "income": monthly_income,
                "loan_id": loan_id
            }
        )

    

def update_status(loan_id, status):
    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE loan_projection
                SET status = :status
                WHERE loan_id = :loan_id
            """),
            {
                "status": status,
                "loan_id": loan_id
            }
        )
    

def update_risk(loan_id, risk):
    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE loan_projection
                SET risk = :risk
                WHERE loan_id = :loan_id
            """),
            {
                "risk": risk,
                "loan_id": loan_id
            }
        )
    

def get_risk(loan_id):

    with engine.connect() as conn:

        return conn.execute(
            text("""
                SELECT risk
                FROM loan_projection
                WHERE loan_id = :loan_id
            """),
            {"loan_id": loan_id}
        ).fetchone()
    

def get_credit_score_and_income(loan_id):

    with engine.connect() as conn:

        return conn.execute(
            text("""
                SELECT credit_score, monthly_income
                FROM loan_projection
                WHERE loan_id = :loan_id
            """),
            {"loan_id": loan_id}
        ).fetchone()

def create_loan_projection(loan_id, status):

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO loan_projection
                (
                    loan_id,
                    status
                )
                VALUES
                (
                    :loan_id,
                    :status
                )
                ON CONFLICT (loan_id)
                DO NOTHING
            """),
            {
                "loan_id": loan_id,
                "status": status
            }
        )

        

