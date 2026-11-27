from fastapi import FastAPI
from backend.app.api.routes.health import router as health_router

app = FastAPI(title="JobHunt AI", description="Personal AI-assisted job discovery and application management.", version="0.1.0")
app.include_router(health_router, prefix="/api")

@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"name": "JobHunt AI", "status": "running", "version": "0.1.0"}
