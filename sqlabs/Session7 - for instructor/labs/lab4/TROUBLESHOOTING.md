# Lab 4 — Troubleshooting

Use the same environment as Lab 3. If an import fails, select that environment's kernel or install this folder's requirements.txt into a fresh environment. The tested package is Evidently 0.7.23; do not use legacy report imports.

Keep data/reference_sms.csv and data/current_sms.csv inside this lab folder. Run notebook cells from this directory; run_report.py resolves its own folder and works from elsewhere. Wrong schemas, empty batches, duplicate/empty IDs and blank messages produce an explicit input error; restore the supplied files rather than silently filling missing data.

Open output/monitoring_report.html in a browser and click the arrow beside a feature. Read the legend, not just colors. If browser or package setup fails, use output/FEATURE_SUMMARY.md and output/url_distribution.png. Complete the same decision worksheet and mark “prepared report inspected.” Move to the fallback after a few minutes of setup trouble.
