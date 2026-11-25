# Session 4 — Repeatable SMS Training Pipeline

This is the **student project** for MLOps Essentials, Session 4, Part 5.

**Start here:** `STUDENT_LAB.md` for numbered exercises and reflection questions.

## What each file is for

| File or folder | Purpose / when to open it |
|---|---|
| `README.md` | Start here for setup and this project map. |
| `STUDENT_LAB.md` | Follow the numbered exercises, commands, checks, and reflection questions. |
| [INSTRUCTOR_README.md](INSTRUCTOR_README.md) | Single instructor guide: preparation, stage explanations, exercise solutions, troubleshooting, handoff, and slide-update brief. |
| `requirements.txt` | Pinned Python dependencies; install these during setup. |
| `prepare_data.py` | Download the official UCI dataset or read a local ZIP, then create `data/sms.csv`. |
| `inspect_data.py` | Inspect columns, missing values, and class balance; edit for Exercise 1. |
| `train.py` | Check data, split, train, evaluate, apply quality gates, and save; edit for Exercises 2 and 4 and the optional recall gate. |
| `make_bad_data.py` | Create a broken dataset copy to practice diagnosing input failures; edit for Exercise 3. |
| `compare_runs.py` | Print saved validation metrics for two model versions to check repeatability. |
| `predict.py` | Load a saved fitted pipeline and classify a synthetic SMS without retraining. |
| `data/` | Generated input files: `sms.csv` and the exercise copy `sms_broken.csv`. |
| `models/` | Generated outputs: `sms_model_<version>.joblib` and its matching `metrics_<version>.json`. |

**Connection to Session 3:** Both labs use the UCI SMS Spam Collection. Session 3 removes duplicate message texts and uses approximately 60%/20%/20% train/validation/test splits. This lab's preparation script preserves duplicate messages, and training uses approximately 70%/15%/15% splits. The source dataset is the same, but the prepared rows and splits can differ, so do not expect matching metrics. This lab trains a new pipeline from the CSV rather than loading Session 3's saved model.

**Quick setup:**

**Python 3.10 or newer is required.** Check `python3 --version` before creating
the environment. The pinned scikit-learn 1.7.2 supports Python 3.10. Activate the
environment before installing dependencies and running the lab scripts.

```bash
python3 -m venv .venv
# Activate your environment: Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 prepare_data.py
```

If the UCI download fails, download the official ZIP in your browser and use
`python3 prepare_data.py --zip "path/to/official.zip"`.
If you already have the original normalized `text,label` dataset from earlier sessions,
place it at `data/sms.csv` instead. Keep any original copy.

**Important:** The official dataset is not bundled in this ZIP. Use UCI's original SMS Spam Collection (5,574 examples; CC BY 4.0): https://archive.ics.uci.edu/dataset/228/sms+spam+collection. Credit: Almeida & Hidalgo (2011), DOI: 10.24432/C5CC84.

**Privacy/security:** Only use synthetic messages for custom inference. Do not publish real private SMS or load untrusted `.joblib` files. The test split is not used in this session to choose a model.
