# Lab 4 — Monitoring Incident Challenge

**45 minutes, individual investigation.** Read [INCIDENT.md](INCIDENT.md), inspect the evidence and recommend an action. Use optional peer discussion after writing your own conclusion. All SMS and operational facts are synthetic. No real messages, held-out test data, labels or model predictions are included.

Use the same Python environment and pinned reporting API as Lab 3. Prepare it before class. The tested setup is Python 3.10.12, Evidently 0.7.23, pandas 2.2.3 and NumPy 2.2.6. No model training, live API, AWS or Docker is needed.

Windows PowerShell, from this lab folder:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_report.py
```

macOS/Linux, from this lab folder:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_report.py
```

Alternatively, open [monitoring_incident.ipynb](monitoring_incident.ipynb), select the environment's Python kernel and run from this lab directory. The supplied script and notebook are complete: spend your time interpreting evidence.

| Stage | Time | Your task |
| --- | ---: | --- |
| Understand | 5 min | Read the incident. Separate what works, the warning, and unknowns. |
| Inspect | 10 min | Load both CSVs in data/. Compare message count, average character length and URL-like share. |
| Generate | 10 min | Run the supplied report and open output/monitoring_report.html. Expand relevant feature rows. |
| Interpret | 10 min | Explain the main change. Assess whether it proves worse predictions; consider sampling or processing issues and missing evidence. |
| Decide | 10 min | Complete submission_template.md in approximately 3–5 sentences. Choose an action and a concrete next step. |

The two monitoring features use exactly the Lab 2/3 definitions: stored character count and case-insensitive substring detection for `http://`, `https://` or `www.`. Evidently receives only `message_length` (numerical) and `has_url` (`yes`/`no`, categorical), with current first and reference second. A URL-like message is not automatically spam.

This incident differs from Lab 3. Inspect each feature; do not copy the earlier interpretation. The 200-message batches are deterministically generated paired notification templates. Equal-length link and printed-handout phrases deliberately hold the length distribution constant while URL frequency changes. This teaching construction does not describe a real SMS population. Generator: scripts/generate_lab4_data.py in the instructor project; no randomness is used.

Submit **one generated or inspected report** and your completed [submission_template.md](submission_template.md). Choose among keep monitoring, investigate further or consider retraining, and justify your decision from the available evidence. If proposing retraining, explain the quality evidence and evaluation needed before release; do not train anything here.

If installation fails, inspect the prepared [HTML report](output/monitoring_report.html), [feature summary](output/FEATURE_SUMMARY.md) and [chart](output/url_distribution.png). Mark “prepared report inspected” in your submission and complete the same reasoning task. Try [HINTS.md](HINTS.md) one hint at a time. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for brief fixes.
