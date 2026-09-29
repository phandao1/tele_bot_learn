from fastapi.testclient import TestClient

from app.main import app


def test_create_then_list_then_summary(database):
    # `with` để FastAPI chạy lifespan (init_db)
    with TestClient(app) as client:
        assert client.post("/expenses", json={"text": "cafe 45k"}).status_code == 201
        assert client.post("/expenses", json={"text": "ăn trưa 90k"}).status_code == 201

        rows = client.get("/expenses").json()
        assert len(rows) == 2

        s = client.get("/summary").json()
        assert s["total"] == 135_000
        assert list(s["by_category"]) == ["ăn uống", "đồ uống"]


def test_create_invalid_text_returns_422_and_saves_nothing(database):
    with TestClient(app) as client:
        assert client.post("/expenses", json={"text": "cafe"}).status_code == 422
        assert client.get("/expenses").json() == []


def test_days_validation(database):
    with TestClient(app) as client:
        assert client.get("/expenses?days=0").status_code == 422
