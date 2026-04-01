"""Secured maintenance endpoints (cron / GitHub Actions)."""

from fastapi import APIRouter, Depends, Header, HTTPException

from sqlalchemy.orm import Session

from ctpc.config import get_settings
from ctpc.db import get_db
from ctpc.ingest.pipeline import run_full_ingest

router = APIRouter(prefix="/internal", tags=["internal"])


@router.post("/jobs/ingest")
def trigger_ingest(
    authorization: str | None = Header(None),
    db: Session = Depends(get_db),
) -> dict:
    settings = get_settings()
    if settings.internal_job_token:
        expected = f"Bearer {settings.internal_job_token}"
        if authorization != expected:
            raise HTTPException(status_code=401, detail="Unauthorized")
    run_full_ingest(db)
    return {"status": "ok"}
