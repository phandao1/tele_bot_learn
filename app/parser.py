"""Parse câu nhắn kiểu "cafe 45k" thành khoản chi tiêu có cấu trúc."""
import re
from dataclasses import dataclass
from decimal import Decimal


class ParseError(ValueError):
    """Câu nhắn không hiểu được."""


@dataclass(frozen=True)
class ParsedExpense:
    amount: int      # đơn vị: đồng
    note: str
    category: str


# số + đơn vị tuỳ chọn: 45k, 45000, 45.000, 1.5tr, 1,5tr
AMOUNT_RE = re.compile(r"^(\d+(?:[.,]\d+)*)(k|tr|m)?$", re.IGNORECASE)
MULTIPLIER = {"k": 1_000, "tr": 1_000_000, "m": 1_000_000}

CATEGORIES = {
    "đồ uống": ["cafe", "cà phê", "ca phe", "trà sữa", "tra sua", "trà", "bia"],
    "ăn uống": ["ăn", "an", "cơm", "com", "phở", "pho", "bún", "bun", "ăn trưa", "an trua"],
    "di chuyển": ["grab", "xăng", "xang", "taxi", "xe bus", "gửi xe", "gui xe"],
    "nhà cửa": ["tiền nhà", "tien nha", "điện", "dien", "nước", "nuoc", "internet"],
    "mua sắm": ["shopee", "lazada", "mua"],
}
DEFAULT_CATEGORY = "khác"


def parse_amount(token: str) -> int:
    """'45k' -> 45000, '1.5tr' -> 1500000, '45.000' -> 45000."""
    match = AMOUNT_RE.match(token)
    if not match:
        raise ParseError(f"Không phải số tiền: {token!r}")
    number, unit = match.groups()
    if unit:
        # có đơn vị: dấu . hoặc , là dấu thập phân
        value = Decimal(number.replace(",", ".")) * MULTIPLIER[unit.lower()]
    else:
        # không đơn vị: dấu . hoặc , là dấu ngăn cách hàng nghìn
        value = Decimal(re.sub(r"[.,]", "", number))
    return int(value)


def detect_category(note: str) -> str:
    padded = f" {note.lower()} "
    for category, keywords in CATEGORIES.items():
        if any(f" {kw} " in padded for kw in keywords):
            return category
    return DEFAULT_CATEGORY


def parse_expense(text: str) -> ParsedExpense:
    tokens = text.strip().split()
    if not tokens:
        raise ParseError("Câu nhắn trống")

    # số tiền nằm cuối ("cafe 45k") hoặc đầu ("45k cafe")
    if AMOUNT_RE.match(tokens[-1]):
        amount_token, rest = tokens[-1], tokens[:-1]
    elif AMOUNT_RE.match(tokens[0]):
        amount_token, rest = tokens[0], tokens[1:]
    else:
        raise ParseError("Không tìm thấy số tiền")

    amount = parse_amount(amount_token)
    if amount <= 0:
        raise ParseError("Số tiền phải lớn hơn 0")

    note = " ".join(rest)
    return ParsedExpense(amount=amount, note=note, category=detect_category(note))
