from sqlalchemy import text
from database import engine


def rebuild_projections():

    with engine.begin() as conn:

        
        conn.execute(
            text("DELETE FROM loan_projection")
        )

    

        rows = conn.execute(
            text("""
                SELECT
                    aggregate_id,
                    event_type,
                    payload
                FROM events
                ORDER BY created_at
            """)
        ).fetchall()

        loan = {}

        for row in rows:

            loan_id = str(row.aggregate_id)
            event_type = row.event_type
            payload = row.payload

            if loan_id not in loan:

                loan[loan_id] = {
                    "status": "APPLIED",
                    "credit_score": None,
                    "monthly_income": None,
                    "risk": None
                }

            if event_type == "CreditScoreFetched":
                loan[loan_id]["credit_score"] = payload["credit_score"]

            elif event_type == "IncomeVerified":
                loan[loan_id]["monthly_income"] = payload["monthly_income"]

            elif event_type == "RiskCalculated":
                loan[loan_id]["risk"] = payload["risk"]

            elif event_type == "LoanApproved":
                loan[loan_id]["status"] = "APPROVED"

            elif event_type == "LoanRejected":
                loan[loan_id]["status"] = "REJECTED"

        for loan_id, state in loan.items():

            conn.execute(
                text("""
                    INSERT INTO loan_projection
                    (
                        loan_id,
                        status,
                        credit_score,
                        monthly_income,
                        risk
                    )
                    VALUES
                    (
                        :loan_id,
                        :status,
                        :credit_score,
                        :monthly_income,
                        :risk
                    )
                """),
                {
                    "loan_id": loan_id,
                    "status": state["status"],
                    "credit_score": state["credit_score"],
                    "monthly_income": state["monthly_income"],
                    "risk": state["risk"]
                }
            )

        

    return {
        "message": "Projections rebuilt successfully"
    }   

