# bd-phone-toolkit

Normalise, validate and classify Bangladeshi mobile numbers. Standard library only.

Built after hand-copying numbers from spreadsheets and SMS into a payment tool and getting the format wrong every second row.

## Install

```bash
git clone https://github.com/mahdihasan-bd/bd-phone-toolkit
cd bd-phone-toolkit
```

No dependencies. Python 3.9+.

## Use it as a library

```python
from phone_tool import parse, is_valid

n = parse("+880 1712-345678")
n.e164       # '+8801712345678'
n.national   # '01712345678'
n.operator   # 'Grameenphone'

is_valid("01012345678")   # False — 010 is not a mobile range
```

Accepted input: `01712345678`, `+8801712345678`, `8801712345678`, `008801712345678`, `1712345678`, and any of those with spaces, dashes or brackets.

Anything that is not an 11-digit number in an assigned operator range raises `InvalidNumber`.

## Use it from the shell

```bash
$ python -m phone_tool "017 1234 5678"
valid    +8801712345678  (Grameenphone)

$ python -m phone_tool 01012345678 --json
{"input": "01012345678", "valid": false, "error": "...is not an 11-digit BD mobile number"}
```

Exit code is `0` for a valid number, `1` for an invalid one, so it drops straight into shell pipelines.

## Tests

```bash
python -m pytest -q
```

## Operator prefixes

| Prefix | Operator |
| --- | --- |
| 013, 017 | Grameenphone |
| 014, 019 | Banglalink |
| 015 | Teletalk |
| 016 | Airtel |
| 018 | Robi |

Porting shifts numbers between networks, so treat the operator as a hint rather than a fact.

## Licence

MIT
