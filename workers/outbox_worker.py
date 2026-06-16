from sqlalchemy import text
from database import engine
import time

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

            print(
                f"Publishing {row.event_type} "
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

        conn.commit()

if __name__ == "__main__":

    print("Outbox Worker Started")

    while True:

        try:
            run_outbox_worker()

        except Exception as e:
            print("Error:", e)

        time.sleep(5)