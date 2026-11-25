# Session 6 — CI/CD for Machine Learning

## Status and confirmed decisions

- Course: **MLOps Essentials: AI Lifecycle Management**.
- This is a new presentation for Session 6.
- Project directory: `/home/dima/git/MLOPS/session6` (confirmed by the instructor).
- Folder organization updated at the instructor's request on 21 November 2026: student handout in `Session6 - for students/`; teaching files, sources and solutions in `Session6 - for instructor/`. Relative maintenance paths below are from the instructor folder unless a path explicitly starts with `session6/`.
- Session 5 is a previous lecture and a visual reference only. Do not edit it or reuse unrelated educational content.
- Reference source: `../../lab4/session5.pptx`.
- Working reference copy: `reference/reference.pptx`.
- Current stage: **Final assembly and quality review**, explicitly authorized by the final assembly brief. The instructor also explicitly authorized completing the missing Part 5 from the supplied brief, using the recommended unexpected-field option and short evidence report.
- Exact titles and English student text from Parts 1–4 are preserved. Production status, overall timing, instructor transitions and stale drafting annotations have been finalized. The final request supersedes earlier pending-generation metadata; no new approval interview is required.
- All five Markdown sources, an editable 39-slide PowerPoint with embedded Hebrew notes, reusable SVGs, guided starter/reference files and independent challenge materials are present. The final QA report records actual checks. No external GitHub repository, hosted CI run, publishing step or deployment was created.
- The instructor's updated hands-on requirements replace the previous three-lab structure with two main labs: guided Lab 1 across Parts 2–3 and independent Lab 2 in Part 5. These requirements take precedence over earlier lab names, timing, and exercise instructions.

## Part 1 — accepted scope and interview decisions

- Part: **CI/CD in an ML Project**, exactly 25 minutes, with seven concise slides.
- Only one main workflow diagram: Code Push → Install Dependencies → Run Tests → Build Docker Image → CI Result.
- Show Continuous Delivery on the slide. Briefly clarify Continuous Deployment in Hebrew instructor notes only.
- Running example: a hypothetical rename of the API response field `label` to `prediction`, while the client still expects `label`.
- Participation: one short whole-class discussion, on Slide 2, included in the 25 minutes.
- No lab, test syntax, workflow YAML, Docker commands, pipeline implementation, deployment, or retraining in this part.
- Use the official [Google Cloud MLOps CI/CD/CT reference](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) as conceptual background, with project files and primary documentation supporting the examples.

## Part 2 — interview decisions and expanded validation

- Part: **Essential Tests**, continuing numbering from Slide 8. Draft ten short slides and separate Markdown lab/instructor guides.
- The instructor selected a self-contained Session 5 API starter and one shared saved model under `../Session6 - for students/sms-service/`.
- Setup instructions must cover both Windows PowerShell and macOS/Linux.
- The instructor requested more schema teaching and additional validation. Explain required fields, expected types, whitespace trimming, and input constraints alongside the three core API behaviors.
- Preserve the MLOPS worksheet's `message` field, `min_length=1`, routes, response fields, saved model, and `spam`/`ham` labels in the starter.
- Guided lab rule: `max_length=500`, measured after whitespace trimming. It is a chosen application policy, not an SMS standard, and is not yet enforced by the existing API.
- Cover missing/empty/whitespace-only input plus null/numeric input; add boundary checks for 500 accepted and 501 rejected. The expanded completion target is five test functions: three core API tests plus two boundary tests.
- Make the schema change only in the new lab copy; preserve the historical Session 5 sources. Keep the resulting API, model, and tests unchanged when continuing into Part 3.
- The final assembly request sets Part 2 to 40 minutes: 15 explanation/live demonstration and 25 guided implementation. Compress explanation timing only; preserve every English student text block and the complete exercise.
- No workflow YAML, CI implementation, advanced testing, mocks, deployment, or retraining in this part.

## Part 3 — requested scope and interview progress

- Part: **GitHub Actions Basics**, Slides 18–26. The final assembly is authorized; preserve the previous English content.
- Requested duration: 50 minutes, comprising 15 minutes of explanation/live demonstration and 35 minutes of guided student work. This replaces the earlier 35-minute Part 3 allocation.
- Continue Lab 1, Stage B, using the same completed Part 2 API, shared fitted model, dependencies, and five test functions. No model retraining or new input-policy change.
- **Confirmed repository decision:** each student creates their own GitHub repository. Plan for the completed Part 2 service files at that repository's root, with `.github/workflows/ci.yml` below the root. This is a source-control handoff of the same project, not a rebuilt application.
- Include guided repository creation, file placement, commit/push instructions, and checks that `model.joblib` is present in a fresh checkout. Do not assume students already have a repository. These are teaching instructions to draft; the assistant has not been asked to create external repositories for students.
- Use one simple job: checkout, Python setup, dependency installation, pytest, and a Docker image build. Build only after tests pass. No publishing, deployment, caching, matrix, custom secrets, or advanced workflow features.
- Preserve the actual lowercase `dockerfile` and its build context. It copies `requirements.txt`, `main.py`, and `model.joblib`; `.dockerignore` permits these files. Do not assume the saved model is available on GitHub merely because it exists on the instructor's machine.
- Explain trigger, workflow, job, step, and runner with minimal terminology. Use one primary editable CI diagram; keep the complete YAML in the separate guided lab guide.
- Provide a complete reference solution, expected results, troubleshooting, and additional Hebrew instructor guidance. Preserve the independent challenge for Part 5.
- Provide a no-GitHub-access fallback: complete example workflow, reproducible or clearly labeled illustrative failure/success logs, an offline inspection exercise, and local pytest/Docker commands where available. Never label local execution or illustrative logs as an actual inspected GitHub Actions run.
- Official references reviewed: [Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python), [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), and [Workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).
- Candidate action release pins verified during inspection: [actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) and [actions/setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0). Recheck release/runner compatibility before finalizing runnable YAML; do not blindly copy older versions from tutorial snippets.
- Docker builds, isolated pytest reference cases and real HTTP checks against a temporary runtime container were executed locally. No hosted GitHub run was observed. The lab starter and reference workflows are files, outside an active course-root workflow.
- **Confirmed readiness:** GitHub accounts and sign-in should be ready before class; repository creation remains inside the guided lab. Include local Git setup/normal push authentication in the preparation checklist rather than teaching a secrets implementation.
- **Confirmed demonstration choice:** the instructor alone demonstrates the familiar deliberately failing health assertion from 200 to 201 and its correction. Students focus on completing a passing workflow, with guided help for incidental failures.
- Draft numbering: Slides 18–26, nine slides totaling 50 minutes. The first eight slides take 15 minutes; the guided work slide takes 35 minutes. The complete workflow stays in the lab guide rather than on a slide.

## Part 4 — requested conceptual release scope

- Part: **From CI Result to a Release**, Slides 27–32, exactly 30 minutes. Six slides with durations 3, 5, 4, 5, 5, and 8 minutes, including the final discussion.
- The instructor's brief resolves the story, teaching depth, participation, and boundaries. The latest part-specific interview rule asks questions only when important decisions remain unresolved; no further questions were needed before this draft.
- Use one continuous future scenario: the SMS API passes its five tests and image build, then the team considers a controlled release. Do not claim an actual CI run, retained image, publishing step, or deployment occurred.
- Use illustrative `sms-api:v1.0` and `sms-api:v1.1` names to match the existing image name. The application update can be the Part 2 input policy while the saved model stays the same. Tags are references that can change, not immutable release guarantees.
- Distinguish the current Part 3 workflow, which builds only `sms-api:ci` on its runner, from a future process that must retain and make the selected release and recovery images available.
- Cover version identification, a team approval decision, the conceptual release, a lightweight smoke test against the active service, and rollback to a known previously working release using an appropriate mechanism.
- The smoke example uses `GET /health` and one valid synthetic `POST /predict` request; no precision/recall claim. The current health response does not include a release-version field.
- Use one main native PowerPoint release workflow: CI Passes → Identify Version → Approval → Release → Smoke Test → Keep or Roll Back. After approval, save a reusable SVG in `assets/diagrams/`. A simple application-version card diagram may also be reused.
- The final eight-minute segment includes a short discussion about valid prediction requests returning HTTP 500 after release. Let students answer first; Hebrew notes explain server-error meaning, limits of CI, smoke-test evidence, when rollback may help, and why it is not an automatic response to every problem.
- No Part 4 lab, new YAML, registry publishing, approval configuration, AWS/Kubernetes deployment, infrastructure configuration, rollback commands, advanced release patterns, or model retraining. Preserve the independent challenge in Part 5.

## Part 5 — independent challenge and final decisions

- Part: **Independent CI Challenge & Recap**, continuing from Slide 33 based on Part 4's current draft numbering. Plan approximately 5–7 concise slides with Hebrew notes.
- Latest requested allocation: 60 minutes — 5 minutes for introduction, 47 minutes for independent work, and 8 minutes for sharing/discussion/recap. This replaces the earlier 50-minute Part 5 allocation. An optional 15-minute extension should go to investigation and troubleshooting, not more theory.
- Use the existing SMS service and the completed Part 2 five-test/500-character-policy baseline, plus Part 3's one-job tests-and-build workflow. No new application, dataset, training, registry publication, deployment, advanced frameworks, or custom secrets.
- Students choose one main path: validation, prediction-response checks, or CI behavior. Paths must have comparable difficulty, measurable acceptance criteria, and room for different valid implementations.
- Avoid duplicating checks already covered: missing/empty/whitespace-only/null/numeric input, length boundaries, `label` presence, and allowed `spam`/`ham` values are already in the baseline. Repeating only these is not a meaningful new improvement.
- Final challenge options: reject unexpected request fields; verify JSON response Content-Type; or add pull-request checks and prove the actual event. Students choose one path.
- Reference checks: guided baseline, controlled failures, extra-field policy, response-header detection and permitted JSON media-type parameters were executed with pytest in an isolated Python 3.10 container. The workflow-only reference was checked statically; actual PR event behavior requires a hosted run and remains NOT VERIFIED.
- A new extra-field policy would be an intentional API change. The existing request model ignores extra fields; it is not correct to call that an existing validation bug. Any new policy must preserve the existing legitimate inputs and other validation rules.
- The existing workflow uses only `push`. A workflow-only path must demonstrate its added behavior in actual run metadata and logs, not merely edit YAML or show an unrelated push run.
- Common evidence: identify the gap, make a meaningful improvement, prove detection or before/after workflow behavior, finish with all local tests passing, a successful hosted CI run and Docker image build, and a brief explanation. Preserve baseline checks; the final test count depends on the chosen improvement.
- Demonstrate Red → Green where practical. For workflow-only work, allow before/after event verification plus a controlled failing assertion. Work in each student's own training repository/feature branch; do not require breaking shared main or deploying anything.
- Student materials must contain only scenario, options, objectives, acceptance criteria, time, deliverables, documentation links, and how to demonstrate completion. No full code/workflow solution, exact command sequence, or prescribed file-by-file implementation.
- Instructor-only Hebrew guidance must include preparation, at least one valid reference solution per path, code examples, common mistakes, three progressively revealed hints per path, and 3–4 final-discussion questions. Do not put all hints or answers on student slides.
- Keep differentiation optional: one path satisfying acceptance criteria is minimum success; additional independent improvements or compatible extra checks are stretch work, not more mandatory labs.
- Provide an access fallback using local pytest, local Docker where available, and clearly labeled example logs. Preserve independent investigation and record which hosted evidence still needs to be obtained.
- Use the latest requested paths: `labs/final-lab/CHALLENGE.md` and `labs/final-lab/INSTRUCTOR_GUIDE.md`. This folder contains **Lab 2 — Independent Challenge**, replacing the earlier `labs/lab2/` destination; it is not a third lab.
- Confirmed final decisions: authorize the new unexpected-field rejection policy for Option A, and require a short `CHALLENGE_REPORT.md` identifying the gap, change, relevant detection/pass evidence, final results and remaining limits. Baseline behavior remains unchanged for the other options.

## Central question and learning objective

**How can we automatically check and package our prediction service after code changes?**

Students should understand CI versus CD versus CT, write and run basic API tests, automate tests with GitHub Actions, inspect failed and successful runs, and build a Docker image after tests pass. Explain the conceptual transition to a controlled release.

## Audience and teaching approach

- Beginners with limited Python and ML experience; previous sessions covered training, MLflow, ML pipelines, and deployment fundamentals.
- Introduce concepts as **term → simple explanation → SMS project example**.
- Keep explanations concrete and practical; use short analogies where useful.
- Instructor background: DevOps and AWS. Put additional technical context in speaker notes.
- Continue the same SMS spam/ham classifier throughout.

## Scope and timing

| Part | Topic | Planned effective minutes | Hands-on placement |
| --- | --- | ---: | --- |
| 1 | CI/CD in an ML project | 25 | Discussion and simple checks for understanding |
| 2 | Essential tests | 40 | Lab 1 — Guided Learning, API testing and schema-validation stage: 25 minutes of student hands-on work |
| 3 | GitHub Actions basics | 50 | Lab 1 — Guided Learning, CI and Docker build stage: 35 minutes of student hands-on work |
| 4 | From CI result to a release | 30 | Controlled release concepts; no full CD implementation |
| 5 | Independent CI challenge and recap | 60 | Lab 2 — Independent Challenge: 5 minutes introduction, 47 minutes independent work, and 8 minutes sharing/recap |
| Total | | 205 | 107 minutes of student hands-on work: 52.2%; introductions and debrief are additional |

The final assembly request defines this 205-minute schedule. Lab 1 has 60 minutes of guided student implementation across Parts 2–3: 25 plus 35. Lab 2 has 47 minutes of independent work within its 60-minute allocation. Do not count observation-only demonstrations, introductions, recap or debrief as implementation time. The final 107-minute requirement is 52.2% of the plan, slightly above the earlier approximate 45–50% target. Preserve it.

Earlier draft aggregate estimates are superseded. Part 2's explanation/demo timing is reduced from 20 to 15 minutes; its 25-minute exercise and exact English student text are preserved. The optional Part 5 extension adds 15 minutes to independent work and the total effective session duration.

Hands-on learning should occupy approximately 45–50% of effective teaching time and must never fall below one-third. Extend the session when needed rather than rushing practical work, and recalculate the proportion against the actual effective duration. Do not sacrifice the independent challenge to make room for additional theoretical slides. Lab 2 builds on the working CI pipeline produced in Lab 1.

## Progressive hands-on learning — updated lab requirements

Use exactly two main labs. The two stages of Lab 1 are one continuing guided lab, not separate labs.

**Learning progression:** Guided demonstration → Guided implementation → Independent problem-solving → Review and discussion.

### Lab 1 — Guided Learning (Parts 2–3)

- Make this lab highly guided, beginner-friendly, and progressive. First demonstrate a small step, then let students implement and verify it.
- Build basic pytest tests for the existing SMS prediction API using FastAPI TestClient.
- Create a simple GitHub Actions CI workflow that runs the automated tests and builds a Docker image after the tests pass.
- Provide clear instructions, code examples, expected results, checkpoints, and troubleshooting tips. Explain why each step is necessary.
- Continue the same tests, service, and saved model from Part 2 into Part 3. Students must finish Lab 1 with a working CI pipeline, including passing automated tests and a successful Docker build.
- The initial estimate was approximately 40–50 minutes across Parts 2–3, with extensions allowed. The instructor's latest Part 3 request expands guided student implementation to 60 minutes: 25 in Part 2 and 35 in Part 3. The extension supports repository creation, workflow completion, fresh-checkout checks, and log inspection.
- Provide detailed Hebrew instructor notes explaining the teaching sequence, rationale, expected outcomes, common errors, and how to assist beginners.

### Lab 2 — Independent Challenge (Part 5)

- Present a realistic CI-related problem using the SMS project and the pipeline students completed in Lab 1.
- Offer several challenge options of comparable difficulty and expected effort. Each student or group chooses one option; different valid implementations are welcome.
- Define clear goals and observable acceptance criteria for each option. Evaluate the result and the student's reasoning, rather than conformity to one reference implementation.
- Do not give students a complete implementation or numbered coding instructions. Do not turn this lab into a guided break/fix recipe.
- Allow students to consult documentation and experiment. Provide optional hints that can be revealed progressively when a student is stuck, without exposing the solution at the outset.
- Keep the challenge within the existing API testing and Docker-building scope. No AWS deployment, full CD pipeline, or model retraining is required.
- Include a short debrief comparing possible solutions, implementation choices, and the evidence that each solution meets its acceptance criteria.
- Use the latest Part 5 allocation of 60 minutes: 5 minutes introduction, 47 minutes independent work, and 8 minutes review/discussion/recap. An optional 15-minute extension prioritizes independent investigation and troubleshooting.
- Provide Hebrew instructor-only notes containing possible solutions, common mistakes, progressive hints, ways to support struggling students without giving away the answer, and questions for the final discussion.
- Keep complete solutions and instructor-only guidance separate from the student-facing challenge brief. In the instructor PPTX, use the Notes section for teaching guidance rather than showing solutions on student-facing slides.

### Lab materials and teaching priorities

- Keep runnable instructions, code examples, challenge briefs, and detailed troubleshooting in separate files under `labs/`; do not crowd slides with them.
- Store both guided stages under `labs/lab1/` and the independent Lab 2 under `labs/final-lab/`, following the latest Part 5 file names. No third lab is planned.
- Detailed guidance belongs in Lab 1. Lab 2 uses clear problem statements, goals, acceptance criteria, and optional progressive hints while preserving student decision-making.
- Preserve the independent work allocation when revising theory, slide counts, or timing.

### In scope

- CI, CD, and CT distinctions.
- Automated API correctness testing, distinct from model precision/recall evaluation.
- pytest and FastAPI TestClient.
- GitHub Actions triggers, workflows, jobs, steps, and runners at beginner level.
- Automatic tests followed by Docker image building.
- Understanding failure logs and successful checks.
- A conceptual controlled release and approval step.

### Outside the practical implementation

- Advanced DevOps theory or advanced GitHub Actions configurations.
- Kubernetes production architecture, complex security scanning, a full CD pipeline, or AWS deployment.
- Repeating model training or switching to another dataset or application.

The older syllabus at `../../../marcotech/sqlabs/MLOps_Essentials_Complete_Syllabus.md` describes a broader Session 6 model-quality-gate lab. The instructor's current master prompt takes precedence: focus on API checks and packaging. Do not add a model-quality-gate implementation without further instruction.

## Visual direction from the reference

- Widescreen 16:9 format with white backgrounds and dark text.
- Aptos Display for titles and Aptos for body text, following the reference theme.
- Large left-aligned headings, consistent margins, generous whitespace, and restrained green diagram accents.
- Prefer one main idea per slide, usually 10–30 student-facing words excluding titles, and 1–3 short bullets.
- Use a flexible slide count; the previous 27-slide outline is not a limit.
- Use native PowerPoint text boxes, basic shapes, lines, arrows, and simple grouped diagrams.
- Keep short code snippets as editable text. Keep runnable code and detailed lab instructions in separate files.
- Build important diagrams with native shapes and also save matching reusable SVGs in `assets/diagrams/`.
- Avoid decorative imagery, unnecessary icons, crowded layouts, complex tables, large code blocks, flattened slides, and HTML slide screenshots.

## English slides and Hebrew speaker notes

- All student-facing slide text must be in English.
- Every instructional slide must contain useful speaker notes written in natural, clear Hebrew in the actual PPTX Notes section.
- Preserve familiar technical terms in English, such as CI, pytest, GitHub Actions, Docker, API, and workflow.
- Notes should support delivery rather than repeat slide text.
- Include, where useful: הסבר למרצה, דוגמה, אנלוגיה, שאלה לסטודנטים, דגשים, מעבר, זמן משוער.
- Do not mechanically include every category on every slide.
- Lab 1 notes must provide detailed Hebrew teaching guidance, explanations, expected outcomes, common errors, and practical assistance.
- Lab 2 notes must provide Hebrew instructor-only possible solutions, common mistakes, progressive hints, assistance that preserves student independence, and final-discussion questions. Do not copy complete solutions into the student challenge brief or slide text.
- Verify embedded notes directly in the generated PPTX; a separate notes document does not satisfy the requirement.
- The reference PPTX contains little substantive embedded commentary and no embedded Hebrew speaker notes; write new notes for Session 6.

## Existing technical conventions and findings

- Dataset: UCI SMS Spam Collection.
- Labels: `spam` and `ham`.
- Saved fitted model: `TfidfVectorizer` + `MultinomialNB` in a scikit-learn Pipeline.
- Serving: FastAPI. Testing: pytest and FastAPI TestClient. Packaging: Docker. Automation: GitHub Actions.
- Existing API contract: `GET /health` returns `{"status": "ok"}`; `POST /predict` accepts a JSON `message` field and returns a JSON `label` field.
- Existing examples load a trusted `model.joblib` next to `main.py` at module import time. Account for this when designing CI setup and tests.
- `../lab4/part2.md` contains the API implementation with whitespace stripping and `min_length=1`.
- A completed implementation at `../../../marcotech/sqlabs/lab4/docker/sms-service/main.py` uses `min_length=2`; do not silently mix these validation policies.
- The completed service and shared saved model have been inspected. Observed responses: health and valid prediction HTTP 200; missing/empty/whitespace-only input HTTP 422. Null/numeric input and the proposed length constraint were also checked directly using Pydantic 2.14.3, without changing either service.
- The Part 2 starter will use the MLOPS worksheet's minimum length, with the shared existing model. The proposed `max_length=500` is a new guided schema change authorized in the final assembly, not a claim about current Session 5 behavior.
- The completed Docker example in that directory uses a lowercase `dockerfile`, Python 3.10, and the model artifact in its build context. Do not assume that directory or artifact is already present in the MLOPS project.
- Existing ML and API dependency pins must be inspected and validated before reuse; do not invent versions. pytest and TestClient's HTTP dependency will need explicit setup for the labs.
- Validate teaching examples against project files and official documentation before approval.
- Use only synthetic custom SMS examples, never private messages.

## Incremental workflow and final assembly authorization

The original part-by-part workflow below governed drafting. The later explicit final assembly request authorizes implementation and asks not to repeat approvals. The instructor separately authorized completion of the missing Part 5. Keep these authorization facts distinct from an assumed earlier approval.

### Stage A — Inspect and interview

Inspect the reference and project, identify style, review the course plan, and ask 3–5 focused questions about unresolved decisions. Wait for the instructor's answers before drafting.

### Stage B — Draft one requested part

When the instructor requests `Create Part N`, save only that part's Markdown draft to `content/partN.md`. Each slide entry must include:

- Slide number and title.
- Exact English student-facing text.
- Proposed diagram or visual, where useful.
- Practical Hebrew instructor notes.
- Estimated duration.
- Lab placement and guided/independent stage, where applicable.

Stop and request explicit Markdown approval. Do not generate PowerPoint at this stage.

### Stage C — Generate the approved part

Only after explicit approval of that part's Markdown, generate native editable PowerPoint slides and embedded Hebrew speaker notes. Create reusable SVG diagrams, preserve approved sections, render where tools permit, and inspect spacing, alignment, overflow, and readability.

### Stage D — Review and refine

Report slides, concepts, labs, visuals, and any specific review decisions. Ask for targeted feedback, refine the part, and do not proceed to the next part until explicitly requested.

### Stage E — Final assembly

After all five parts are approved, assemble and review `output/session6.pptx`. Verify ordering, English slide text, embedded Hebrew notes, editability, visual consistency, the two-lab progression, total timing, and hands-on proportion. Confirm that Lab 1 ends with a working CI pipeline and Lab 2 retains meaningful independent work, comparable challenge options, acceptance criteria, optional progressive hints, and a debrief. Deliver the PPTX, Markdown sources, student lab guides, separate instructor guidance, reusable diagrams, and minimal regeneration source.

## Project layout

```text
session6/
├── README.md
├── Session6 - for students/
│   ├── README.md
│   ├── LAB1.md
│   ├── LAB2.md
│   └── sms-service/                  # Eight-file beginner starter
└── Session6 - for instructor/
    ├── README.md
    ├── FILES_GUIDE.md
    ├── content/                      # Five editable Markdown sources
    ├── assets/diagrams/              # Five reusable SVG diagrams
    ├── labs/
    │   ├── lab1/                     # Hebrew guides and expanded references
    │   │   └── solutions/            # Complete runnable five-test demo
    │   └── final-lab/                # Independent challenge guide and solutions
    ├── output/session6.pptx
    ├── output/qa/                    # Small JSON validation records
    ├── reference/reference.pptx      # Required for regeneration
    ├── scripts/                      # Build and optional inspection tools
    ├── requirements-presentation.txt
    ├── requirements-qa.txt
    ├── FINAL_QA_REPORT.md
    └── SESSION6_MASTER_SPEC.md
```

Remove local environments, caches, redundant starter copies and reproducible inspection images/PDFs from the distributed course folders. Preserve the compiled PPTX, English student content, embedded Hebrew notes, model artifacts and editable regeneration sources. The instructor's completed guided project and the student starter are intentionally different working states; each includes its required model and dependencies.

Use a reliable library that supports native editable elements and actual notes. Preserve regeneration source, use minimal dependencies, and avoid unnecessary build infrastructure. The final deck and Notes pages were rendered with LibreOffice and inspected. Validation results and limits are in `FINAL_QA_REPORT.md`.

## Confirmed interview decisions

The instructor has selected the self-contained starter/shared saved model, both Windows PowerShell and macOS/Linux command paths, and a repository created separately by each student. Do not re-ask those choices. Include beginner-friendly Git and repository-creation steps as part of the guided Part 3 lab.

The Part 3 interview is complete: GitHub accounts/sign-in ready before class, and the temporary health assertion change from 200 to 201 is demonstrated only by the instructor in the guided stage. Do not re-ask these choices. The final assembly request authorizes PowerPoint and lab-file generation.

The Part 5 decisions are complete: the instructor authorized completion from the supplied brief, including the recommended unexpected-field policy option and short evidence report. Do not repeat the interview.

Lab guidance is decided by the updated requirements: detailed examples and implementation guidance in Lab 1; an independent challenge with acceptance criteria and optional progressive hints in Lab 2. Do not re-ask whether both labs should use the same level of scaffolding.

## Quality checks for every part

- Slides are short, readable, and focused on one main idea.
- All slide elements that can be native are editable.
- Visual style, margins, typography, and spacing are consistent.
- No text is cut off or overflowing.
- Relevant diagrams have reusable SVG exports.
- Every instructional slide has practical embedded Hebrew notes.
- Exercises appear at the agreed points and remain separate from detailed runnable instructions.
- Lab 1 spans Parts 2–3 and ends with working automated tests and a Docker build.
- Lab 2 protects independent problem-solving time, offers comparable challenge options, and includes acceptance criteria, progressive hints, and a short debrief.
- Student-facing challenge materials do not reveal complete implementations, numbered coding instructions, or instructor-only solutions.
- Student hands-on time is calculated separately from demonstrations and debrief; target approximately 45–50% and never less than one-third.
- Examples, commands, tests, and workflows are accurate and appropriate for beginners.
- Previously approved parts remain intact.
