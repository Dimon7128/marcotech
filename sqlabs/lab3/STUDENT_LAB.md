# MLOps Essentials — Session 4 Student Lab
## A Repeatable SMS Training Pipeline

**Mission:** Run a trustworthy SMS training workflow with one command, explain its stages, recognize a failure, and save the **entire fitted TF-IDF + Naive Bayes pipeline** for Session 5.

**Project flow:** Load + check → stratified split → fit TF-IDF and classifier → evaluate → quality gate → save. The **test data stays untouched** during candidate selection. The notebook experiments and MLflow runs from earlier sessions remain useful; this lab packages training into a repeatable script.

**Files to use:** `prepare_data.py`, `inspect_data.py`, `train.py`, `make_bad_data.py`, `compare_runs.py`, `predict.py`, `requirements.txt`. Most code is already provided. There are **four small coding exercises**, clearly marked.

> **Before running anything:** Predict what a successful training run should create. What could go wrong if the SMS dataset contains no `text` column?

---

## Beginner Core — Mandatory

### Step 1 — Prepare your project

**WHY:** Everyone needs the same basic environment and input format.

**WHAT:** Use local Python and the official UCI SMS dataset. The original UCI data contains 5,574 labeled messages and must be converted into a CSV with `text` and `label` columns.

**RUN** — open a terminal **inside the extracted project folder**:

```bash
python -m venv .venv
```

Activate it:

- **Windows PowerShell:** `.venv\Scripts\Activate.ps1`
- **macOS/Linux:** `source .venv/bin/activate`

Then:

```bash
python -m pip install -r requirements.txt
python prepare_data.py
```

**VERIFY:** The terminal reports `READY` and a file `data/sms.csv` exists. It contains `text` and `label` columns. The download uses UCI data, not a synthetic replacement.

**EXPLAIN:** Why do we prepare the dataset once instead of downloading it during every training run?

<details><summary>Hint / fallback</summary>
If the download fails, open https://archive.ics.uci.edu/dataset/228/sms+spam+collection in your browser, download the ZIP, and run `python prepare_data.py --zip "PATH_TO_ZIP"`. You can also copy a previously normalized `text,label` UCI CSV from an earlier session to `data/sms.csv`. If PowerShell blocks activation, use `.venv\Scripts\python.exe` instead of `python` for each subsequent command.
</details>

### Step 2 — Inspect the dataset (Coding Exercise 1)

**WHY:** An ML pipeline should verify its input before training.

**WHAT:** Inspect row count, column names, missing values, and the balance between ham and spam.

**Predict:** Will the dataset contain approximately the same number of ham and spam messages?

**RUN:**

```bash
python inspect_data.py
```

Open `inspect_data.py` and **uncomment the line** beginning with `# print('Class counts:'...` so you see the count of each label. Run it again.

**VERIFY:** You see the `text` and `label` columns, and class counts showing **more ham than spam**. No raw SMS message text is printed.

**EXPLAIN:** Why might accuracy be misleading on a dataset with many more ham messages than spam?

<details><summary>Hint</summary>
A comment begins with `#`. Removing that first `#` activates a provided Python statement. A model that predicts “ham” most of the time might be accurate overall but miss spam.
</details>

### Step 3 — Run the complete workflow (Coding Exercise 2)

**WHY:** One command should run stages in a reliable order.

**WHAT:** Train the baseline candidate, read its stage status messages, and add one useful log.

**Predict:** Which stage must run before TF-IDF is fitted? Which stage should run before the artifact is saved?

**RUN:**

```bash
python train.py --version v1
```

Look for `LOAD + CHECK`, `SPLIT`, `TRAIN`, `EVALUATE`, `QUALITY GATE`, and `SAVE`. Then open `train.py`, find `quality_gate()`, and **add one log line** *before* the precision comparison that prints the required and observed spam precision. Suggested starting point:

```python
log(f"Precision gate: required {MIN_SPAM_PRECISION}, observed {metrics['spam_precision']}")
```

**Important:** Do **not** rerun with `v1` after it succeeds; model versions are not overwritten. Your new log will appear when you train `v2` in Step 5.

**VERIFY:** A successful first run created `models/sms_model_v1.joblib` and `models/metrics_v1.json`. Stage messages appear in the expected order.

**EXPLAIN:** Why is it useful to see which stage failed without opening the full script?

<details><summary>Hint / fallback</summary>
Find the `quality_gate(metrics)` function. Put the new line inside the function and keep the same four-space indentation as the surrounding statements. If the quality gate fails on your real dataset, record the actual precision and recall; ask the instructor to review the source data and split instead of changing the threshold just to pass.
</details>

### Step 4 — Read the evaluation and make a decision

**WHY:** A finished training run is not automatically an acceptable model.

**WHAT:** Inspect the measured spam precision, recall, and the classroom quality gate.

**Predict:** Can precision be high while recall is low? What would that mean for missed spam?

**RUN:** Open `models/metrics_v1.json` with a text editor. Find `spam_precision`, `spam_recall`, and `minimum_spam_precision`.

**VERIFY:** The report stores numeric validation metrics and the threshold used for the run. **Your actual values may differ** from other students if the input dataset or package versions differ.

**EXPLAIN:** Would you accept the model solely because `spam_precision` passed the example 0.90 gate? What else should you examine?

<details><summary>Hint</summary>
Precision asks: “When we say spam, how often are we right?” Recall asks: “Of all actual spam messages, how many did we catch?” Both matter.
</details>

### Step 5 — Break and repair the workflow (Coding Exercise 3)

**WHY:** Good automation should stop before training when inputs are invalid.

**WHAT:** Generate a **broken copy** of the dataset, observe the error, then correct the input.

**Predict:** If the `text` column is removed, will a model file for `v2` be created?

**RUN:**

```bash
python make_bad_data.py
python train.py --data data/sms_broken.csv --version v2
```

This run should **fail**. Inspect its message. Then open `make_bad_data.py` and change `COLUMN_TO_DROP = 'text'` to `COLUMN_TO_DROP = 'label'`. Rerun both commands and compare the error messages.

Now **repair the input** by using the original validated dataset:

```bash
python train.py --data data/sms.csv --version v2
```

**VERIFY:** The two broken runs stop before fitting and do not create `sms_model_v2.joblib`. The corrected run succeeds, creates `v2`, and displays your **new quality-gate log** from Step 3.

**EXPLAIN:** Why do we change a copy instead of damaging the original data file?

<details><summary>Hint</summary>
Open `make_bad_data.py` and change only the string after `COLUMN_TO_DROP =`. The validation function in `train.py` checks that both required columns exist.
</details>

### Step 6 — Verify repeatability (Coding Exercise 4)

**WHY:** Repeating the same procedure with unchanged inputs and settings should produce comparable results.

**WHAT:** Add a tiny training-status detail, run a new version, and compare validation metrics.

**Predict:** If data, random seed, dependencies, and training parameters remain unchanged, should `v3` have the same validation precision and recall as `v1`?

**RUN:** Open `train.py` and find the comment marked `EXERCISE 4` in `fit_model()`. Add this line **after `model.fit(...)`**:

```python
log(f"TF-IDF features: {len(model.named_steps['tfidf'].vocabulary_)}")
```

Then:

```bash
python train.py --version v3
python compare_runs.py v1 v3
```

**VERIFY:** The new log prints a vocabulary size. The `v1` and `v3` **validation precision and recall match** in the same environment with unchanged data and training settings.

**EXPLAIN:** Did adding a log change the model? What changes *would* make the results different?

<details><summary>Hint</summary>
The number of TF-IDF features comes from the fitted vectorizer: `model.named_steps['tfidf'].vocabulary_`. Logging should not modify model training.
</details>

### Step 7 — Reuse the whole fitted pipeline

**WHY:** Session 5 will load a saved artifact for inference instead of training again.

**WHAT:** Load the trusted artifact and ask it to classify **synthetic** messages.

**Predict:** Should `predict.py` need the training CSV?

**RUN:**

```bash
python predict.py --version v1 --text "Claim your free reward today"
python predict.py --version v1 --text "Please pick up bread after work"
```

**VERIFY:** Each command prints a predicted `spam` or `ham` label; it does **not** retrain the model. Individual predictions are model-dependent, so investigate rather than assume an exact answer.

**EXPLAIN:** Why would saving only the Naive Bayes classifier, without TF-IDF, cause problems when handling new text?

<details><summary>Hint</summary>
The model expects numerical features, while the application receives raw strings. The saved pipeline must include the fitted text transformation.
</details>

---

## Step 8 — Optional Advanced Challenge: Add a Recall Quality Gate

**Scenario:** The team cares about missed spam as well as wrongly flagged legitimate messages. Can our training workflow refuse to save a candidate that misses too much spam?

**WHY:** Quality gates decide whether a candidate is acceptable; training completion alone is not enough.

**WHAT:** Change a configurable recall threshold, observe a rejected run, then restore it and try again. **Do not change the data or fitted-model parameters.**

**Predict:** Does tightening the recall gate change the model's measured recall, or only the decision to save it?

**RUN:**

1. Read `spam_recall` from `models/metrics_v1.json`.
2. Open `train.py` and find `MIN_SPAM_RECALL = 0.00`.
3. Set it to a threshold **higher than the measured recall**, such as `1.00` if recall is below 1.00. (If recall is exactly 1.00, temporarily use `1.01` only to demonstrate an impossible gate.)
4. Run `python train.py --version v4`.
5. Verify that training and evaluation complete, but the recall quality gate **rejects saving v4**.
6. Restore `MIN_SPAM_RECALL = 0.00` and run the same `v4` command again.

**VERIFY:** First attempt ends with `Quality gate FAILED` and no `sms_model_v4.joblib`; the second attempt saves the file. Compare the logged recall values between runs.

**EXPLAIN:** Did the model improve after relaxing the gate? What is the risk of making a gate too strict or too lenient?

<details><summary>Hint</summary>
The gate is in `quality_gate()`, *after* `evaluate()` and *before* `save()`. The model is trained the same way both times. Only the acceptance policy changes.
</details>

---

## Step 9 — Final verification and Session 5 handoff

**RUN:** Check the `models/` folder for `sms_model_v1.joblib` and `metrics_v1.json`. Use:

```bash
python predict.py --version v1 --text "Let's meet at the library tomorrow"
```

**VERIFY:** You can load the saved whole pipeline and get a prediction without the training dataset. Keep this trusted file and your matching `requirements.txt` for Session 5 (FastAPI deployment).

**Exit questions:** What prevents bad input from reaching training? Why don't we fit TF-IDF on the validation/test sets? Why must a new model be evaluated before it is promoted?

**Dataset credit:** Almeida & Hidalgo (2011), *SMS Spam Collection*, UCI Machine Learning Repository, DOI: 10.24432/C5CC84, CC BY 4.0. Use **synthetic** SMS for your own inference examples. Do not upload private messages or load unfamiliar `.joblib` files.
