"""Generate a local report. Run: python run_report.py. No model is trained."""
from pathlib import Path
from monitoring import load_features, make_report, export_report, summarize

ROOT = Path(__file__).resolve().parent

def main():
    reference = load_features(ROOT / "data/reference_sms.csv")
    current = load_features(ROOT / "data/current_sms.csv")
    print("SYNTHETIC SMS — no labels or model predictions.")
    print("Reference:", summarize(reference))
    print("Current:  ", summarize(current))
    result = make_report(reference, current)
    path = export_report(result, reference, current, ROOT / "output")
    print("Open in your browser:", path)
    print("Data drift alone does not measure prediction quality.")

if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"Input problem: {error} See the lab guide or use the prepared output.")
