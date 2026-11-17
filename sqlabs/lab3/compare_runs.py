"""Compare saved validation reports for two versions; do not use the test set."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('first', help='e.g. v1')
parser.add_argument('second', help='e.g. v2')
args = parser.parse_args()

for version in (args.first, args.second):
    path = ROOT / 'models' / f'metrics_{version}.json'
    report = json.loads(path.read_text(encoding='utf-8'))
    print(f"{version}: precision={report['spam_precision']:.4f}, "
          f"recall={report['spam_recall']:.4f}, seed={report['random_seed']}")
