from sqlalchemy import create_engine, text
from uuid import uuid4

DATABASE_URL = "postgresql://postgres:Witness%40123@localhost:5432/Witness"

engine = create_engine(DATABASE_URL)

event_id = str(uuid4())
loan_id = str(uuid4())

with engine.begin() as conn:
    conn.execute(
        text("""
        INSERT INTO events
        (id, aggregate_id, event_type, payload)
        VALUES
        (:id, :aggregate_id, :event_type, :payload)
        """),
        {
            "id": event_id,
            "aggregate_id": loan_id,
            "event_type": "LoanApplied",
            "payload": '{"amount":100000}'
        }
    )
    

print("Event Inserted!")