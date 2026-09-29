import pytest

from app.parser import ParseError, parse_amount, parse_expense


@pytest.mark.parametrize(
    "token, expected",
    [
        ("45k", 45_000),
        ("45K", 45_000),
        ("45000", 45_000),
        ("45.000", 45_000),   # không đơn vị: dấu chấm là ngăn cách nghìn
        ("1tr", 1_000_000),
        ("1.5tr", 1_500_000),  # có đơn vị: dấu chấm là thập phân
        ("1,5tr", 1_500_000),
        ("2m", 2_000_000),
    ],
)
def test_parse_amount(token, expected):
    assert parse_amount(token) == expected


def test_parse_amount_invalid():
    with pytest.raises(ParseError):
        parse_amount("abc")


def test_amount_at_end():
    e = parse_expense("cafe 45k")
    assert e.amount == 45_000
    assert e.note == "cafe"
    assert e.category == "đồ uống"


def test_amount_at_start():
    e = parse_expense("45k cafe sáng")
    assert e.amount == 45_000
    assert e.note == "cafe sáng"


def test_number_in_middle_is_part_of_note():
    e = parse_expense("ăn trưa 2 người 90k")
    assert e.amount == 90_000
    assert e.note == "ăn trưa 2 người"
    assert e.category == "ăn uống"


def test_unknown_category_falls_back():
    assert parse_expense("cắt tóc 100k").category == "khác"


def test_extra_whitespace():
    assert parse_expense("   grab   35k  ").amount == 35_000


@pytest.mark.parametrize("text", ["", "   ", "cafe", "cafe abc"])
def test_no_amount_raises(text):
    with pytest.raises(ParseError):
        parse_expense(text)


def test_zero_amount_raises():
    with pytest.raises(ParseError):
        parse_expense("cafe 0")
