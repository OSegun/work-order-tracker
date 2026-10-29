from typing import Annotated, TypeAlias

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import SessionLocal

router = APIRouter(prefix="/health", tags=["health"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency: TypeAlias = Annotated[Session, Depends(get_db)]


@router.get("/live", status_code=status.HTTP_200_OK)
def live() -> dict[str, str]:
    """Confirm the process is responding. Never touches the database."""
    return {"status": "alive"}


@router.get("/ready", status_code=status.HTTP_200_OK)
def ready(db: db_dependency) -> dict[str, str]:
    """Confirm the process is responding and the database answers."""
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from None
    return {"status": "ready"}
