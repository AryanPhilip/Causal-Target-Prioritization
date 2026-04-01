from __future__ import annotations

from ctpc.api.app import create_app
from ctpc.core.settings import Settings
from ctpc.db.session import DatabaseManager


def build_app():
    settings = Settings()
    manager = DatabaseManager.from_url(settings.database_url)
    return create_app(manager=manager, seed_demo_data=settings.seed_on_startup)


app = build_app()
