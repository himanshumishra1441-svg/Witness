import json
from sqlalchemy import text
from database import engine

def create_snapshot(loan_id: str):

    with engine.connect() as conn:

        row = conn.execute(
            text("""
                SELECT
                    loan_id,
                    status,
                    credit_score,
                    monthly_income,
                    risk
                FROM loan_projection
                WHERE loan_id = :loan_id
            """),
            {"loan_id": loan_id}
        ).fetchone()

        event_count = conn.execute(
            text("""
                 SELECT COUNT(*)
                 FROM events
                 WHERE aggregate_id = :loan_id
            """),
            {"loan_id": loan_id}
        ).scalar()

        snapshot_state = {
            "status": row.status,
            "credit_score": row.credit_score,
            "monthly_income": row.monthly_income,
            "risk": row.risk
        }

        conn.execute(
             text("""
                 INSERT INTO snapshots
                 (
                     aggregate_id,
                     state,
                     last_event_time,
                     event_count
                 )
                VALUES
                 (
                     :aggregate_id,
                     :state,
                     NOW(),
                     :event_count
                )
                 ON CONFLICT (aggregate_id)
                 DO UPDATE
                 SET
                     state = EXCLUDED.state,
                     last_event_time = NOW(),
                     event_count = EXCLUDED.event_count
          """),
         {
             "aggregate_id": loan_id,
             "state": json.dumps(snapshot_state),
             "event_count": event_count
         }
    )

        conn.commit()

    return {
        "loan_id": loan_id,
        "snapshot": snapshot_state
    }


def replay_from_snapshot(loan_id: str):

    with engine.connect() as conn:
        snapshot = conn.execute(
            text("""
                SELECT state, event_count
                FROM snapshots
                WHERE aggregate_id = :loan_id
            """),
            {"loan_id": loan_id}

        ).fetchone()
        if not snapshot:
            return {"error": "Snapshot not found"}
        
        state = snapshot.state
        event_count = snapshot.event_count

        rows = conn.execute(
            text("""
                SELECT event_type, payload
                FROM events
                WHERE aggregate_id = :loan_id
                ORDER BY created_at
                OFFSET :offset
            """),
            {
                "loan_id": loan_id,
                "offset": event_count
            }
        ).fetchall()

        for row in rows:

            event_type = row.event_type
            payload = row.payload

            if event_type == "CreditScoreFetched":
                state["credit_score"] = payload["credit_score"]

            elif event_type == "IncomeVerified":
                state["monthly_income"] = payload["monthly_income"]

            elif event_type == "RiskCalculated":
                state["risk"] = payload["risk"]

            elif event_type == "LoanApproved":
                state["status"] = "APPROVED"

            elif event_type == "LoanRejected":
                state["status"] = "REJECTED"
                

    return {
        "loan_id": loan_id, 
        "state": state,
        "replayed_events": len(rows),
        "snapshot_event_count": event_count
    }