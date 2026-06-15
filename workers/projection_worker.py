

from sqlalchemy import text
from database import engine
from repositories.projection_repository import (create_loan_projection, update_credit_score, 
                                                update_monthly_income, update_status, update_risk)
from repositories.dashboard_repository import increment_approved, increment_rejected, increment_high_risk, increment_low_risk
from repositories.statistics_repository import (increment_total_loans, increment_approved_loans, increment_rejected_loans)
import time


def run_projection_worker():

    print("Projection worker started")

    with engine.connect() as conn:

        checkpoint = conn.execute(
            text("""
                SELECT last_event_id
                FROM projection_checkpoints
                WHERE projection_name = 'loan_projection'
            """)
        ).fetchone()

        last_checkpoint = checkpoint.last_event_id

        print("Last checkpoint:", last_checkpoint)

        
        if last_checkpoint is None:

            print("No checkpoint found. Rebuilding from beginning...")

            rows = conn.execute(
                text("""
                    SELECT
                        id,
                        aggregate_id,
                        event_type,
                        payload
                    FROM events
                    ORDER BY created_at
                """)
            ).fetchall()

        
        else:

            checkpoint_row = conn.execute(
                text("""
                    SELECT created_at
                    FROM events
                    WHERE id = :event_id
                """),
                {
                    "event_id": last_checkpoint
                }
            ).fetchone()

            print("Checkpoint time:", checkpoint_row.created_at)

            rows = conn.execute(
                text("""
                    SELECT
                        id,
                        aggregate_id,
                        event_type,
                        payload
                    FROM events
                    WHERE created_at > :checkpoint_time
                    ORDER BY created_at
                """),
                {
                    "checkpoint_time": checkpoint_row.created_at
                }
            ).fetchall()

        print("Events found:", len(rows))

        last_event_id = None

        for row in rows:

            last_event_id = row.id
            loan_id = str(row.aggregate_id)
            event_type = row.event_type
            payload = row.payload

            print(f"Processing {event_type} for loan {loan_id}")


            if event_type == "LoanApplied":

                create_loan_projection(
                    loan_id,
                    "Applied"
                )

                increment_total_loans()


            elif event_type == "CreditScoreFetched":

                update_credit_score(
                    loan_id,
                    payload["credit_score"]
                )


            elif event_type == "IncomeVerified":

                update_monthly_income(
                    loan_id,
                    payload["monthly_income"]
                )


            elif event_type == "RiskCalculated":

                risk = payload["risk"]

                update_risk(
                    loan_id,
                    payload["risk"]

                )

                if risk == "low":
                    increment_low_risk()
                else:
                    increment_high_risk()


            elif event_type == "LoanApproved":

                update_status(
                    loan_id,
                    "Approved"
                )

                increment_approved()

                increment_approved_loans()


            elif event_type == "LoanRejected":

                update_status(
                    loan_id,
                    "Rejected"
                )

                increment_rejected()

                increment_rejected_loans()

            print(event_type)

        if last_event_id:

            conn.execute(
                text("""
                    UPDATE projection_checkpoints
                    SET last_event_id = :event_id
                    WHERE projection_name = 'loan_projection'
                """),
                {
                    "event_id": last_event_id
                }
            )

            conn.commit()

            print("Checkpoint updated:", last_event_id)


if __name__ == "__main__":

    print("Continuous Projection Worker Started")

    while True:

        try:
            run_projection_worker()

        except Exception as e:
            print("Error occurred:", e)

        time.sleep(5)
            