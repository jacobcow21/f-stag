from fastapi import APIRouter
from app.db.database import get_db

router = APIRouter()


@router.get("/health")
async def health_check():
    try:
        db = get_db()
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "ok",
        "database": db_status,
    }
