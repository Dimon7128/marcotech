"""Make a broken COPY of the dataset; never change the original."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'data' / 'sms.csv'
DESTINATION = ROOT / 'data' / 'sms_broken.csv'

# EXERCISE 3: Change 'text' to 'label', then regenerate the broken copy.
COLUMN_TO_DROP = 'text'

data = pd.read_csv(SOURCE)
if COLUMN_TO_DROP not in data.columns:
    raise ValueError(f'Column not found: {COLUMN_TO_DROP}')
data = data.drop(columns=[COLUMN_TO_DROP])
data.to_csv(DESTINATION, index=False)
print(f'Created broken copy: {DESTINATION.relative_to(ROOT)}')
print(f'Remaining columns: {list(data.columns)}')
