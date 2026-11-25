# Lab 3 — Generate and Interpret a Monitoring Report

**25 minutes.** Generate an Evidently report, explain one chart, and name the evidence still needed to assess prediction quality. All messages are synthetic. These CSVs are byte-for-byte copies of Lab 2; there are no labels or model predictions. No training, live API, Docker or AWS is needed.

Prepare Python 3.10–3.11 and the environment before class. The tested setup is Python 3.10.12 with Evidently 0.7.23, pandas 2.2.3 and NumPy 2.2.6. Later Python versions and other operating systems have not been executed here. Use a separate environment from Session 6's saved model.

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

You can instead open [monitoring_report.ipynb](monitoring_report.ipynb) in your existing notebook editor, select this environment's Python kernel and run its short cells in order. Keep the notebook working directory in this lab folder. The complete companion script produces the same files.

1. **Load and inspect — 5 minutes.** Open the two files in [data/](data/). Run the loading cells. `message_length` counts characters, including stored spaces and punctuation. `has_url` is categorical `yes`/`no`, using the same lowercased substring check as Lab 2: `http://`, `https://` or `www.`. It is approximate and is not a spam label.
2. **Generate — 10 minutes.** Run the supplied report code. Open [output/monitoring_report.html](output/monitoring_report.html) in a browser. Expand the `has_url` row using its left arrow. Read the current/reference legend and compare the bars over `yes`. The code passes current first and reference second; only the two derived features enter Evidently.
3. **Interpret — 7 minutes.** Complete [WORKSHEET.md](WORKSHEET.md). Explain one observed change using a count or chart. A tool warning describes changed feature distributions; it does not measure accuracy.
4. **Next evidence — 3 minutes.** Suggest what to inspect next and what matching predictions and reliable labels would add. Share one sentence with the class.

Submit your worksheet and the generated or inspected HTML report. A short evidence-based answer is sufficient. Keep raw messages out of production monitoring logs; these public classroom examples are synthetic.

If setup takes more than a few minutes, use the prepared [HTML](output/monitoring_report.html), [chart](output/url_distribution.png) and [calculated summary](output/FEATURE_SUMMARY.md). Complete the same questions and mark the report as “prepared report inspected.” There is no need to debug installation during the lab.

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md). The provided helper [monitoring.py](monitoring.py) contains the short feature and report implementation; there is no Python completion exercise in this lab.
