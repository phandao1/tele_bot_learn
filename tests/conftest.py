import os

import pytest

from app import db


@pytest.fixture
def database(monkeypatch):
    """Database thật cho integration test.

    An toàn: dùng TEST_DATABASE_URL (KHÔNG phải DATABASE_URL), vì fixture này
    xoá sạch bảng expenses trước mỗi test.
    """
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        if os.getenv("CI"):
            # Trên CI mà thiếu DB thì phải ĐỎ, không được lặng lẽ bỏ qua
            pytest.fail("TEST_DATABASE_URL chưa được set trên CI")
        pytest.skip("Không có TEST_DATABASE_URL, bỏ qua test cần database")
    monkeypatch.setenv("DATABASE_URL", url)
    db.init_db()
    with db.connect() as conn:
        conn.execute("TRUNCATE expenses RESTART IDENTITY")
    yield
