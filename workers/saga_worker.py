from sqlalchemy import text
from database import engine
from services.loan_service import fetch_credit_score, verify_income
from services.risk_service import calculate_risk_for_loan
from services.decision_service import make_decision_for_loan
import time


def run_saga():

    print("Saga worker started")

    with engine.begin() as conn:

        checkpoint = conn.execute(
            text("""
                SELECT last_event_id
                FROM saga_checkpoints
                WHERE saga_name = 'loan_saga'
            """)
        ).fetchone()

        last_checkpoint = checkpoint.last_event_id

        print("Last checkpoint:", last_checkpoint)

        if last_checkpoint is None:

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

            print(
                f"Saga saw {row.event_type}"
            )

            if row.event_type == "LoanApplied":
                loan_id = str(row.aggregate_id)
                print(
                    f"Saga triggering credit score fetch for {loan_id}"
                )

                fetch_credit_score(loan_id)

            elif row.event_type == "CreditScoreFetched":

                loan_id = str(row.aggregate_id)

                print(
                    f"Saga triggering income verification for {loan_id}"
                )

                verify_income(loan_id)

            elif row.event_type == "IncomeVerified":

                loan_id = str(row.aggregate_id)

                print(
                    f"Saga triggering risk calculation for {loan_id}"
                )

                time.sleep(6)

                calculate_risk_for_loan(loan_id)

            elif row.event_type == "RiskCalculated":

                loan_id = str(row.aggregate_id)

                print(
                    f"Saga triggering decision for {loan_id}"
                )

                make_decision_for_loan(loan_id)


        if last_event_id:

            conn.execute(
                text("""
                    UPDATE saga_checkpoints
                    SET last_event_id = :event_id
                    WHERE saga_name = 'loan_saga'
                """),
                {
                    "event_id": last_event_id
                }
            )

        

            print(
                "Saga checkpoint updated:",
                last_event_id
            )


if __name__ == "__main__":

    print("Loan Saga Started")

    while True:

        try:
            run_saga()

        except Exception as e:

            print("Error:", e)

        time.sleep(5)