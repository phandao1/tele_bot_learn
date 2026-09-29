from app.parser import ParsedExpense
from app.report import format_summary, format_vnd, summarize


def make(amount, category):
    return ParsedExpense(amount=amount, note="", category=category)


def test_format_vnd():
    assert format_vnd(45_000) == "45.000đ"
    assert format_vnd(1_500_000) == "1.500.000đ"


def test_summarize_total_and_order():
    s = summarize([make(45_000, "đồ uống"), make(90_000, "ăn uống"), make(30_000, "đồ uống")])
    assert s["total"] == 165_000
    assert list(s["by_category"].items()) == [("ăn uống", 90_000), ("đồ uống", 75_000)]


def test_summarize_empty():
    assert summarize([])["total"] == 0
    assert format_summary(summarize([])) == "Chưa có khoản chi nào."
