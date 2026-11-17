"""Prepare the UCI SMS Spam Collection into data/sms.csv (text,label).

Source: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
Dataset: Almeida and Hidalgo (2011), CC BY 4.0.
"""

import argparse
import csv
import io
import urllib.request
import zipfile
from pathlib import Path

DATA_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description="Prepare the official UCI SMS dataset")
    parser.add_argument("--zip", dest="zip_path", type=Path,
                        help="Local copy of the official UCI dataset ZIP (offline option)")
    args = parser.parse_args()

    if args.zip_path:
        zip_bytes = args.zip_path.read_bytes()
        print("SOURCE — using local UCI ZIP")
    else:
        print("SOURCE — downloading the UCI SMS Spam Collection")
        try:
            with urllib.request.urlopen(DATA_URL, timeout=30) as response:
                zip_bytes = response.read()
        except Exception as exc:
            raise SystemExit(
                "Download failed. Download the ZIP from the UCI dataset page "
                "in your browser, then run: python prepare_data.py --zip YOUR_FILE.zip"
            ) from exc

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        members = [name for name in archive.namelist()
                   if name.rsplit("/", 1)[-1] == "SMSSpamCollection"]
        if len(members) != 1:
            raise SystemExit("Could not locate SMSSpamCollection inside the ZIP.")
        lines = archive.read(members[0]).decode("utf-8-sig").splitlines()

    rows = []
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        if "\t" not in line:
            raise SystemExit(f"Source line {index}: expected label and tab-separated text")
        label, text = line.split("\t", 1)
        label = label.strip().lower()
        if label not in {"ham", "spam"} or not text.strip():
            raise SystemExit(f"Source line {index}: invalid label or empty text")
        rows.append((text, label))

    out_path = ROOT / "data" / "sms.csv"
    out_path.parent.mkdir(exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["text", "label"])
        writer.writerows(rows)
    counts = {label: sum(1 for _, actual in rows if actual == label)
              for label in ("ham", "spam")}
    print(f"READY — {len(rows)} messages saved in data/sms.csv; "
          f"ham={counts['ham']}, spam={counts['spam']}")
    print("Privacy: text is not printed or included in training logs.")


if __name__ == "__main__":
    main()
