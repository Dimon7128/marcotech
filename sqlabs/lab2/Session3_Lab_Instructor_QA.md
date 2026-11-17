
# Session 3 — Instructor preparation and Q&A

Short answers to students' questions, in notebook order. Numbers are from the default run (seed 42).

## Before class — highest-return preparations

- **Rehearse in a fresh student runtime.** Restart and run the core notebook top to bottom with the defaults; keep `RUN_FINAL_TEST=False`. Confirm both run records, the save/reload checks, and the final ZIP. Keep your executed notebook as a reference rather than relying on remembered numbers.
- **Have the two recovery paths ready.** Keep the extracted UCI `SMSSpamCollection` file available for upload if the download fails. Rehearse the CSV + joblib fallback with `SESSION3_SKIP_MLFLOW_INSTALL=1` set before Step 0 in a runtime without MLflow. That flag skips installation; it does not disable an already installed MLflow. Confirm you can finish and export without tracking.
- **Prepare one mistake-count explanation and one surprising SMS.** Use Run A: 96 spam caught, 32 missed, 0 false alarms. Precision = `96 / (96 + 0)`; recall = `96 / (96 + 32)`. Try the synthetic messages beforehand and keep one unexpected prediction to explain using Step 7's known/ignored words, rather than improvising a phrase that must be classified correctly.
- **Protect time for the handoff.** Treat Steps 8 and 10 as optional; finish selection, save/reload, and Step 9 export first. Open your reference ZIP and check its four required files. Ask students to explain their choice in their own words: `AUTO` and the default reason can pass the notebook assertions without demonstrating understanding.


## Step 1 — Inspect the SMS dataset

### Why is spam recall important when spam messages are less common?
**Answer:** Recall is the share of real spam the model catches. When spam is rare, accuracy hides misses, because guessing "ham" every time is already right most of the time.
**In this lab:** "Always ham" is 87.6% accurate but catches 0% of spam. Run A catches 96 of the 128 validation spam (96 ÷ 128 = 0.750).

## Step 2 — Split once and keep the test set locked

### What does `random_state=42` mean?
**Answer:** The split shuffles the messages randomly. `random_state` fixes that shuffle, so the same messages land in train, validation and test on every run. Any whole number works; 42 is just a convention.
**In this lab:** Run A and Run B are compared on identical data, and students get the same numbers as the instructor.

### Why remove duplicates before splitting, and fit TF-IDF only on training data?
**Answer:** A repeated SMS in both training and validation lets the model be tested on a message it already saw. Fitting TF-IDF on all messages also leaks information: the vocabulary and word weights would include validation and test text, even without their labels.
**In this lab:** Remove duplicate texts first, then split. The pipeline's `fit(X_train, y_train)` learns both TF-IDF and the classifier from training only; `predict(X_val)` reuses them without fitting again.

## Step 3 — Train Run A

### What does the MLflow warning "Model logged without a signature and input example" mean?
**Answer:** It is a harmless notice. A *signature* describes what the model takes in and gives out (here: text in, `ham`/`spam` out). An *input example* is a sample input saved with the model. The lab does not pass `input_example`, so MLflow cannot record either. The model is still logged and works.
**In this lab:** Ignore it. The metrics and the saved pipeline are not affected, and it should appear again for Run B. In real projects you add an `input_example` so the signature is saved and inputs can be checked later.

## Step 4 — Train Run B

### What does `alpha` change? Does a larger value mean a better model?
**Answer:** `alpha` controls smoothing: it adds a small amount to each feature's class count so a feature absent from one class does not get zero probability there. Larger values soften the influence of sparse evidence; they do not guarantee better precision or recall.
**In this lab:** Only `alpha` changes: 0.5 → 1.0. Run B catches 81 spam instead of 96, with no false alarms in either run. Say “this change hurt recall on our validation set,” not “larger alpha always hurts recall.”

## Step 6 — Choose a candidate

### Precision is 1.000 — does that mean the model makes no mistakes?
**Answer:** It means every message it flagged as spam in this validation run was spam. It says nothing about the spam it failed to flag, and it does not guarantee zero false alarms on future messages.
**In this lab:** Run A still misses 32 of 128 spam messages. Its perfect precision is based on 96 spam alerts, not proof that automatic blocking is safe in production.


### Would a review folder change your pick?
**Answer:** It depends on what a mistake costs. With automatic blocking, a false alarm deletes a real message, so precision comes first. With a review folder, a person checks flagged messages, so a false alarm is only a delay and recall comes first.
**In this lab:** With the core Runs A and B, no: Run A wins both goals (precision tied at 1.000, recall 0.750 vs 0.633). In the bonus Step 10, yes: Run A wins for blocking (0 real messages blocked, 32 spam delivered) and Run C wins for a review folder (13 real messages held for review, 8 spam delivered).

## Step 7 — Save, reload and test custom SMS

### Why save the whole pipeline instead of just the classifier?
**Answer:** The classifier expects numbers in the exact feature order learned during training. The fitted TF-IDF stage supplies that vocabulary, order and weighting. A newly fitted vectorizer can produce different features even with the same settings.
**In this lab:** Save and reload `selected_pipeline.joblib`, then call `predict()` on raw SMS strings. The checks confirm both fitted stages are present; manually rebuilding a vectorizer is unnecessary.

### My obvious spam was called ham. Is the notebook broken? Is the spam score a confidence guarantee?
**Answer:** A surprising prediction alone does not mean the code is broken. This model uses learned word patterns, not human understanding; unfamiliar wording may provide little evidence. Its spam score is a model estimate, not a verified probability of being correct.
**In this lab:** Inspect “Known words used” and the known/ignored-word table. Unknown words contribute no TF-IDF features. Use your custom SMS to explain a limitation; use the fixed validation set to compare models.

## Step 9 — Final verification and export

### What if the final test score is worse — can we switch to Run B?
**Answer:** Report the result for the frozen candidate. Switching or tuning based on test performance makes that test set part of model selection, so it no longer provides an independent final check. Further development would need a fresh independent evaluation.
**In this lab:** Keep `RUN_FINAL_TEST=False` unless you allow the final check after selection. If enabled, evaluate the selected model once and keep the original selection reason; do not test both runs to find a winner.

## Step 10 — Optional bonus (Run C)

### What does `fit_prior` do, and why is `True` the default?
**Answer:** It sets the model's starting belief before it reads any word. `True` learns that belief from the training data: about 7 ham for every spam (2,710 vs 386), so spam needs strong word evidence. `False` starts at 50/50, so the words alone decide: more spam is caught, with more false alarms. `True` is the default because learning base rates from the data is the standard Bayesian approach and tends to give the best overall accuracy when the training mix matches real traffic.
**In this lab:** Runs A and B never set it, so the default applies. Run C sets `fit_prior=False`: precision falls from 1.000 to 0.902 and recall rises from 0.750 to 0.938.
