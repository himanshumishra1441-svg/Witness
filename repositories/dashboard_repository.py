from sqlalchemy import text
from database import engine

def get_dashboard():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT
                    low_risk_count,
                    high_risk_count,
                    approved_count,
                    rejected_count
                FROM risk_dashboard_projection
                WHERE id = 1
            """)
        ).mappings().first()

        return dict(result)
    
def increment_approved():

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE risk_dashboard_projection
                SET approved_count = approved_count + 1
                WHERE id = 1
            """)
        )

        

def increment_rejected():
    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE risk_dashboard_projection
                SET rejected_count = rejected_count + 1
                WHERE id = 1
            """)
        )

def increment_low_risk():

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE risk_dashboard_projection
                SET low_risk_count = low_risk_count + 1
                WHERE id = 1
            """)
        )

    

def increment_high_risk():

    with engine.begin() as conn:

        conn.execute(
                text("""
                    UPDATE risk_dashboard_projection
                    SET high_risk_count = high_risk_count + 1
                    WHERE id = 1
                """)
            )
        
    