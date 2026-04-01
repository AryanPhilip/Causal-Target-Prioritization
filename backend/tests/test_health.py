from fastapi.testclient import TestClient

from ctpc.main import app


def test_healthz():
    c = TestClient(app)
    r = c.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"service": "ctpc-backend"}
