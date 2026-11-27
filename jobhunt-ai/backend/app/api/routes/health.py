from fastapi import APIRouter
from sqlalchemy import text
from backend.app.database.session import engine

router = APIRouter(tags=["health"])

@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/health/database")
def database_health() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception:
        return {"database": "unavailable"}
