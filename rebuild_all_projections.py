from sqlalchemy import text
from database import engine

def rebuild():

    with engine.connect() as conn:

        print("Clearing loan projection...")

        conn.execute(
            text("""
                DELETE FROM loan_projection
            """)
        )

        print("Resetting dashboard...")

        conn.execute(
            text("""
                UPDATE risk_dashboard_projection
                SET
                    low_risk_count = 0,
                    high_risk_count = 0,
                    approved_count = 0,
                    rejected_count = 0
                WHERE id = 1
            """)
        )

        conn.execute(
            text("""
                UPDATE projection_checkpoints
                SET last_event_id = NULL
                WHERE projection_name = 'loan_projection'
            """)
        )

        conn.commit()

        print("Done")


if __name__ == "__main__":
    rebuild()