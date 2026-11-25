# Session 6 — CI/CD for Machine Learning

**MLOps Essentials: AI Lifecycle Management** · English slides · Hebrew instructor notes

Open [the editable PowerPoint](output/session6.pptx). All 39 slides use native text, shapes, and connectors; the instructor notes are embedded in the actual Notes section. The design follows Session 5's reference identity.

This is the instructor folder. Distribute the separate [student folder](<../Session6 - for students/>) to the class. Run presentation-generation commands from this instructor folder.

For a short explanation of the project files and what to distribute, see [FILES_GUIDE.md](FILES_GUIDE.md).

The final plan is **205 effective minutes**, including **107 minutes of student hands-on work (52.2%)**: 25 minutes in Part 2, 35 in Part 3, and 47 in Part 5. Breaks are additional. Keep the independent challenge if practical work needs an extension.

| Part | Slides | Minutes |
| --- | --- | ---: |
| CI/CD in an ML Project | 1–7 | 25 |
| Essential Tests | 8–17 | 40 |
| GitHub Actions Basics | 18–26 | 50 |
| From CI Result to a Release | 27–32 | 30 |
| Independent CI Challenge & Recap | 33–39 | 60 |

## Teaching files

- [Master specification](SESSION6_MASTER_SPEC.md): scope and confirmed decisions.
- [Markdown sources](content): exact English text, Hebrew notes, layouts and timing for all five parts.
- [QA report](FINAL_QA_REPORT.md): executed tests, visual checks, and verification limits.
- [Reusable SVG diagrams](assets/diagrams): five diagrams with editable vector text; the PPTX versions use native PowerPoint shapes.
- `output/qa/`: small JSON records of completed checks. Generated inspection PDFs and preview images were removed during cleanup; the QA commands below recreate them when needed.

## Student handout

Distribute only **[Session6 - for students/](<../Session6 - for students>)**, a self-contained handout with 11 files:

- [Start here and file guide](<../Session6 - for students/README.md>).
- [Lab 1: guided tests and CI](<../Session6 - for students/LAB1.md>).
- [Lab 2: independent challenge](<../Session6 - for students/LAB2.md>).
- `sms-service/`: the eight original starter files, including the saved model and both hidden ignore files.

Students work in their own copy outside another Git repository. They need Python 3.10, Git, a code editor, Internet access and normal GitHub sign-in/push access. They create their own repository during Lab 1 and continue from it in Lab 2. Both Windows PowerShell and macOS/Linux setup commands are included. Local Docker is optional for the normal online path.

The starter's label-assertion TODO and missing maximum length are intentional exercise tasks. The minimal handout contains no instructor notes, solutions, presentation tools or build environment. The original expanded guides remain under `labs/` for instructor use and maintenance.

## Instructor files

- [Guided API testing notes](labs/lab1/instructor_notes_he.md).
- [Guided CI notes](labs/lab1/part3_instructor_notes_he.md).
- [Completed guided project](labs/lab1/solutions/): a complete eight-file demo with the saved model, runtime/dev dependencies, Docker files and five passing tests. Copy the whole folder to a separate working location for live demonstrations.
- [Workflow starter and reference](labs/lab1/workflows): teaching examples. The student's completed workflow belongs at `.github/workflows/ci.yml` in their own repository, with the service files at its root.
- [Independent challenge instructor guide](labs/final-lab/INSTRUCTOR_GUIDE.md): Hebrew reference solutions, common mistakes, three hint levels per path and debrief questions. Its `solutions/` directory has instructor reference files; the guide explains how to use them.

The shared model is the trusted existing SMS `TfidfVectorizer` + `MultinomialNB` Pipeline. Runtime dependency pins match the previous project. The new 500-character limit is an application rule measured after trimming, not an SMS standard. Synthetic text only is used in examples.

## Prepare the guided demonstration

Use your working copy of `labs/lab1/solutions/`. Set up Python 3.10 using the commands in the [student lab](<../Session6 - for students/LAB1.md>), then run from the completed project folder:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Expected: **5 passed**. For the GitHub demonstration, place the complete reference workflow at `.github/workflows/ci.yml` in your demo repository. Prepare actual failed/passing runs before class; the offline guide contains illustrative examples if hosted access is unavailable.

## Regenerate the presentation

Python 3.10 or later:

```bash
python -m venv .venv-build
```

Activate `.venv-build` with your platform's normal activation command, then:

```bash
python -m pip install -r requirements-presentation.txt
python scripts/build_presentation.py
```

The generator reads `content/part1.md` through `part5.md`, uses `reference/reference.pptx` for its proportions and theme, writes `output/session6.pptx`, and updates the five SVG diagrams. It does not alter lab work. Keep the slide title and fenced `text` block in each slide entry as the source of truth; use `scripts/build_presentation.py` for layout changes. Generating again replaces the PPTX, so preserve manual PowerPoint edits before rebuilding.

The previous local `.venv-build/` was removed during cleanup. The commands above create a fresh environment from the retained dependency file.

Install **Aptos**, **Aptos Display** and **Aptos Mono** for the intended slide typography, and **Arial** for Hebrew notes. Fonts are not bundled. Microsoft provides [the Aptos font pack](https://www.microsoft.com/en-us/download/details.aspx?id=106087). Rendering was verified with these fonts available.

## Repeat optional presentation QA

Install `requirements-qa.txt` into the presentation environment. With LibreOffice available, render the slides:

```bash
libreoffice --headless --convert-to pdf --outdir output/qa output/session6.pptx
```

With LibreOffice's `python3-uno` installed, export the actual Notes pages using the system Python:

```bash
python3 scripts/export_notes.py
```

Then run the native/source, notes, PDF, SVG and static workflow checks:

```bash
python scripts/check_presentation.py
```

This creates previews and machine-readable QA results. A visual review still matters. These checks do not execute hosted GitHub Actions; the instructor should prepare real failed/passing demonstration runs before teaching. The supplied offline logs are explicitly illustrative.
