import csv, json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_score, recall_score, accuracy_score, confusion_matrix

SRC = "/home/dima/git/marcotech/sqlabs/lab1/dataset/SMSSpamCollection"
try:
    raw = pd.read_csv(SRC, sep="\t", header=None, names=["label", "text"], quoting=csv.QUOTE_NONE, encoding="utf-8")
except UnicodeDecodeError:
    raw = pd.read_csv(SRC, sep="\t", header=None, names=["label", "text"], quoting=csv.QUOTE_NONE, encoding="latin-1")
raw["label"] = raw["label"].astype(str).str.strip().str.lower()
raw = raw.dropna(subset=["text"]).copy()
raw["text"] = raw["text"].astype(str).str.strip()
conflicts = raw.groupby("text")["label"].nunique()
ambiguous = set(conflicts[conflicts > 1].index)
df = raw.loc[~raw["text"].isin(ambiguous)].drop_duplicates("text").reset_index(drop=True)

out = {}
out["source_rows"] = len(raw)
out["usable"] = len(df)
out["conflicts"] = len(ambiguous)
out["counts"] = df["label"].value_counts().to_dict()
out["pct"] = (df["label"].value_counts(normalize=True) * 100).round(2).to_dict()

X_temp, X_test, y_temp, y_test = train_test_split(df["text"], df["label"], test_size=0.20, stratify=df["label"], random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, stratify=y_temp, random_state=42)
out["split"] = {n: {"n": len(y), "spam": int((y == "spam").sum()), "spam_pct": round(100 * (y == "spam").mean(), 2)}
                for n, y in [("train", y_train), ("val", y_val), ("test", y_test)]}

def fit(alpha, min_df=1):
    p = Pipeline([("tfidf", TfidfVectorizer(min_df=min_df)), ("classifier", MultinomialNB(alpha=alpha))])
    p.fit(X_train, y_train)
    return p

def scores(p, X, y):
    pred = p.predict(X)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=["ham", "spam"]).ravel()
    return {"acc": round(accuracy_score(y, pred), 4),
            "precision": round(precision_score(y, pred, pos_label="spam", zero_division=0), 4),
            "recall": round(recall_score(y, pred, pos_label="spam", zero_division=0), 4),
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp), "alerts": int((pred == "spam").sum())}

out["runs"] = {}
for name, a in [("A", 0.5), ("B", 1.0)]:
    p = fit(a)
    out["runs"][name] = scores(p, X_val, y_val)
    out["runs"][name]["vocab"] = len(p.named_steps["tfidf"].vocabulary_)

out["alpha_sweep"] = {}
for a in [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]:
    out["alpha_sweep"][a] = scores(fit(a), X_val, y_val)

out["min_df"] = {}
for m in [1, 2, 3, 5]:
    p = fit(0.5, m)
    s = scores(p, X_val, y_val)
    s["vocab"] = len(p.named_steps["tfidf"].vocabulary_)
    out["min_df"][m] = s
for a in [0.5, 1.0]:
    for m in [1, 3]:
        p = fit(a, m)
        s = scores(p, X_val, y_val)
        s["vocab"] = len(p.named_steps["tfidf"].vocabulary_)
        out.setdefault("alpha_mindf", {})[f"{a}/{m}"] = s

# AUTO choice and custom messages
pa, pb = fit(0.5), fit(1.0)
sel = pa if out["runs"]["A"]["precision"] >= out["runs"]["B"]["precision"] else pb
msgs = ["Hi! Can we meet at the library tomorrow?", "Congratulations! Claim your free prize now!", "Please send the meeting notes when you can."]
idx = list(sel.classes_).index("spam")
out["custom"] = {}
for nm, p in [("A", pa), ("B", pb)]:
    out["custom"][nm] = [(m, str(p.predict([m])[0]), round(float(p.predict_proba([m])[0, idx]), 4)) for m in msgs]
out["test_A"] = scores(pa, X_test, y_test)
out["test_B"] = scores(pb, X_test, y_test)

# most spam-like and ham-like words for selected model(s)
import numpy as np
for nm, p in [("A", pa), ("B", pb)]:
    vec = p.named_steps["tfidf"]; clf = p.named_steps["classifier"]
    names = np.array(vec.get_feature_names_out())
    log_ratio = clf.feature_log_prob_[idx] - clf.feature_log_prob_[1 - idx]
    order = np.argsort(log_ratio)
    out[f"top_spam_words_{nm}"] = names[order[::-1][:10]].tolist()
    out[f"top_ham_words_{nm}"] = names[order[:10]].tolist()

with open("/tmp/s3work/ref.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
print("done")
