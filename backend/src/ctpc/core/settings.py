from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CTPC_", extra="ignore")

    database_url: str = "sqlite+pysqlite:///:memory:"
    seed_on_startup: bool = True
