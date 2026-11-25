# Session 7 — Final QA report

**Result:** Passed the implemented checks and visual review on 21 November 2026.

[Final editable PowerPoint](output/Session7_Monitoring_Maintenance.pptx) · [Slides-only PDF](output/Session7_Monitoring_Maintenance.pdf) · [Part names, objectives and main goals](SESSION7_OVERVIEW.md).

| Part | Slides | Minutes | Hands-on |
| --- | --- | ---: | ---: |
| What should we monitor? | 1–8 | 25 | 10 |
| Drift in SMS messages | 9–19 | 35 | 15 |
| A simple monitoring report | 20–28 | 35 | 25 |
| What happens after an alert? | 29–37 | 30 | 0 |
| Guided lab and recap | 38–45 | 55 | 45 |
| Total | 45 | 180 | 95 |

## Presentation

Five editable opening slides were added at slides 1, 9, 20, 29 and 38. Each displays the part’s exact name, one objective and three main goals. The same outcomes appear in the instructor overview and student README. One minute was transferred from existing teaching time in each part; all lab allocations are preserved.

All 40 original teaching/lab slides retain their student-facing content. Their rendered main content regions are pixel-identical to the previous deck; only the footer numbering changes. The native slides and all 45 embedded Hebrew Notes pages match the current sources. Timing labels and the two explicit slide references in notes were updated.

The final PPTX opened and rendered using LibreOffice Impress 7.3.7.2 with Aptos, Aptos Display, Aptos Mono and Arial resolved as intended. Package CRC/XML relationships, editable text/shapes, source content, slide and part numbering, bounds, overlaps, 10–30-word body budgets, native content fonts, RTL paragraphs, complete rendered text/notes and SVG labels passed. Only the two actual report excerpts are raster pictures; no slide is flattened.

The new openings and their actual Hebrew Notes pages were visually inspected. The original 40 content regions were compared with the previously reviewed deck. All remaining source/render checks passed. Fifteen reusable SVG diagrams and their JSON definitions are retained; duplicate PNG diagram exports are excluded after cleanup.

Evidence: [presentation checks](output/qa/final/checks.json), [rendering environment](output/qa/final/render-environment.json), [visual review](output/qa/final/visual-review.json), [rendered-region comparison](output/qa/final/slide-region-comparison.json), [original slide preservation](output/qa/source-preservation.json).

## Labs and portability

The relocated Lab 2 starter and completed copy were executed and independently verified. Both Lab 3/4 scripts and notebooks were executed using the environment installed from the supplied requirements, with Python 3.10.12, Evidently 0.7.23, pandas 2.2.3, NumPy 2.2.6 and ipykernel 7.3.0. Character counts, URL rules, invalid inputs, argument order, actual report outputs and HTML export passed. The two reporting helpers remain identical.

Lab 3’s ten-message batches are identical to Lab 2: average length 25.4 → 109.0 characters and URL-like share 20% → 80%; Evidently flags both features. Lab 4 has 200 messages per batch, identical length distributions with mean 75.7 characters, and URL-like share 10% → 70%; Evidently flags the URL feature and not length. The focused data generator reproduces the original CSV bytes.

Both relocated HTML reports opened offline with no JavaScript errors, and their actual chart traces match the expected counts. Report screenshots are actual captures. No spam model or raw-text drift classifier is trained; no prediction-quality metrics are computed from unlabeled data.

The student handout contains 37 required files. All 25 relative Markdown links passed. A temporary relocated copy ran the Lab 2 starter/completed copy and Lab 3/4 scripts from a different working directory. Twenty original lab source/data/worksheet/answer files were checked for unchanged hashes. Instructor keys and note-bearing decks are excluded from the handout.

Evidence: [Lab 2 checks](output/qa/labs/lab2-checks.json), [monitoring lab checks](output/qa/labs/checks.json), [student package checks](output/qa/student-package-checks.json), and each monitoring lab’s output/browser-checks.json.

## Organization and cleanup

The root follows Session 6: one README, one instructor folder and one student folder. The instructor folder retains the final presentation and preview, objectives overview, editable sources, lab masters/answers, required reports/data, local style reference, scripts and small QA records. The student folder retains only the exercise files and fallbacks.

Disposable environments, caches, duplicate ZIPs, obsolete standalone part decks, superseded authoring scripts, duplicate student guides/images and generated inspection files were removed. Teaching files were backed up outside the course folder before cleanup. See [organization checks](output/qa/organization-checks.json) for the inventory, retained essentials, removed categories and backup location. The render/check commands in README.md recreate inspection artifacts when needed.

## Verification limits

Microsoft PowerPoint desktop was not available; the actual PPTX was verified with LibreOffice and python-pptx. Other machines may substitute fonts. Student execution was tested on Linux/Python 3.10.12; Windows/macOS commands were not executed on those systems. The 180-minute schedule and lab timings are teaching plans, not measurements from a live class. All incidents and data are synthetic. Technical QA does not imply final instructor sign-off on the teaching content.
