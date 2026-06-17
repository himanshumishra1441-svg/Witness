from sqlalchemy import text
from database import engine
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def run_outbox_worker():
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT
                    id,
                    event_type,
                    aggregate_id,
                    payload
                FROM outbox
                WHERE processed = FALSE
                ORDER BY created_at
            """)
        ).fetchall()

        for row in rows:

            producer.send(
                "loan-events",
                {
                    "event_type": row.event_type,
                    "loan_id": str(row.aggregate_id),
                    "payload": row.payload
                }
            )


            print(
                f"Published {row.event_type} "
                f"for loan {row.aggregate_id}"
            )

            conn.execute(
                text("""
                    UPDATE outbox
                    SET processed = TRUE
                    WHERE id = :id
                """),
                {
                    "id": row.id
                }
            )

        producer.flush()

        conn.commit()

if __name__ == "__main__":

    print("Outbox Worker Started")

    while True:

        try:
            run_outbox_worker()

        except Exception as e:
            print("Error:", e)

        time.sleep(5)