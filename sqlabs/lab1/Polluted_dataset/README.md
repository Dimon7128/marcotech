# Data Pollution Challenge

This optional experiment shows why data quality matters. It keeps the original UCI
SMS dataset unchanged and creates a second file with repeated, incorrectly labeled
examples.

## Files

| File | Purpose |
|---|---|
| `baseline_SMSSpamCollection` | Unchanged UCI source dataset: 5,574 rows. |
| `balanced_polluted_SMSSpamCollection` | Generated scenario C dataset: 7,884 rows. |
| `generate_polluted.py` | Deterministically creates and validates the polluted file. |
| `prepare_data.py` | Small replacement for the notebook's Step 3 cleaning block. |

Both datasets are tab-separated and have no header. Load them with the column names
`label` and `text`.

## Scenario A: Baseline

- Use `baseline_SMSSpamCollection`.
- Call `prepare_data(raw, remove_duplicates=True)`.
- Original rows: 5,574 (`ham`: 4,827; `spam`: 747).

## Scenario C: Balanced Pollution

The generated file adds exactly 2,310 rows to the original source data:

- 1,000 copies of `WIN a FREE prize!`, incorrectly labeled `ham`.
- 1,000 copies of the package-fee message, incorrectly labeled `ham`.
- 310 distinct, clearly spam messages, correctly labeled `spam`.

It has 7,884 rows (`ham`: 6,827; `spam`: 1,057). The overall spam percentage stays
close to the source dataset, but the repeated wrong labels make the data harmful.
Call `prepare_data(raw, remove_duplicates=False)` so the repeated polluted messages
are not removed.

## Generate the polluted file

From this directory, run:

```bash
python generate_polluted.py
```

The script validates row counts, labels, and the 2,310 added rows every time it runs.

## Fair comparison in Colab

First make a clean test set **before** adding pollution. Then use only the clean
development rows plus the 2,310 appended pollution rows to train scenario C. This
prevents either model from training on the final clean test messages.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from prepare_data import prepare_data

COLUMNS = ["label", "text"]

def load_sms(filename):
    return pd.read_csv(filename, sep="\t", header=None, names=COLUMNS, encoding="latin-1")

baseline_raw = load_sms("baseline_SMSSpamCollection")
polluted_raw = load_sms("balanced_polluted_SMSSpamCollection")

# This test set is clean and never used as training data.
clean_all = prepare_data(baseline_raw, remove_duplicates=True)
clean_development, clean_test = train_test_split(
    clean_all, test_size=0.15, stratify=clean_all["label"], random_state=42
)

# The generated pollution begins immediately after the 5,574 original rows.
pollution_rows = polluted_raw.iloc[len(baseline_raw):].copy()
scenario_a = clean_development.copy()
scenario_c = pd.concat([clean_development, pollution_rows], ignore_index=True)

polluted_examples = [
    "WIN a FREE prize!",
    "URGENT: Your package is waiting! Pay $1.99 delivery fee to release your prize: http://ship-pkg.info",
]

def train_and_evaluate(name, training_data):
    X_train, X_val, y_train, y_val = train_test_split(
        training_data["text"], training_data["label"], test_size=0.20,
        stratify=training_data["label"], random_state=42
    )
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", MultinomialNB()),
    ])
    model.fit(X_train, y_train)

    # Both models use the same untouched clean test set.
    predicted = model.predict(clean_test["text"])
    print(f"\n{name} - clean test")
    print("Rows:", len(training_data))
    print("Accuracy:", round(accuracy_score(clean_test["label"], predicted), 3))
    print("Spam precision:", round(precision_score(clean_test["label"], predicted, pos_label="spam", zero_division=0), 3))
    print("Spam recall:", round(recall_score(clean_test["label"], predicted, pos_label="spam", zero_division=0), 3))
    ConfusionMatrixDisplay.from_predictions(clean_test["label"], predicted, labels=["ham", "spam"])
    plt.title(f"{name} - untouched clean test")
    plt.show()

    print("Polluted-message predictions:")
    for message, label in zip(polluted_examples, model.predict(polluted_examples)):
        print(f"{label.upper():4} | {message}")
    return model

baseline_model = train_and_evaluate("Scenario A: baseline", scenario_a)
polluted_model = train_and_evaluate("Scenario C: balanced pollution", scenario_c)
```

Do not compare the models only on a split of the polluted file: that evaluation
contains repeated wrong labels and can hide real-world harm. The untouched clean test
set is the meaningful comparison.
