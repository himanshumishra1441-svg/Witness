from sqlalchemy import text
from database import engine

def save_event(event_id, aggregate_id, event_type, payload, request_id):

    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO events
            (id, aggregate_id, event_type, payload, request_id)
            VALUES
            (:id, :aggregate_id, :event_type, :payload, :request_id)
            """),
            {
                "id": event_id,
                "aggregate_id": aggregate_id,
                "event_type": event_type,
                "payload": payload,
                "request_id": request_id
            }
        )

        conn.execute(
            text("""
                INSERT INTO outbox
                (id, event_type, aggregate_id, payload, processed)
                VALUES
                (:id, :event_type, :aggregate_id, :payload, FALSE)
                """),
                {
                    "id": event_id,
                    "event_type": event_type,
                    "aggregate_id": aggregate_id,
                    "payload": payload
                }

        )    
        

def get_events(loan_id):

    with engine.connect() as conn:

        return conn.execute(
            text("""
                SELECT event_type, payload
                FROM events
                WHERE aggregate_id = :loan_id
                ORDER BY created_at
            """),
            {"loan_id": loan_id}
        ).fetchall()

def get_loan_history(loan_id):

    with engine.connect() as conn:

        return conn.execute(
            text("""
                SELECT
                    event_type,
                    payload,
                    created_at
                FROM events
                WHERE aggregate_id = :loan_id
                ORDER BY created_at
            """),
            {
                "loan_id": loan_id
            }
        ).fetchall()
    
def decision_already_exists(loan_id):

    with engine.connect() as conn:

        row = conn.execute(
            text("""
                 SELECT 1
                 FROM events WHERE aggregate_id = :loan_id
                 and event_type IN('LoanApproved','LoanRejected')
                 LIMIT 1
            """),
            {
                "loan_id": loan_id
            }
        ).fetchone()

        return row is not None
    
def get_event_count(loan_id):

    with engine.connect() as conn:

        count = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM events
                WHERE aggregate_id = :loan_id
            """),
            {
                "loan_id": loan_id
            }
        ).scalar()

        return count
