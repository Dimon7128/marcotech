# Session 6 — Final QA Report

**Reviewed:** 20 November 2026.  
**Folder reorganization checked:** 21 November 2026.  
**Deliverable:** [output/session6.pptx](output/session6.pptx).  
**Result:** Local presentation and lab checks **PASS**. Hosted GitHub Actions and Microsoft PowerPoint desktop checks are **NOT VERIFIED**, as detailed below.

## Presentation

| Part | Slides | Count | Minutes |
| --- | --- | ---: | ---: |
| 1 — CI/CD in an ML Project | 1–7 | 7 | 25 |
| 2 — Essential Tests | 8–17 | 10 | 40 |
| 3 — GitHub Actions Basics | 18–26 | 9 | 50 |
| 4 — From CI Result to a Release | 27–32 | 6 | 30 |
| 5 — Independent CI Challenge & Recap | 33–39 | 7 | 60 |
| Total | 1–39 | 39 | 205 |

- **PASS — Source preservation.** The 32 pre-existing English titles and student text blocks from Parts 1–4 match the saved earlier drafts exactly. Part 5 was completed from the supplied brief with explicit instructor authorization. No earlier part-specific PPTX files were available; the five Markdown sources were used for assembly.
- **PASS — Timing reconciliation.** The final request's 40-minute Part 2 replaces its earlier 45-minute estimate. Explanation/demo now takes 15 minutes; the complete 25-minute exercise and English slide text are preserved. Other part allocations remain intact.
- **PASS — Editability.** Native PowerPoint text boxes, shapes, groups and connectors throughout; editable YAML/code text; no embedded raster slide images. All package XML and internal relationships validate, and the saved deck reopens with python-pptx and LibreOffice.
- **PASS — Speaker notes.** **39/39** slides have substantive Hebrew notes embedded in `ppt/notesSlides/notesSlideN.xml`, with right-to-left paragraphs and English technical terms preserved. Their complete text and paragraph order match the Markdown after formatting is removed. All 39 actual Notes pages were rendered. Sampled Hebrew pages, including the longest note and lab guidance, were visually inspected. No rendered text extends beyond a Notes page.
- **PASS — Visual review.** All 39 slides rendered and reviewed using LibreOffice Impress 7.3.7 with Aptos/Aptos Display/Aptos Mono and Arial available. Rendered slide text matches the Markdown exactly after whitespace normalization. No text lies outside a slide; no blank, duplicated, overlapping or cut-off slides found. A wrapped dependency label, inherited shape shadows and the longest Notes-page layout were corrected.
- **PASS — Typography and diagrams.** Consistent 16:9 proportions, white backgrounds, dark text and restrained reference green. Slide bodies contain 12–29 words, excluding titles and slide numbers. Student text is 24–40 pt; slide numbers are 13 pt. Hebrew notes use Arial 11–12 pt. Five reusable SVGs were parsed, rendered and visually inspected; all contain vector shapes and text with no linked images.
- **PASS — Teaching continuity.** One SMS project throughout. API correctness remains distinct from model precision/recall. CI checks changes, CD concerns releases, CT concerns retraining. Part 4 is a future release scenario; no publishing, deployment, AWS lab or training was added. Brief reminders connect parts; no accidental duplicate slides were found.

Inspection evidence: [machine-readable checks](output/qa/presentation-checks.json), [slide manifest](output/qa/slide-manifest.json), and [English preservation audit](output/qa/source-preservation.json). The rendered previews/PDFs were inspected during the original validation and removed during the 21 November 2026 cleanup. The small JSON evidence records are retained; the instructor README explains how to recreate inspection files.

## Hands-on materials

| Activity | Student implementation minutes |
| --- | ---: |
| Guided Lab 1, Part 2 — API tests and schema boundary | 25 |
| Guided Lab 1, Part 3 — repository, workflow and result inspection | 35 |
| Lab 2, Part 5 — independent CI challenge | 47 |
| Total | 107 of 205 (52.2%) |

- **PASS — Guided lab.** An eight-file starter includes the trusted saved model, API, declared runtime/dev dependencies, three starter tests, lowercase `dockerfile` and hidden ignore files. The one deliberate TODO and absence of the new maximum are documented. The guided solution has five tests and the 500-character policy. Windows PowerShell and macOS/Linux setup, expected results, troubleshooting, repository creation and Hebrew teaching guidance are supplied.
- **PASS — Progression.** Part 3 continues from the completed Part 2 files in each student's own repository. Workflow starter and complete reference are under `labs/lab1/workflows/`; no active course-root workflow was installed.
- **PASS — Independent challenge.** `labs/final-lab/CHALLENGE.md` offers three missions with goals, acceptance criteria and a short evidence report. It has no complete implementation or numbered coding recipe. Hebrew `INSTRUCTOR_GUIDE.md` separately supplies reference solutions, common mistakes, three hint levels per path, support guidance and debrief questions. API-policy changes are limited to the selected mission.
- **PASS — Access fallback.** Local pytest/Docker checks and an offline workflow-inspection guide are supplied. Example hosted logs are explicitly illustrative. Local evidence cannot substitute for an actual PR-event run in mission C; missing hosted evidence is recorded honestly.

## Executed technical checks

The reference cases ran in an isolated Docker environment using **Python 3.10.22**, pytest 8.4.2, HTTPX 0.28.1, FastAPI 0.128.2, Pydantic 2.14.3, Starlette 0.50.0, scikit-learn 1.7.2, joblib 1.5.3 and pandas 2.2.3. Dependency files preserve the previous runtime pins. These were local copied-file/container checks, not a GitHub checkout or hosted run.

| Case actually executed | Observed result | Status |
| --- | --- | --- |
| Distributed starter, including its deliberate TODO | 1 failed, 2 passed | PASS: expected exercise state |
| Completed tests before adding the maximum length | 1 failed, 4 passed | PASS: new boundary detects missing rule |
| Completed guided solution | 5 passed | PASS |
| Deliberate health assertion of 201 | 1 failed, 4 passed | PASS: expected detection |
| A: extra-field test before new policy | 1 failed, 5 passed | PASS: expected detection |
| A: reference policy and test | 6 passed | PASS |
| B: header check against correct response | 6 passed | PASS |
| B: wrong media type with the new check | 1 failed, 5 passed | PASS: expected detection |
| B: same wrong media type with baseline checks only | 5 passed | PASS: demonstrates the original gap |
| B: valid JSON media type with charset parameter | 6 passed | PASS |

Each run also emitted one dependency deprecation warning from Starlette's use of an AnyIO alias; it did not affect results. No warnings were hidden.

- **PASS — Schema probes.** Ten additional requests confirmed missing, null, numeric, empty and whitespace-only rejection; valid prediction; 500 accepted/501 rejected; and the same boundaries after surrounding spaces are trimmed.
- **PASS — Model handoff.** The loaded artifact has `TfidfVectorizer` and `MultinomialNB` steps with `ham`/`spam` classes. The distributed model's SHA-256 matches the original artifact: `265bd0ba388c1e7ba3c827593d15dda611ea1b57696668658f311fd8c83326b0`. No model training was executed.
- **PASS — Docker build.** Built the completed service using the supplied lowercase `dockerfile`, original `.dockerignore`, runtime requirements and saved model, tagged locally `sms-api:session6-qa`. The build uses the same command structure/context as the lab; the tag distinguishes QA. The Dockerfile copies the required API/model files and needs no dataset.
- **PASS — Runtime HTTP.** Started that image temporarily with Uvicorn and made five real HTTP requests inside the container: health 200, valid prediction 200 with an allowed label, 500 characters accepted, 501 rejected with 422, and whitespace-only input rejected with 422. Removed the temporary container afterward. This was a local runtime check, not deployment or hosted CI.

Actual outputs: [pytest and schema results](output/qa/technical/lab-test-results.json), [container HTTP results](output/qa/technical/docker-smoke-results.json).

## Workflow and official reference checks

- **PASS — Static YAML.** Verified `on: [push]`, read-only contents permission, one Ubuntu job, checkout, Python 3.10 setup, dependency install, pytest, and Docker build in that order. No override hides test failures. The student's destination is `.github/workflows/ci.yml` with application files at repository root. Mission C's reference retains that job and adds `pull_request`.
- **PASS — Current reference inspection.** The pinned [checkout v7.0.1 manifest](https://raw.githubusercontent.com/actions/checkout/v7.0.1/action.yml) and [setup-python v7.1.0 manifest](https://raw.githubusercontent.com/actions/setup-python/v7.1.0/action.yml) use Node 24. GitHub's [Python versions manifest](https://raw.githubusercontent.com/actions/python-versions/main/versions-manifest.json) lists Python 3.10.22 Linux x64 builds for Ubuntu 24.04 and 26.04. Both current [24.04](https://raw.githubusercontent.com/actions/runner-images/main/images/ubuntu/Ubuntu2404-Readme.md) and [26.04](https://raw.githubusercontent.com/actions/runner-images/main/images/ubuntu/Ubuntu2604-Readme.md) runner inventories list Docker client/server. No fixed OS version is assumed for `ubuntu-latest`.
- **NOT VERIFIED — Hosted execution.** No actual GitHub Actions push/PR run was created or observed. Checkout, hosted Python setup, runner-specific installation and skipped-build behavior are statically reviewed, not reported as executed. Prepare and inspect real failed/passing demonstration runs before teaching; the supplied offline summaries remain illustrative.

Reference-inspection record: [workflow reference checks](output/qa/technical/workflow-reference-checks.json). API/schema explanations were checked against the project and official [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/), [Pydantic configuration](https://pydantic.dev/docs/validation/latest/api/pydantic/config/) and [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) documentation.

## Remaining verification

- **NOT VERIFIED — Microsoft PowerPoint desktop.** The deck was reopened and rendered with LibreOffice and its package verified programmatically. A manual open/edit check in Microsoft PowerPoint itself was not performed. Aptos fonts are not embedded; installation and regeneration instructions are in [README.md](README.md).
- **NOT VERIFIED — Student machines and accounts.** Windows/macOS commands were reviewed; those platforms and each student's GitHub access were not exercised here. Complete the supplied prerequisite checks before class.

No outstanding local slide-layout, embedded-notes, starter-code or reference-test defects were found. Hosted-run evidence remains a teaching-preparation task, with the fallback available if access is unavailable.

## Instructor/student folder organization — 21 November 2026

- **PASS — Distribution.** The course root contains only a short README and the two role folders. The student handout retains its original 11 files, byte-for-byte unchanged.
- **PASS — Instructor demo.** `labs/lab1/solutions/` now includes all eight required project files. Its five API tests were rerun in the existing isolated test container: **5 passed, 1 dependency deprecation warning**.
- **PASS — Presentation preservation.** The production PPTX is byte-for-byte unchanged. All 39 English slide text blocks and 39 embedded Hebrew notes still match their Markdown sources.
- **PASS — Regeneration.** The relocated generation source was run with output directed to a temporary folder. All 39 regenerated slide XML parts and 39 Notes XML parts were identical to the production deck. Relative Markdown links resolve after relocation.
- **PASS — Cleanup.** Removed the old duplicate starter, local presentation environment, Python caches and reproducible inspection images/PDFs. Preserved the presentation, model artifacts, all five Markdown sources, five SVGs, reference/theme input, generation scripts, lab references/solutions and six small JSON QA records. Expanded lab guides are labeled as instructor references; distribute the separate student handout.

This reorganization check did not repeat hosted CI or Microsoft PowerPoint desktop validation. The previous verification limits above still apply.
