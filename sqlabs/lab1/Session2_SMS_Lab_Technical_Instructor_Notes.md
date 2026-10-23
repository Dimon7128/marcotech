# Session 2 — SMS Spam Lab: Technical Instructor Notes

**Companion to:** `Session2_SMS_Spam_Detection_Colab_UPDATED.ipynb`  
**Purpose:** Quick reference to **what each cell does**, **how it works**, and **which parameters matter**. Follow notebook Steps 0–8. No timings.

## Step 0 — Verify the environment

**Code:** `import pandas as pd`, `import sklearn`; print `pd.__version__` and `sklearn.__version__`.

- **What:** Checks both libraries can be imported; displays installed versions.
- **Why:** `pandas` handles dataset tables; `scikit-learn` handles splitting, training, and evaluation.
- **Key detail:** `as pd` gives pandas a short name. Versions help reproduce results and diagnose incompatibilities. **No installation is performed.**

## Step 1 — Download and load the dataset

**Code:** `urlopen(DATA_URL, timeout=20)` → `ZipFile` → `SMSSpamCollection` → `pd.read_csv(...)` → `sms.head(3)`.

- **What:** Downloads the UCI ZIP (or accepts a manual upload), extracts the text file, and loads it as a DataFrame named `sms`.
- **Why:** Training needs examples with the original SMS text **and** their known `ham` / `spam` labels.
- **Parameters:**
  - `DATA_URL`: the UCI ZIP address; `timeout=20`: give the download up to 20 seconds before falling back to upload.
  - `sep="\t"`: columns are tab-separated; `header=None`: the source has no header row.
  - `names=["label", "text"]`: assign understandable column names.
  - `encoding="latin-1"`: decode the source text; `quoting=csv.QUOTE_NONE`: treat quotes as ordinary characters.
- **Verify:** `len(sms)` must be **5,574 before cleaning**; `sms.head(3)` shows the first three labeled messages. `assert` stops execution when the downloaded file has an unexpected format.

## Step 2 — Investigate the dataset

**Code:** `sms.shape`, `sms.columns.tolist()`, `sms["label"].value_counts()` and `value_counts(normalize=True)`.

- **What:** Shows table dimensions, column names, class counts, and class percentages.
- **Parameters:** `normalize=True` returns **proportions**, multiplied by 100 for percentages; `.round(1)` displays one decimal place.
- **Guided exercise 1:** `sms.loc[sms["label"] == selected_label, ["label", "text"]]` filters rows for `selected_label="ham"` or `"spam"`; `.head(4)` shows four examples.
- **Guided exercise 2:** Remove `#` to activate `print(sms["label"].value_counts())`. `#` comments out a line.
- **Ask:** Which class is more common? Would a model predicting only `ham` have high overall accuracy? Can one word such as “free” reliably determine the label?

## Step 3 — Clean and split the data

**Code:** `dropna` → `str.strip()` → remove empty text → `drop_duplicates(subset="text")` → `train_test_split(...)` twice.

- **What:** Removes missing, blank, and exact duplicate messages, then creates **training / validation / test** sets.
- **Why:** Repeated identical messages appearing across sets could give an unrealistically optimistic evaluation.
- **Parameters:**
  - `subset=["label", "text"]` for `dropna`: discard rows missing either field.
  - `str.strip()`: remove leading/trailing whitespace; `subset="text"`: keep only the first occurrence of an identical text (even if a duplicate has a conflicting label).
  - First `test_size=0.30`: 70% training / 30% temporary data.
  - Second `test_size=0.50`: split that 30% equally into **15% validation / 15% test**.
  - `stratify=...`: approximately preserve the ham/spam ratio; `random_state=42`: make splits reproducible.
- **Key variables:** `X_*` = SMS text (inputs); `y_*` = correct labels (targets). The record count **decreases** after cleaning.

## Step 4 — Train the classifier

**Code:** `Pipeline([("tfidf", TfidfVectorizer()), ("classifier", MultinomialNB())])`; `model.fit(X_train, y_train)`.

- **What:** Builds one two-stage model and learns from **training data only**.
- **How:** `TfidfVectorizer()` learns vocabulary and converts text to numerical word features; `MultinomialNB()` uses those features to learn spam/ham patterns.
- **Parameters:** `TfidfVectorizer()` uses its defaults; `MultinomialNB()` uses default smoothing (`alpha=1.0`). Neither needs tuning for the core lab.
- **Why `Pipeline` matters:** The same text transformation is applied during both `fit()` and later `predict()`; fitting it on training data helps avoid **data leakage**.
- **Verify:** “Training complete” and two class names.

## Step 5 — Validate performance and inspect mistakes

**Code:** `model.predict(X_val)` → `show_scores(...)`; compare against `["ham"] * len(y_val)`.

- **What:** Measures performance on held-out validation SMS; compares with an **always-ham** baseline.
- **How:** `accuracy_score` = overall correct; `precision_score` = proportion of spam alerts that truly are spam; `recall_score` = proportion of actual spam detected.
- **Parameters:** `pos_label="spam"` makes spam the class being measured; `zero_division=0` reports zero when precision is otherwise undefined (e.g., no spam alerts); `round(..., 3)` prints three decimals.
- **Error investigation:** Build `validation_review`, keep rows where `actual != predicted`, then change `kind`:
  - `"missed spam"`: actual spam → predicted ham (**false negative**).
  - `"false alarm"`: actual ham → predicted spam (**false positive**).
- **Ask:** Why can the always-ham baseline have high accuracy and zero spam recall? Which mistake is more harmful for automatically blocked SMS?

## Optional advanced — Change spam classification strictness

**Code:** `model.predict_proba(X_val)[:, spam_index]` → `with_threshold(scores, threshold)`; compare `0.50`, `0.80`, optionally `0.90`.

- **What:** Changes the **decision rule**, not the trained model; flags spam only if its spam score meets the threshold.
- **Parameters:** `spam_index = list(model.classes_).index("spam")` identifies the correct score column; `[:, spam_index]` selects that score for every SMS; `threshold` sets the spam-flagging cutoff.
- **Expect:** Raising the threshold usually flags fewer messages and may reduce false alarms, **but precision need not increase** and recall may fall.
- **Important:** Naive Bayes scores from `predict_proba()` are **not necessarily calibrated probabilities**. Choose and compare thresholds on **validation data**, never the untouched test set. The notebook saves the **original pipeline**, not the custom threshold decision rule.

## Step 6 — Final test evaluation

**Code:** `model.predict(X_test)` → `show_scores(...)` → `ConfusionMatrixDisplay.from_predictions(...)`.

- **What:** Gives the original baseline model a final evaluation on untouched test messages.
- **Parameters:** `labels=["ham", "spam"]` sets matrix class order; `display_labels=["Ham", "Spam"]` controls displayed names; `values_format="d"` shows whole-number counts.
- **Read the plot:** **Rows = actual**, **columns = predicted**. Actual ham → predicted spam = false positive; actual spam → predicted ham = false negative.
- **Rule:** Do not keep tuning based on final test results; that compromises the independent check.

## Step 7 — Predict custom messages

**Code:** `new_messages = [...]`; `model.predict(new_messages)`; `zip(...)` prints each message beside its prediction.

- **What:** Performs inference on **three new synthetic** SMS messages (clear ham, clear spam, ambiguous).
- **Parameters:** Edit the three **strings** in `new_messages`; do **not** include their labels in model input.
- **Ask:** Which prediction surprised you? What wording may have influenced it?
- **Caution:** Three hand-written SMS are a demonstration, **not a statistically valid test set**; use invented messages, never private messages.

## Step 8 — Save the complete pipeline

**Code:** `joblib.dump(model, model_path)`; write JSON metadata; `joblib.load(model_path)`; compare predictions.

- **What:** Saves **TF-IDF + classifier together**, plus the dataset source, seed, package versions, and artifact name.
- **Parameters:** `model_path` (`.joblib`) is the model artifact; `info_path` (`.json`) is metadata; `indent=2` makes the JSON readable.
- **Verify:** Reload the trusted local file and confirm predictions match; uncomment `files.download(...)` lines in Colab to download both files.
- **Safety:** `joblib.load()` can execute code from untrusted files. Only load artifacts you created or fully trust; keep compatible library versions.

## Instructor quick reminders

- **Main story:** inspect data → split → fit text processing + classifier → validate → optional threshold experiment → final test → infer → save.
- **Most important parameters to explain:** `test_size`, `stratify`, `random_state`, `pos_label`, and advanced `threshold`.
- **Don't confuse:** class **imbalance** with model accuracy; **validation** with final test; **high precision** with **high recall**.
- **Troubleshooting:** download blocked → upload UCI ZIP; unexpected row count → verify original data; no errors shown in review → try the other `kind`; lost Colab runtime → rerun cells from Step 0.

## Relevant official documentation

- [UCI — SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
- [pandas — read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [scikit-learn — train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)
- [scikit-learn — TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [scikit-learn — MultinomialNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html)
- [scikit-learn — Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
- [scikit-learn — Classification metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
- [scikit-learn — Model persistence](https://scikit-learn.org/stable/model_persistence.html)
