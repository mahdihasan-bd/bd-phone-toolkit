import pytest

from phone_tool import InvalidNumber, is_valid, operator_of, parse


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("01712345678", "+8801712345678"),
        ("+8801712345678", "+8801712345678"),
        ("8801712345678", "+8801712345678"),
        ("008801712345678", "+8801712345678"),
        ("017 1234-5678", "+8801712345678"),
        ("01712 345678", "+8801712345678"),
        ("+880 17 1234 5678", "+8801712345678"),
        ("1712345678", "+8801712345678"),
    ],
)
def test_parse_accepts_common_formats(raw, expected):
    assert parse(raw).e164 == expected


def test_national_is_zero_prefixed():
    assert parse("+8801912345678").national == "01912345678"


@pytest.mark.parametrize("raw", ["", "abc", "0171234567", "017123456789", "01012345678", "01212345678"])
def test_rejects_bad_input(raw):
    assert is_valid(raw) is False
    with pytest.raises(InvalidNumber):
        parse(raw)


@pytest.mark.parametrize(
    "raw,operator",
    [("01712345678", "Grameenphone"), ("01912345678", "Banglalink"), ("01512345678", "Teletalk"), ("01812345678", "Robi")],
)
def test_operator_lookup(raw, operator):
    assert operator_of(raw) == operator
