"""Command line interface: python -m phone_tool <number> [--json]"""

from __future__ import annotations

import argparse
import json
import sys

from .core import InvalidNumber, parse


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="phone_tool", description="Validate and classify BD mobile numbers")
    ap.add_argument("number", help="number in almost any format: 01712345678, +880 1712 345678")
    ap.add_argument("--json", action="store_true", help="machine readable output")
    args = ap.parse_args(argv)

    try:
        num = parse(args.number)
    except InvalidNumber as exc:
        if args.json:
            print(json.dumps({"input": args.number, "valid": False, "error": str(exc)}))
        else:
            print(f"invalid: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"input": args.number, "valid": True, "e164": num.e164,
                          "national": num.national, "operator": num.operator}))
    else:
        print(f"valid    {num.e164}  ({num.operator})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
