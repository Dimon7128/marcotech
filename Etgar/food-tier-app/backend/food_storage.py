"""
Data tier: a single CSV file at backend/data/food_history.csv.

Why a CSV?
    For an educational 3-tier app the CSV plays the role that a real database
    would play in production. It is human-readable, easy to inspect with
    `cat` / Excel, and lets students focus on the architecture instead of
    SQL setup.

Columns:
    food, tier, explanation

All public functions normalize the food name (trim + lowercase) so that
"Egg ", "egg" and "EGG" all map to the same row.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Optional

# Resolve the CSV path relative to this file so the module works the same
# whether you run `uvicorn` from the backend folder or from the project root.
DATA_DIR = Path(__file__).resolve().parent / "data"
CSV_PATH = DATA_DIR / "food_history.csv"

CSV_HEADER = ["food", "tier", "explanation"]


def normalize(food: str) -> str:
    """Single source of truth for how a food name is stored and looked up."""
    return food.strip().lower()


def ensure_csv_exists() -> None:
    """Create the CSV file (with header row) if it does not exist yet.

    Called once at application startup. Safe to call multiple times.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)


def find(food: str) -> Optional[dict]:
    """Return the saved row for `food`, or None if it is not in the CSV.

    The lookup is case- and whitespace-insensitive thanks to `normalize`.
    """
    key = normalize(food)
    if not CSV_PATH.exists():
        return None

    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Defensive: skip malformed rows instead of crashing the API.
            if not row.get("food"):
                continue
            if normalize(row["food"]) == key:
                return {
                    "food": row["food"],
                    "tier": row["tier"],
                    "explanation": row["explanation"],
                }
    return None


def save(food: str, tier: str, explanation: str) -> dict:
    """Append a new row to the CSV and return the saved dict.

    Note: we do NOT de-duplicate here. The caller (the service layer in
    main.py) is responsible for checking with `find()` first. Keeping the
    storage layer dumb makes it easier to reason about for students.
    """
    ensure_csv_exists()
    row = {
        "food": normalize(food),
        "tier": tier,
        "explanation": explanation,
    }
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writerow(row)
    return row
