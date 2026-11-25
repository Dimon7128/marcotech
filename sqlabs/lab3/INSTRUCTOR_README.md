# Session 4 — Instructor guide: repeatable SMS training

Use [STUDENT_LAB.md](STUDENT_LAB.md) for student instructions and this guide for explanations, exercise solutions, preparation, and slide updates. The [project README](README.md) owns the file map, setup commands, and dataset credit. This is the single instructor reference for Lab 3.

## Teaching objective and boundaries

Students turn an experiment into an ordered workflow that checks input, stops on failure, and saves an accepted, reusable candidate. They run supplied scripts and make **four small edits**.

```text
load/check → split → fit → evaluate → quality gate → save
```

Explain the two meanings of pipeline:

- **Training workflow:** `train.main()` coordinates the stages above.
- **Fitted scikit-learn Pipeline:** TF-IDF plus Multinomial Naive Bayes, saved together so inference accepts raw text with the learned transformation.

Training starts manually. CT triggers, deployed-model comparison, promotion approval, and final test evaluation remain lecture concepts. Session 4 trains a new model from CSV; it does not load Session 3's estimator or call MLflow. See the README for the sessions' different preparation and split choices; their metrics are not directly comparable.

## Before class

Use local Python, a writable project folder, an editor, terminal, and browser. **Python >=3.10 is required** by pinned scikit-learn 1.7.2; Python 3.10 is the class baseline. Preserve `requirements.txt`: pandas 2.2.3, scikit-learn 1.7.2, joblib 1.5.3. Python and transitive dependencies are not fully pinned, so retain the working environment for comparisons and serving.

Follow the README setup once, then check from the lab folder with the selected interpreter:

```bash
python3 --version
python3 -c "import pandas, sklearn, joblib; print(pandas.__version__, sklearn.__version__, joblib.__version__)"
python3 inspect_data.py
```

Expected direct package versions: `2.2.3 1.7.2 1.5.3`. Check that `python3` selects Python 3.10 or newer in the active environment. If PowerShell blocks activation, invoke `.venv\Scripts\python.exe` directly.

The official UCI dataset is **not bundled**. Arrange download access or use:

```bash
python3 prepare_data.py --zip "PATH_TO_OFFICIAL_ZIP"
```

A previously normalized UCI `text,label` CSV is also supported. Observe preparation row/class counts rather than making an exact count a pass condition. Most script paths resolve from the script folder; relative `--zip` paths resolve from the terminal's current directory.

Keep the prepared input and environment unchanged during the exercise. Check that v1–v4 are unused; otherwise choose unused versions consistently throughout the worksheet. Demonstrate comments, four-space indentation, functions, CLI arguments, f-strings, dictionary access, and reading JSON as needed. No advanced Python, GitHub, Docker, GPU, or cloud account is needed today.

## Compact code reference

All six scripts serve distinct exercise roles; keep the README's file-to-task map. They exchange files rather than importing one another. `inspect_data.py`, `make_bad_data.py`, and `compare_runs.py` execute at the top level, so importing them also executes their operations.

| Stage / function | Behavior to explain |
|---|---|
| Preparation: `prepare_data.main()` | Reads one `SMSSpamCollection` member from a downloaded/local ZIP, splits at the first tab, normalizes labels, validates records, and writes `data/sms.csv`. Re-running replaces that CSV; duplicates are preserved. |
| Input: `load_and_check(path)` | Returns checked rows. Requires `text,label`, a nonempty dataset, nonblank string texts, exact `ham`/`spam` labels, and at least ten of each class. Invalid input stops before fitting. |
| Split: `split_data(data)` | Two stratified splits with seed 42 produce about 70% train / 15% validation / 15% test. Stratification preserves class proportions; it does not balance them. Only train and validation are returned. |
| Fit: `fit_model(train)` | Fits `TfidfVectorizer()` and `MultinomialNB(alpha=1.0)` on training rows only. Saved step names are `tfidf` and `classifier`. |
| Evaluate: `evaluate(model, valid)` | Predicts without refitting. Spam precision/recall use `pos_label='spam'`, `zero_division=0`; the report rounds scores to four decimals and includes thresholds and seed. |
| Accept: `quality_gate(metrics)` | Requires precision >=0.90 and recall >=0.00 by default. Both checks already exist; equality passes. Comparisons use rounded report scores. |
| Save: `save(model, metrics, version)` | Writes `models/sms_model_<version>.joblib` and `models/metrics_<version>.json`. Refuses a version if either file exists; this check occurs after fitting/evaluation. |
| Entry point: `main()` / `log()` | `--data` defaults to `data/sms.csv`; versions must be `v` plus digits. Stage logs flush immediately. Handled input/gate/version failures exit with status 1. |

**Two caveats:** Held-out test rows are discarded by `split_data()`; there is no saved test subset or final test score. Because preparation keeps duplicates and splitting is by row, identical messages may cross subsets. Training-only TF-IDF prevents preprocessing leakage but does not guarantee independent message content.

## Walkthrough and exercise solutions

Follow Student Steps 1–9 in order. The worksheet owns the full commands and reflection questions; these are the instructor checkpoints.

### Steps 1–2 — Prepare and inspect (Exercise 1)

After setup, run `python3 inspect_data.py`. Show column names and missing counts without printing message text. Explain that `ham` means legitimate SMS. Enable this provided line in `inspect_data.py` and rerun:

```python
print('Class counts:', data['label'].value_counts().to_dict())
```

Expect more ham than spam. A majority-class predictor can have high accuracy while missing spam; this motivates spam precision and recall.

### Steps 3–4 — Baseline and evaluation (Exercise 2)

Run `python3 train.py --version v1`. Show five numbered stages and the unnumbered gate between evaluation and saving. Success creates the matching model/report pair described above. Then add this line inside `quality_gate()`, before the comparisons:

```python
log(f"Precision gate: required {MIN_SPAM_PRECISION}, observed {metrics['spam_precision']}")
```

Do not rerun a successful v1: the new log appears on the repaired v2 run. Read `models/metrics_v1.json`: precision asks how often a spam prediction is correct; recall asks how much actual spam was caught. High precision can coexist with low recall. The gate is an illustrative classroom policy; passing it does not authorize deployment. Actual metrics depend on the input and environment.

### Step 5 — Break and repair input (Exercise 3)

```bash
python3 make_bad_data.py
python3 train.py --data data/sms_broken.csv --version v2
```

The first broken copy lacks `text`. Change only `COLUMN_TO_DROP = 'text'` to `COLUMN_TO_DROP = 'label'` in `make_bad_data.py`, then repeat both commands. Each attempt must report the missing column, stop before `TRAIN`, and create neither v2 output. The original CSV remains intact.

Repair by selecting the original input:

```bash
python3 train.py --data data/sms.csv --version v2
```

With the same accepted baseline input/settings, this saves v2 and displays Exercise 2's precision log. Input validation and validation-set evaluation are different checks at different stages.

### Step 6 — Repeatability (Exercise 4)

Add this line in `fit_model()`, immediately after `model.fit(...)`:

```python
log(f"TF-IDF features: {len(model.named_steps['tfidf'].vocabulary_)}")
```

Then run:

```bash
python3 train.py --version v3
python3 compare_runs.py v1 v3
```

Expect a positive vocabulary size and matching validation precision/recall when input, settings, and environment are unchanged. Logging changes observability rather than fitting. `compare_runs.py` prints values for manual comparison; it does not assert equivalence or promote a candidate. Equal rounded metrics do not prove identical artifact bytes or predictions on every message.

### Step 7 — Reuse the fitted pipeline

```bash
python3 predict.py --version v1 --text "Please pick up bread after work"
```

`predict.py` loads the saved whole pipeline, transforms text, and prints `ham` or `spam` without reading the CSV or calling `fit()`. Do not promise a particular label for an arbitrary example. Use synthetic messages and load only trusted joblib artifacts: loading can execute code.

### Step 8 — Optional recall challenge

The recall check is already implemented. Raise `MIN_SPAM_RECALL` above the measured v1 recall, then run `python3 train.py --version v4`. Use `1.00` if recall is below 1.00; `1.01` is an intentionally impossible demonstration only if recall equals 1.00.

Expect evaluation to finish, the gate to reject, and neither v4 output to exist. Restore `0.00` and rerun v4: measured recall stays the same and saving is allowed. Changing acceptance policy does not improve the fitted model. Discuss the costs of overly strict or permissive gates.

### Step 9 — Exit check

Locate the model/report pair, confirm prediction still works, and ask why input checks precede fitting, why TF-IDF learns only from training data, and why evaluation precedes promotion.

## Diagnose failures

| Symptom | Instructor response |
|---|---|
| Install/import failure | Check Python >=3.10, active interpreter, and installation of the existing requirements. scikit-learn is pinned to 1.7.2 for Python 3.10 compatibility. |
| Download/CSV unavailable | Prepare data first; use the official local-ZIP or normalized-CSV fallback above. |
| Missing column | Expected in Step 5. Select the original input instead of weakening validation. |
| Python edit fails | Check indentation, comment removal, quotation marks, and dictionary keys. |
| `Version already exists` | Either member of the output pair occupies that version; select an unused version consistently. |
| `Quality gate FAILED` | Read measured scores in the evaluation log: rejected runs save no metrics JSON. Review data/settings before changing policy. |
| Different repeatability metrics | Check dataset bytes, training settings, and environment, as well as the seed. |
| Artifact load/version error | Use the trusted local artifact and a compatible training/serving environment. |

## Handoff and preparation deadlines

**End of Session 4:** Retain the trusted `sms_model_v1.joblib`, matching metrics, requirements, and actual Python version. Confirm prediction works. Preserve original versioned files; [Session 5's starter](../lab4/Part1.md) uses a serving copy named `model.joblib` beside `main.py`.

| Session | Route and preparation |
|---|---|
| 5 — Prediction service | Keep local Python/editor/browser working. Instructor supplies compatible FastAPI/Uvicorn setup; load the whole pipeline once, without retraining on startup. Teach `/health`, `/predict`, JSON, invalid input, and browser `/docs`. Docker is a guided demo or optional extension in the revision brief; participants check client/server readiness with `docker version` beforehand. The existing lab4 handout includes a Docker part, so state the chosen participation scope explicitly. |
| 6 — CI | Prepare GitHub sign-in, repository write access, Actions permission, and a supported commit/push route. Instructor supplies tests, dependencies, workflow, and trusted model delivery to the runner. Push → Actions runner → API tests → Docker build where practical. No custom webhook, automatic retraining, persistent hosting, or cloud CD is established. |
| 7 — Monitoring | Supply reference/current batches and a local/notebook exercise or prepared report. Students decide investigate/keep/retrain; no retraining exercise is required by the revision brief. |
| 8 — Architecture/demo | Preserve code, artifacts, CI evidence, and monitoring decision. Explain AWS architecture and demonstrate accumulated work; the revision brief requires no live deployment or student AWS account. |

Introduce later tools and deadlines now; install their dependencies in the relevant lesson. Colab is an instructor-prepared training fallback, not a verified adapter or complete replacement for later work: check compatibility, run scripts from a real folder, and preserve outputs outside the temporary runtime. Use instructor CI logs/screenshots if GitHub access fails and a prepared monitoring report if generation fails.

## Slide-update brief

For slide revision, supply `session4.pptx`, this guide, `STUDENT_LAB.md`, `requirements.txt`, and the revised Sessions 3–8 plans. Inspect those inputs and flag missing/conflicting material. Preserve the four mandatory edits and beginner scope.

Prepare about nine short slide units:

| Unit | Essential student-facing idea / placement |
|---|---|
| 1. Roadmap | Experiments → repeatable training → prediction API. Reuse original slide 4; keep Sessions 6–8 brief. |
| 2. Working environment | Local Python today and for the API lesson. Put Colab limits in notes; place before practical work. |
| 3. Today's readiness | Python, writable project, editor/terminal, environment, official CSV. Keep commands/offline fallback in notes. |
| 4. Part 5 — Lab 3 | Run, inspect stages, break/repair, save whole pipeline. Replace original slide 33 and point to the worksheet. |
| 5. Deliverables | Model + report + requirements/Python note + successful prediction. Place after the lab. |
| 6. Session 5 | Synthetic SMS → FastAPI → saved pipeline → label; inference reuses the fitted pipeline. |
| 7. Before Session 5 | Preserve files/environment; follow service setup; optional Docker readiness. Do not assign API implementation early. |
| 8. Before Session 6 | GitHub/repository/Actions access and commit/push readiness; tests/workflow are taught later. |
| 9. Later automation | Push → CI runner → tests → optional build. Distinguish this from today's manual training and conceptual CT. |

Deck checks confirmed **33 original slides**. Correct flower-species prose on **13, 25, 26** to SMS ham/spam. Consolidate duplicate topics **23/28** (CT objectives), **24/29** (retraining reasons), **25/26** (training/inference). Original 33 is “Questions?”; there is no Part 5 lab transition. Slide 31's notes explicitly keep CT conceptual.

Revision targets from the slide brief: five parts, **180 minutes = 25 + 40 + 30 + 30 + 55**, roughly **26–28 slides**. Count introductions/readiness within those parts. Map replacements/removals and state the resulting slide count; flag timing/count tradeoffs rather than crowding slides or silently changing exercises. These targets are not timing claims about the current deck.

For each proposed slide, provide title, 15–30 student-facing words, simple visual idea, 2–4 short speaker-note sentences, and original-slide insertion/replacement location. Prefer one idea and at most three short bullets. Keep commands, technical caveats, and troubleshooting in notes. Finish with readiness grouped into today / before Session 5 / before Session 6, fallback notes, and a one-sentence handoff. Request English Markdown content and a placement plan; actual deck/source editing is a separate task.

## Verification

Before consolidation on **2026-11-11**, disposable copies passed **27 synthetic-data checks and 28 official-UCI checks** under Python 3.12.13 with the direct dependency pins used at that time (including scikit-learn 1.8.0). Coverage included ZIP normalization/invalid-input preservation, all four exercise edits, stage order, whole-artifact contents, invalid data stopping before fitting, both gates, rejection without either output, version protection, repeated metrics, and prediction after removing the copied dataset.

The downloaded official ZIP prepared 5,574 rows (4,827 ham / 747 spam). Baseline v1/v3 validation precision **1.0000** and recall **0.7857** matched; these are observed results, not future pass criteria. Slide references above were checked against the actual deck. At that review, student instructions, Python source, dependency pins, and PowerPoint remained unchanged.

On **2026-11-17**, the updated direct pins (pandas 2.2.3, scikit-learn 1.7.2, joblib 1.5.3) installed successfully in a clean Python 3.10.12 environment, and `pip check` passed. Disposable copies of both lab folders passed training, the quality gate, artifact save/load, and prediction using the prepared official UCI CSV. Observed validation precision was **1.0000** and recall **0.7857** in both copies. This compatibility check did not rerun the full historical check suite above.

Further reference: [scikit-learn Pipeline](https://scikit-learn.org/1.7/modules/generated/sklearn.pipeline.Pipeline.html), [data leakage pitfalls](https://scikit-learn.org/1.7/common_pitfalls.html), [model persistence](https://scikit-learn.org/1.7/model_persistence.html), [GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions), [FastAPI first steps](https://fastapi.tiangolo.com/tutorial/first-steps/).
