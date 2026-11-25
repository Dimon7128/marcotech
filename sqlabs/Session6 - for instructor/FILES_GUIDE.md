# Session 6 — Which files are for whom?

**Give students only [Session6 - for students/](<../Session6 - for students>).** It contains 11 files: three short guides and the eight-file starter project. Its [README](<../Session6 - for students/README.md>) explains every student file and the required tools.

Students work in their own copy of `sms-service/`, outside another Git repository. They need Python 3.10, Git, a code editor, Internet access and a GitHub account. Local Docker is optional for the normal online lab. During Lab 1 they create their own repository and `.github/workflows/ci.yml`; Lab 2 continues from that completed project.

## Main instructor files

| Path | Purpose |
| --- | --- |
| `README.md` | Course index, timing and regeneration instructions. |
| `SESSION6_MASTER_SPEC.md` | Course requirements and agreed teaching decisions. |
| `FINAL_QA_REPORT.md` | What was checked, results and verification limits. |
| `FILES_GUIDE.md` | This distribution and file guide. |
| `output/session6.pptx` | The complete presentation, including Hebrew instructor Notes. |
| `reference/reference.pptx` | Previous-session presentation used for visual style. |
| `requirements-presentation.txt` | Python dependencies for building the presentation. |
| `requirements-qa.txt` | Extra dependencies for presentation checks and previews. |
| `.gitignore` | Excludes local presentation environment/cache files from Git. |
| `output/qa/` | Small JSON validation records; generated PDFs/images were removed and can be recreated. |

## Editable slide sources

| File | Purpose |
| --- | --- |
| `content/part1.md` | CI/CD/CT introduction; English slide text and Hebrew notes. |
| `content/part2.md` | API testing and schema validation; slide text and notes. |
| `content/part3.md` | GitHub Actions; slide text and notes. |
| `content/part4.md` | Controlled release concepts; slide text and notes. |
| `content/part5.md` | Independent challenge and recap; slide text and notes. |

## Lab source and instructor materials

These originals remain available for teaching and maintenance. The separate student folder provides a smaller handout.

| Path | Purpose |
| --- | --- |
| `../Session6 - for students/sms-service/` | Student starter. Its eight files are explained in the student README; the old duplicate starter was removed from the instructor materials. |
| `labs/lab1/part2_api_testing.md` | Expanded guided API-testing instructions. |
| `labs/lab1/part3_github_actions.md` | Expanded guided repository/workflow instructions and reference YAML. |
| `labs/lab1/part3_offline_inspection.md` | Optional offline log-reading exercise. |
| `labs/lab1/instructor_notes_he.md` | Hebrew API-testing guidance and completed tests. |
| `labs/lab1/part3_instructor_notes_he.md` | Hebrew CI teaching and demonstration guidance. |
| `labs/lab1/solutions/main.py` | Completed guided API with the 500-character rule. |
| `labs/lab1/solutions/test_api.py` | Five completed guided tests. |
| `labs/lab1/solutions/model.joblib` | Saved fitted model for the runnable instructor demo. |
| `labs/lab1/solutions/requirements.txt` | Demo runtime dependency versions. |
| `labs/lab1/solutions/requirements-dev.txt` | Demo runtime and test packages; use for local setup. |
| `labs/lab1/solutions/dockerfile` | Builds the completed demonstration API. |
| `labs/lab1/solutions/.dockerignore` | Keeps the demo build context limited to runtime files. |
| `labs/lab1/solutions/.gitignore` | Excludes the demo's local environment and caches from Git. |
| `labs/lab1/workflows/ci-starter.yml` | Workflow exercise with TODOs. |
| `labs/lab1/workflows/ci-complete.yml` | Complete reference workflow. |
| `labs/final-lab/CHALLENGE.md` | Expanded independent student challenge brief. |
| `labs/final-lab/INSTRUCTOR_GUIDE.md` | Hebrew solutions, progressive hints and debrief guidance. |
| `labs/final-lab/solutions/option_a_main.py` | Reference API policy for rejecting extra fields. |
| `labs/final-lab/solutions/option_a_check.py` | Reference test for unexpected fields. |
| `labs/final-lab/solutions/option_b_check.py` | Reference response-media-type test. |
| `labs/final-lab/solutions/option_c_ci.yml` | Reference workflow checking pushes and pull requests. |

Keep the instructor guides, solutions and the presentation's instructor Notes out of the student handout.

## Presentation scripts and diagrams

| File | Purpose |
| --- | --- |
| `scripts/build_presentation.py` | Regenerates the editable PPTX and SVGs from Markdown. |
| `scripts/check_presentation.py` | Checks deck/source consistency, rendered PDFs, notes and workflow structure. |
| `scripts/export_notes.py` | Exports the actual Notes pages with LibreOffice for inspection. |
| `assets/diagrams/ci-cd-ct.svg` | Reusable CI/CD/CT comparison. |
| `assets/diagrams/part1-ci-pipeline.svg` | Reusable introductory CI pipeline. |
| `assets/diagrams/part3-ci-workflow.svg` | Reusable GitHub Actions workflow diagram. |
| `assets/diagrams/part4-application-versions.svg` | Reusable application-version diagram. |
| `assets/diagrams/part4-release-workflow.svg` | Reusable future release process. |
