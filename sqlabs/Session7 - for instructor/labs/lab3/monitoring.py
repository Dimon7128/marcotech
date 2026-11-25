"""Shared, readable implementation copied into Labs 3 and 4.

Only two derived features enter Evidently. No raw-text drift model is used.
"""
from pathlib import Path
import json
from importlib.metadata import version

import pandas as pd
from evidently import Dataset, DataDefinition, Report
from evidently.presets import DataDriftPreset

URL_MARKERS = ("http://", "https://", "www.")


def has_url_like(message):
    """Same approximate substring rule as Lab 2; not a spam decision."""
    return any(marker in message.lower() for marker in URL_MARKERS)


def load_features(path):
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"Missing CSV: {path.name}. Keep the data folder beside the notebook/script.")
    try:
        records = pd.read_csv(path, dtype=str, keep_default_na=False)
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        raise ValueError(f"Invalid CSV: {path.name}.") from error
    if list(records.columns) != ["record_id", "message"]:
        raise ValueError(f"{path.name}: expected exactly record_id,message columns.")
    if records.empty:
        raise ValueError(f"{path.name}: the batch has no messages.")
    if records.record_id.str.strip().eq("").any() or records.record_id.duplicated().any():
        raise ValueError(f"{path.name}: record IDs must be nonempty and unique.")
    if records.message.str.strip().eq("").any():
        raise ValueError(f"{path.name}: missing or empty message; restore the supplied CSV.")
    # Character count includes stored spaces and punctuation, just as in Lab 2.
    return pd.DataFrame({
        "message_length": records.message.str.len(),
        "has_url": records.message.apply(lambda text: "yes" if has_url_like(text) else "no"),
    })


def summarize(features):
    count = int(features.has_url.eq("yes").sum())
    return {"messages": len(features), "average_length": float(features.message_length.mean()),
            "url_like_count": count, "url_like_percentage": 100 * count / len(features)}


def make_report(reference_features, current_features):
    # Explicit types: a numerical length and a categorical yes/no indicator.
    schema = DataDefinition(numerical_columns=["message_length"], categorical_columns=["has_url"])
    reference = Dataset.from_pandas(reference_features, data_definition=schema)
    current = Dataset.from_pandas(current_features, data_definition=schema)
    # The tested API takes CURRENT first, REFERENCE second.
    return Report([DataDriftPreset()]).run(current, reference)


def export_report(result, reference_features, current_features, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    result.save_html(str(output / "monitoring_report.html"))
    result.save_json(str(output / "evidently_result.json"))
    summary = {"synthetic": True, "evidently_version": version("evidently"),
               "reference": summarize(reference_features), "current": summarize(current_features),
               "quality_evidence": "No labels or matching predictions; accuracy is unknown."}
    (output / "feature_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = ["# Synthetic SMS feature summary", "", "Computed directly from the supplied CSVs.", "",
             "| Batch | Messages | Mean characters | URL-like messages | URL-like share |",
             "| --- | ---: | ---: | ---: | ---: |"]
    for label, key in [("Reference (earlier)", "reference"), ("Current (newer)", "current")]:
        row = summary[key]
        lines.append(f'| {label} | {row["messages"]} | {row["average_length"]:.1f} | {row["url_like_count"]} | {row["url_like_percentage"]:.1f}% |')
    lines += ["", "`message_length` counts characters; `has_url` uses the case-insensitive substring rule",
              "`http://`, `https://` or `www.`. It does not validate URLs or classify spam.", "",
              "This table describes input changes. Use the real HTML report for the tool's result.",
              "No reliable labels or matching predictions are provided. Prediction quality is unknown.", ""]
    (output / "FEATURE_SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")
    return output / "monitoring_report.html"
