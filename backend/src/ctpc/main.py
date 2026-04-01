"""FastAPI entrypoint."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ctpc.config import get_settings
from ctpc.db import get_session_factory
from ctpc.ingest.pipeline import run_full_ingest
from ctpc.routers import api_v1
from ctpc.routers.internal import router as internal_router

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

scheduler: BackgroundScheduler | None = None


def _scheduled_ingest() -> None:
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        log.info("Scheduled ingest starting")
        run_full_ingest(db)
        log.info("Scheduled ingest finished")
    except Exception:
        log.exception("Scheduled ingest failed")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global scheduler
    settings = get_settings()
    if settings.ingest_on_startup:
        try:
            SessionLocal = get_session_factory()
            db = SessionLocal()
            try:
                run_full_ingest(db)
            finally:
                db.close()
        except Exception:
            log.exception("Startup ingest failed (DB may be empty until migrate + network)")

    if not os.environ.get("CTPC_DISABLE_SCHEDULER"):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            _scheduled_ingest,
            IntervalTrigger(hours=6),
            id="ctpc_ingest",
            replace_existing=True,
        )
        scheduler.start()
        log.info("Background scheduler started (6h ingest interval)")
    yield
    if scheduler:
        scheduler.shutdown(wait=False)


app = FastAPI(title="CTPC API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1.router)
app.include_router(internal_router)


@app.get("/healthz")
def healthz() -> dict:
    return {"service": "ctpc-backend"}
