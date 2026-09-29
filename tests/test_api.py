from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_parse_ok():
    r = client.post("/parse", json={"text": "cafe 45k"})
    assert r.status_code == 200
    assert r.json() == {"amount": 45_000, "note": "cafe", "category": "đồ uống"}


def test_parse_invalid():
    r = client.post("/parse", json={"text": "cafe"})
    assert r.status_code == 422
