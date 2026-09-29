import psycopg
import pytest

from app import db
from app.parser import ParsedExpense


def make(amount=45_000, note="cafe", category="đồ uống"):
    return ParsedExpense(amount=amount, note=note, category=category)


def test_add_and_list(database):
    saved = db.add_expense(make())
    assert saved["id"] == 1
    assert saved["amount"] == 45_000

    rows = db.list_expenses(days=7)
    assert len(rows) == 1
    assert rows[0]["note"] == "cafe"


def test_list_newest_first(database):
    db.add_expense(make(note="a"))
    db.add_expense(make(note="b"))
    assert [r["note"] for r in db.list_expenses(days=7)] == ["b", "a"]


def test_list_excludes_old_rows(database):
    db.add_expense(make(note="mới"))
    with db.connect() as conn:
        conn.execute(
            "INSERT INTO expenses (amount, note, category, created_at) "
            "VALUES (10000, 'cũ', 'khác', now() - interval '30 days')"
        )
    notes = [r["note"] for r in db.list_expenses(days=7)]
    assert notes == ["mới"]


def test_database_rejects_non_positive_amount(database):
    with pytest.raises(psycopg.errors.CheckViolation):
        db.add_expense(make(amount=0))
