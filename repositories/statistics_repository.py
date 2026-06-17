from sqlalchemy import text
from database import engine


def increment_total_loans():

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE loan_statistics_projection
                SET total_loans = total_loans + 1
                WHERE id = 1
            """)
        )

       


def increment_approved_loans():

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE loan_statistics_projection
                SET approved_loans = approved_loans + 1
                WHERE id = 1
            """)
        )

  

def increment_rejected_loans():

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE loan_statistics_projection
                SET rejected_loans = rejected_loans + 1
                WHERE id = 1
            """)
        )

        

def get_statistics():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    total_loans,
                    approved_loans,
                    rejected_loans
                FROM loan_statistics_projection
                WHERE id = 1
            """)
        ).mappings().first()

        return dict(result)