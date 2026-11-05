"""Normalise, validate and classify Bangladeshi mobile numbers.

Pure standard library — no dependencies.

    >>> from phone_tool import parse
    >>> p = parse("+880 1712-345678")
    >>> p.e164, p.operator
    ('+8801712345678', 'Grameenphone')
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# BD mobile numbers are 11 digits: 01X + 8 more. The third digit picks the operator.
OPERATOR_PREFIXES = {
    "013": "Grameenphone",
    "014": "Banglalink",
    "015": "Teletalk",
    "016": "Airtel",
    "017": "Grameenphone",
    "018": "Robi",
    "019": "Banglalink",
}

COUNTRY_CODE = "880"
_SEPARATORS = re.compile(r"[\s\-().]+")


class InvalidNumber(ValueError):
    """Raised when the input cannot be a Bangladeshi mobile number."""


@dataclass(frozen=True)
class PhoneNumber:
    national: str  # 01XXXXXXXXX
    e164: str      # +8801XXXXXXXXX
    operator: str
    is_mobile: bool = True


def _digits(raw: str) -> str:
    cleaned = _SEPARATORS.sub("", raw.strip())
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    if not cleaned.isdigit():
        raise InvalidNumber(f"unexpected characters in {raw!r}")
    return cleaned


def parse(raw: str) -> PhoneNumber:
    """Return a PhoneNumber for any common way of writing a BD mobile number."""
    d = _digits(raw)

    if d.startswith(COUNTRY_CODE):
        d = d[len(COUNTRY_CODE):]
    if d.startswith("00"):
        d = d[len("00") + len(COUNTRY_CODE):]
    if not d.startswith("0") and len(d) == 10:
        d = "0" + d

    if len(d) != 11 or not d.startswith("01"):
        raise InvalidNumber(f"{raw!r} is not an 11-digit BD mobile number")

    operator = OPERATOR_PREFIXES.get(d[:3])
    if operator is None:
        raise InvalidNumber(f"unknown operator prefix {d[:3]!r}")

    return PhoneNumber(national=d, e164="+" + COUNTRY_CODE + d[1:], operator=operator)


def is_valid(raw: str) -> bool:
    try:
        parse(raw)
    except InvalidNumber:
        return False
    return True


def operator_of(raw: str) -> str:
    return parse(raw).operator
