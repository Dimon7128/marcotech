"""Lab 2: compare synthetic SMS batches. Complete the single TODO below.

Run with the Python environment described in README.md: python starter.py
Loading, feature calculation and printing are supplied. No model is trained.
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
URL_MARKERS = ("http://", "https://", "www.")


def has_url_like(message):
    """Approximate substring check; it does not validate URLs or identify spam."""
    return any(marker in message.lower() for marker in URL_MARKERS)


def load_features(filename):
    records = pd.read_csv(ROOT / filename, dtype=str, keep_default_na=False)
    features = records.copy()
    features["message_length"] = features["message"].str.len()
    features["has_url_like"] = features["message"].apply(has_url_like)
    return features


def summarize(features):
    # TODO: replace None with the mean of the message_length column.
    average_length = None
    url_percentage = 100 * features["has_url_like"].mean()
    return {
        "Average length (characters)": average_length,
        "URL-like messages (%)": url_percentage,
    }


def main():
    print("SYNTHETIC SMS SCENARIOS — no production data, labels or model predictions.\n")
    batches = {"Reference": load_features("reference.csv"), "Current": load_features("current.csv")}
    for name, features in batches.items():
        print(f"{name}: {len(features)} synthetic messages")
        print(features[["record_id", "message_length", "has_url_like"]].to_string(index=False))
        print()
    summary = pd.DataFrame({name: summarize(features) for name, features in batches.items()})
    print("Comparison (rounded to one decimal place):")
    print(summary.round(1).fillna("TODO").to_string())
    print("\nExplain what changed, what is still unknown, and what evidence would help.")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        raise SystemExit("Keep reference.csv and current.csv beside starter.py. See README.md or use EXPECTED_RESULTS.md.")
