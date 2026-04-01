import os

import pytest

os.environ.setdefault("CTPC_DISABLE_SCHEDULER", "1")


@pytest.fixture(scope="session", autouse=True)
def database_url():
    url = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://ctpc:ctpc@127.0.0.1:5432/ctpc",
    )
    os.environ["DATABASE_URL"] = url
    return url
