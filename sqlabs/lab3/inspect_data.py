"""Look at the structure of the SMS dataset without printing message text."""
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parent / 'data' / 'sms.csv'
data = pd.read_csv(path)
print('Rows:', len(data))
print('Columns:', list(data.columns))
print('Missing values:', data[['text', 'label']].isna().sum().to_dict())

# EXERCISE 1: Uncomment the line below to see ham/spam counts.
# print('Class counts:', data['label'].value_counts().to_dict())
