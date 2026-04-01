import httpx

from ctpc.config import get_settings


def client() -> httpx.Client:
    s = get_settings()
    return httpx.Client(
        timeout=s.http_timeout_seconds,
        headers={"User-Agent": "ctpc-backend/0.1 (research; contact: https://github.com)"},
    )
