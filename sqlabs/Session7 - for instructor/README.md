# Session 7 — Monitoring & Maintenance

**MLOps Essentials: AI Lifecycle Management** · English slides · Hebrew instructor notes

Open [the final editable PowerPoint](output/Session7_Monitoring_Maintenance.pptx) or [the slides-only PDF](output/Session7_Monitoring_Maintenance.pdf). All 45 slides have embedded Hebrew notes. Each part begins with its name, objective and three main goals.

This is the instructor folder. Distribute the separate [student folder](<../Session7 - for students/>) to the class. Run presentation commands from this instructor folder. See [FILES_GUIDE.md](FILES_GUIDE.md) for file purposes and [SESSION7_OVERVIEW.md](SESSION7_OVERVIEW.md) for each part’s full objectives and goals.

**Schedule:** 180 minutes, including 95 minutes of student hands-on work (52.8%). The five opening slides use existing teaching time; no lab time was reduced. Setup should happen before class; breaks are additional.

| Part | Objective | Slides | Minutes | Hands-on |
| --- | --- | --- | ---: | ---: |
| 1. What should we monitor? | Distinguish service health from prediction quality. | 1–8 | 25 | 10 |
| 2. Drift in SMS messages | Explain changing SMS patterns and their limits. | 9–19 | 35 | 15 |
| 3. A simple monitoring report | Generate and interpret a simple monitoring report. | 20–28 | 35 | 25 |
| 4. What happens after an alert? | Choose a response to a monitoring alert. | 29–37 | 30 | 0 |
| 5. Guided lab and recap | Investigate an SMS incident and justify an action. | 38–45 | 55 | 45 |

## Teaching and lab materials

- [Part objectives and main goals](SESSION7_OVERVIEW.md): the intended outcomes and timing for all five parts.
- [Session plan](planning/SESSION7_PLAN.md): actual slide order and activity timing.
- [Slide sources](slides/): each part’s slides.json is the authoring source; CONTENT.md is the generated English slide text and Hebrew teaching notes.
- [Lab 1 guidance and answers](labs/lab1/INSTRUCTOR_GUIDE_HE.md): six simulated HTTP/prediction records.
- [Lab 2 guidance and answers](labs/lab2/INSTRUCTOR_GUIDE_HE.md): feature comparison and the completed mean calculation.
- [Lab 3 answer key](labs/lab3/instructor/ANSWER_KEY_HE.md): generate a report and interpret one chart.
- [Lab 4 answer key](labs/lab4/instructor/ANSWER_KEY_HE.md): independent incident reasoning and decision guidance.
- [QA report](FINAL_QA_REPORT.md): completed checks and verification limits.

The instructor labs retain the editable masters and expected results. The separate student folder has the handout. Labs 3–4 contain prepared HTML, calculated summaries and a chart for fallback. All SMS and service facts are synthetic; the course uses the existing SMS classifier context without training a model, changing a deployment or using the untouched final test set.

Lab 3 reuses the exact Lab 2 batches: average length 25.4 → 109.0 characters and URL-like share 20% → 80%. Lab 4 uses a distinct incident: URL-like share 10% → 70%, while the full length distribution is unchanged with mean 75.7 characters. Reliable new labels and matching predictions are absent, so prediction quality is unknown and investigation is the initial response.

## Prepare before class

Use Python 3.10 for student execution. Follow the setup in the student guides. Labs 3–4 use the same tested Evidently 0.7.23, pandas 2.2.3, NumPy 2.2.6 and ipykernel 7.3.0 requirements. Prepare packages and report fallbacks before class. No live API, AWS or Docker is required for the labs.

## Edit and rebuild

Create a local build environment and install requirements-presentation.txt. Then run:

```bash
python scripts/build_presentation.py --all
```

Edit slides/partN/slides.json for slide text, notes or timing. slides/manifest.json records part names, objectives, goals and ordering. The builder refreshes CONTENT.md, SVG diagrams, the final PPTX and the small QA slide manifest. Save manual PowerPoint edits before rebuilding. The local style reference is [reference/session6.pptx](reference/session6.pptx); the package does not rely on Session 6’s old directory paths.

Install Aptos, Aptos Display and Aptos Mono for the slides, and Arial for Hebrew notes. Fonts are not bundled.

To synchronize the separate student folder from the explicit student file list:

```bash
python scripts/package_students.py
```

To reproduce only Lab 4’s deterministic synthetic data, run scripts/generate_lab4_data.py, regenerate the lab reports and refresh the student folder. No randomness is used. The notebooks are editable sources; no obsolete notebook-authoring script is retained.

## Optional verification

Install requirements-qa.txt in the presentation environment. With LibreOffice Impress and python3-uno available, run:

```bash
python3 scripts/render_presentation.py --all
python scripts/check_presentation.py --all
```

Rendering uses the system Python that can import UNO; content checks use the presentation environment. These commands recreate temporary PDFs and previews in output/qa/final/. Visually inspect them before recording a new review. The distribution retains only the small QA records; inspection images and PDFs are removed after verification.

The lab checks are scripts/check_lab2.py and scripts/check_monitoring_labs.py. Install requirements-lab-qa.txt in a separate temporary notebook QA environment; use a lab environment installed from labs/lab3/requirements.txt as --lab-python for the monitoring check. The retained requirement files recreate the removed local environments when needed. scripts/capture_reports.cjs optionally regenerates real report screenshots using Playwright; its browser and module installation belong outside the teaching package. See [the verified API usage](reference/EVIDENTLY_API.md).
