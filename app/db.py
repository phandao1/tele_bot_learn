"""Lớp truy cập PostgreSQL (SQL thuần, dùng psycopg 3)."""
import os

import psycopg
from psycopg.rows import dict_row

from app.parser import ParsedExpense

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id         BIGSERIAL PRIMARY KEY,
    amount     BIGINT NOT NULL CHECK (amount > 0),
    note       TEXT NOT NULL,
    category   TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_expenses_created_at ON expenses (created_at);
"""

COLUMNS = "id, amount, note, category, created_at"


def connect() -> psycopg.Connection:
    # Đọc biến môi trường ở thời điểm gọi (không phải lúc import)
    # để test có thể trỏ sang database khác.
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)


def init_db() -> None:
    with connect() as conn:
        conn.execute(SCHEMA)


def add_expense(e: ParsedExpense) -> dict:
    with connect() as conn:
        return conn.execute(
            f"INSERT INTO expenses (amount, note, category) VALUES (%s, %s, %s) "
            f"RETURNING {COLUMNS}",
            (e.amount, e.note, e.category),
        ).fetchone()


def list_expenses(days: int) -> list[dict]:
    with connect() as conn:
        return conn.execute(
            f"SELECT {COLUMNS} FROM expenses "
            f"WHERE created_at >= now() - make_interval(days => %s::int) "
            f"ORDER BY created_at DESC, id DESC",
            (days,),
        ).fetchall()
