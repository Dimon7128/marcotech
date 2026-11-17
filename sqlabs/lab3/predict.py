"""Tiny Session 5 preview: load ONLY a trusted local joblib artifact."""

import argparse
import re
from pathlib import Path

import joblib

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description="Predict a synthetic SMS example")
    parser.add_argument("--version", default="v1")
    parser.add_argument("--text", default="Claim your bonus prize now!")
    args = parser.parse_args()
    if not re.fullmatch(r"v[0-9]+", args.version):
        parser.error("--version must look like v1 or v2")
    artifact = ROOT / "models" / f"sms_model_{args.version}.joblib"
    if not artifact.is_file():
        parser.error(f"Model not found: {artifact.name}. Train first.")
    # joblib may execute code when loading. Load only artifacts YOU created and trust.
    model = joblib.load(artifact)
    print(f"Prediction: {model.predict([args.text])[0]}")


if __name__ == "__main__":
    main()
