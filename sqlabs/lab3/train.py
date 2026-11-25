"""Session 4 SMS workflow: load/check -> split -> train -> evaluate -> save.

Run with: python3 train.py --version v1
Only training data fits the scikit-learn Pipeline. Validation is for model review.
The held-out test data is NEVER used to choose a candidate in this lab.
"""

import argparse
import json
import re
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent
RANDOM_SEED = 42
MIN_SPAM_PRECISION = 0.90  # Classroom-only example, NOT universal guidance.
MIN_SPAM_RECALL = 0.00     # Advanced challenge: raise this and observe the gate.


def log(message):
    print(message, flush=True)


def load_and_check(path):
    log('[1/5] LOAD + CHECK — STARTED')
    data = pd.read_csv(path, keep_default_na=False)
    missing = {'text', 'label'} - set(data.columns)
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(sorted(missing))}")
    if data.empty:
        raise ValueError('Dataset is empty')
    if not data['text'].map(lambda x: isinstance(x, str) and bool(x.strip())).all():
        raise ValueError('Empty or invalid SMS text found')
    if not data['label'].isin(['ham', 'spam']).all():
        raise ValueError("Labels must be exactly 'ham' or 'spam'")
    counts = data['label'].value_counts()
    if set(counts.index) != {'ham', 'spam'} or counts.min() < 10:
        raise ValueError('Need at least 10 ham and 10 spam examples')
    log(f'[1/5] LOAD + CHECK — COMPLETED ({len(data)} rows)')
    return data


def split_data(data):
    log('[2/5] SPLIT — STARTED')
    train_valid, _untouched_test = train_test_split(
        data, test_size=0.15, random_state=RANDOM_SEED, stratify=data['label']
    )
    train, valid = train_test_split(
        train_valid, test_size=0.15 / 0.85, random_state=RANDOM_SEED,
        stratify=train_valid['label']
    )
    log(f'[2/5] SPLIT — COMPLETED (train={len(train)}, '
        f'validation={len(valid)}, held-out test={len(_untouched_test)})')
    return train, valid


def fit_model(train):
    log('[3/5] TRAIN — STARTED')
    model = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=1.0)),
    ])
    model.fit(train['text'], train['label'])
    # log(f"TF-IDF features: {len(model.named_steps['tfidf'].vocabulary_)}")
    log('[3/5] TRAIN — COMPLETED')
    return model


def evaluate(model, valid):
    log('[4/5] EVALUATE — STARTED')
    predicted = model.predict(valid['text'])
    precision = float(precision_score(valid['label'], predicted,
                                      pos_label='spam', zero_division=0))
    recall = float(recall_score(valid['label'], predicted,
                                pos_label='spam', zero_division=0))
    log(f'[4/5] EVALUATE — COMPLETED (spam precision={precision:.3f}, '
        f'spam recall={recall:.3f})')
    return {'spam_precision': round(precision, 4),
            'spam_recall': round(recall, 4),
            'minimum_spam_precision': MIN_SPAM_PRECISION,
            'minimum_spam_recall': MIN_SPAM_RECALL,
            'random_seed': RANDOM_SEED}


def quality_gate(metrics):
    # EXERCISE 2: Add one status log showing the required and actual spam precision.
    # Hint: metrics['spam_precision'] and MIN_SPAM_PRECISION
    if metrics['spam_precision'] < MIN_SPAM_PRECISION:
        raise ValueError('Quality gate FAILED: spam precision below threshold')
    if metrics['spam_recall'] < MIN_SPAM_RECALL:
        raise ValueError('Quality gate FAILED: spam recall below threshold')
    log('QUALITY GATE — PASSED')


def save(model, metrics, version):
    log('[5/5] SAVE — STARTED')
    models_dir = ROOT / 'models'
    models_dir.mkdir(exist_ok=True)
    model_path = models_dir / f'sms_model_{version}.joblib'
    metrics_path = models_dir / f'metrics_{version}.json'
    if model_path.exists() or metrics_path.exists():
        raise FileExistsError('Version already exists. Select a new --version.')
    joblib.dump(model, model_path)
    metrics_path.write_text(json.dumps({'version': version, **metrics}, indent=2) + '\n',
                            encoding='utf-8')
    log(f'[5/5] SAVE — COMPLETED ({model_path.relative_to(ROOT)})')
    return model_path


def main():
    parser = argparse.ArgumentParser(description='Repeatable SMS model training')
    parser.add_argument('--data', default='data/sms.csv', help='CSV with text,label')
    parser.add_argument('--version', default='v1', help='New version, e.g. v1 or v2')
    args = parser.parse_args()
    if not re.fullmatch(r'v[0-9]+', args.version):
        parser.error('Version must look like v1, v2, ...')
    data_path = Path(args.data)
    if not data_path.is_absolute():
        data_path = ROOT / data_path
    try:
        data = load_and_check(data_path)
        train, valid = split_data(data)
        model = fit_model(train)
        metrics = evaluate(model, valid)
        quality_gate(metrics)
        model_path = save(model, metrics, args.version)
    except (ValueError, FileNotFoundError, FileExistsError, pd.errors.ParserError) as error:
        log(f'FAILED — {error}')
        raise SystemExit(1) from error
    log(f'SUCCESS — {model_path.name} is ready for Session 5')
    log('NOTE — the final held-out test set was not used for model selection')


if __name__ == '__main__':
    main()
