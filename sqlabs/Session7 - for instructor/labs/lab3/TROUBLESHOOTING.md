# Lab 3 — Troubleshooting

| Problem | Action |
| --- | --- |
| `ModuleNotFoundError` | Use the Python environment where you installed requirements.txt; select the same kernel in the notebook. |
| CSV missing | Keep data/reference_sms.csv and data/current_sms.csv beside the notebook's folder. Run the notebook from this lab directory. The companion script works from any working directory. |
| Empty/invalid data | Restore the supplied CSV. The loader reports wrong columns, empty batches, duplicate/empty IDs and empty messages explicitly. Do not silently fill missing messages. |
| Report is not visible in the notebook | Open output/monitoring_report.html in a browser; no live server is required. |
| Chart is hidden | Click the arrow at the left of the has_url row. Read the `current` and `reference` legend; the `yes` bars count URL-like messages. |
| API/import differs | Use the pinned Evidently 0.7.23 requirements in a fresh environment. Do not mix legacy `evidently.report` examples with this lab. |
| Installation/browser fails | Open output/FEATURE_SUMMARY.md and output/url_distribution.png, then answer the same questions. |

Setup belongs before class. After a few minutes of trouble, move to the prepared report rather than spending the exercise on installation.
