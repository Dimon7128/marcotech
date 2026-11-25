# Evidently API used in Session 7

Verified 21 November 2026 against the installed **Evidently 0.7.23** package and official documentation:

- [Quickstart: Data and ML checks](https://docs.evidentlyai.com/quickstart_ml)
- [Data drift explanation](https://docs.evidentlyai.com/metrics/explainer_drift)
- [Data definition](https://docs.evidentlyai.com/docs/library/data_definition)
- [Output formats](https://docs.evidentlyai.com/docs/library/output_formats)

The labs import Dataset, DataDefinition and Report from evidently, and DataDriftPreset from evidently.presets. They explicitly declare message_length as numerical and has_url as categorical, convert both feature frames using Dataset.from_pandas, and call Report([DataDriftPreset()]).run(current, reference). The returned Snapshot exports with save_html and save_json. Both scripts and notebooks executed successfully with these calls.

Only the two derived columns are evaluated. Raw SMS text is excluded, so no text drift classifier is trained. Default comparison behavior is retained; the lesson does not teach statistical tests or tune thresholds. The actual tool UI may display those details, but slides focus on changed distributions and evidence limits. A drift result does not measure prediction quality without matching predictions and reliable labels.

See output/qa/labs/checks.json and each lab's output/browser-checks.json for actual execution, input checks, offline browser validation and chart counts. The tested dependency versions are pinned in each lab's requirements.txt. Core package versions and execution evidence are recorded in the retained QA JSON; the dependency list is not a cross-platform installation lock.
