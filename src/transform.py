"""
Phase 1 — Single-Year Schema Inspection

Purpose:
- Inspect the structure of job ads for one year at a time
- No transformations, no writes
"""

import json
from pathlib import Path
from pprint import pprint


YEAR = 2016
RAW_FILE = Path(f"data/raw/arbetsformedlingen/{YEAR}/{YEAR}.jsonl")


def inspect_one_record(path: Path) -> None:
    with path.open("r", encoding="utf-8") as f:
        first_line = f.readline()

    record = json.loads(first_line)

    print(f"Top-level keys in {YEAR}:")
    pprint(list(record.keys()))

    print(f"\nExample record from {YEAR}:")
    pprint(record)


if __name__ == "__main__":
    inspect_one_record(RAW_FILE)
