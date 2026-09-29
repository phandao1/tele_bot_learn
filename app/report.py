"""Tổng hợp danh sách chi tiêu thành báo cáo."""
from collections import defaultdict
from collections.abc import Iterable

from app.parser import ParsedExpense


def format_vnd(amount: int) -> str:
    """45000 -> '45.000đ'"""
    return f"{amount:,}".replace(",", ".") + "đ"


def summarize(expenses: Iterable[ParsedExpense]) -> dict:
    """Trả về tổng tiền và tổng theo danh mục (giảm dần)."""
    by_category: dict[str, int] = defaultdict(int)
    total = 0
    for e in expenses:
        by_category[e.category] += e.amount
        total += e.amount
    ordered = dict(sorted(by_category.items(), key=lambda kv: kv[1], reverse=True))
    return {"total": total, "by_category": ordered}


def format_summary(summary: dict) -> str:
    if summary["total"] == 0:
        return "Chưa có khoản chi nào."
    lines = [f"Tổng: {format_vnd(summary['total'])}"]
    lines += [f"- {cat}: {format_vnd(amt)}" for cat, amt in summary["by_category"].items()]
    return "\n".join(lines)
