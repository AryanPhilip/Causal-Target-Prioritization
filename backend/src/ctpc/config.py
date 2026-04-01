from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg://ctpc:ctpc@127.0.0.1:5432/ctpc"
    ctpc_profile_default: str = "balanced"
    ingest_schedule_cron: str = "0 */6 * * *"  # every 6 hours
    ingest_on_startup: bool = False
    opentargets_api_url: str = "https://api.platform.opentargets.org/api/v4"
    chembl_api_url: str = "https://www.ebi.ac.uk/chembl/api/data"
    clinicaltrials_api_url: str = "https://clinicaltrials.gov/api/v2/studies"
    http_timeout_seconds: float = 60.0
    internal_job_token: str = ""  # optional Bearer for POST /internal/jobs/ingest


@lru_cache
def get_settings() -> Settings:
    return Settings()
