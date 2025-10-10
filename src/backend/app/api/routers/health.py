from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    try:
        # Test database connection
        db.execute("SELECT 1")
        database_status = "connected"
    except Exception:
        database_status = "disconnected"

    return {
        "status": "ok",
        "message": "PostProber API is healthy!",
        "database": database_status,
        "version": "1.0.0"
    }