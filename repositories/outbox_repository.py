from sqlalchemy import text
from database import engine

def save_outbox_message(message_id, event_type, aggregate_id, payload):
    with engine.connect() as conn:

        conn.execute(
            text("""
                INSERT INTO outbox
                (
                    id,
                    event_type,
                    aggregate_id,
                    payload
                )
                VALUES
                (
                    :id,
                    :event_type,
                    :aggregate_id,
                    :payload
                )
            """),
            {
                "id": message_id,
                "event_type": event_type,
                "aggregate_id": aggregate_id,
                "payload": payload
            }
        )

        conn.commit()

        
