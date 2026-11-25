# Lab 1 — Guided Learning, Stage B: Automate the SMS API

**Instructor reference:** Expanded teaching material. Distribute the compact [student guide](<../../../Session6 - for students/LAB1.md>) with the student folder.

**Status:** Final teaching materials. See [the QA report](../../FINAL_QA_REPORT.md) for executed checks and hosted-run limitations.  
**Placement:** Session 6, Part 3. Continue the same Lab 1 from Part 2.  
**Student work:** Approximately 35 minutes after the instructor's explanation and demonstration.  
**Goal:** Push your completed SMS service to your own repository, run its five tests automatically, and build its Docker image in CI.

## Before the exercise

- Have your GitHub account and sign-in ready. You will create the repository during the lab.
- Have Git available, with your normal method of authenticating a push to GitHub. Complete one-time Git identity/sign-in setup before the timed exercise where possible; ask the instructor for help if it blocks you.
- Finish [Lab 1, Stage A](part2_api_testing.md): five local tests pass, the allowed-label TODO is completed, and the lab API has `max_length=500` after trimming.
- Keep the same trusted fitted model, Python 3.10, runtime dependency versions, and test code. No training or dataset download is needed.
- GitHub Actions must be available in your repository. No custom workflow secrets, registry account, or deployment credentials are needed. Your normal GitHub access is needed to commit and push.
- Docker on your own machine is optional for the main cloud lab; GitHub's Ubuntu runner performs the build. Local Docker is needed only if you choose to reproduce the build locally.

If GitHub access is unavailable, use the [offline inspection exercise](part3_offline_inspection.md). It explains what can be completed locally and what still requires a real GitHub run.

## Checkpoints and time

| Activity | Minutes | Checkpoint |
| --- | ---: | --- |
| Create the repository and prepare the existing files | 8 | Correct project-root layout |
| Complete and understand the starter YAML | 10 | Four TODO values replaced |
| Check tracked files, commit, and push | 6 | Workflow and saved model visible on GitHub |
| Inspect the run and logs | 8 | Five tests and Docker build succeeded |
| Explain the result | 3 | Know what passed and what was not performed |
| Total | 35 | A working CI pipeline |

Queueing or installation delays can require an extension. Keep working through the checkpoints with the instructor rather than skipping log inspection.

## 1. Create your own repository

**Why:** Your workflow and the files it needs must be available to GitHub, not only on your laptop.

In GitHub, create a new repository under your account. Choose a name such as `sms-api-ci`. Use the repository visibility agreed for the class and confirm Actions is available.

For this guided path, create an **empty** repository: leave the options to add a README, `.gitignore`, or license unselected. We will supply the existing project files and make the first commit locally. Keep the repository's setup page open so you can copy its actual remote URL later.

Create a separate local folder for this repository outside the course checkout. Copy these eight files from your **completed Part 2** `sms-service/` folder:

```text
main.py
model.joblib
requirements.txt
requirements-dev.txt
test_api.py
dockerfile
.dockerignore
.gitignore
```

Include the two hidden ignore files. Do not copy the course repository's `.git` directory or a virtual environment. This copies the same working application; do not recreate the API, replace the model, remove tests, or change the input rules.

Open a terminal inside your new local project folder. **Every command in this guide runs from this project root.**

Your completed layout will be:

```text
your-student-repository/
├── .github/
│   └── workflows/
│       └── ci.yml
├── main.py
├── model.joblib
├── requirements.txt
├── requirements-dev.txt
├── test_api.py
├── dockerfile
├── .dockerignore
└── .gitignore
```

This layout differs from the path used to distribute the lab in the course materials. In **your** repository, the service files are directly at the root.

### Check the existing tests locally

Use the Python environment from Part 2 if it is already active. Otherwise, prepare a matching environment in the new folder.

Windows PowerShell:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

macOS/Linux:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Run:

```bash
python -m pytest -q
```

Expect **`5 passed`**. If this fails, fix the Stage A problem with the instructor before investigating a cloud-specific problem. TestClient still loads `model.joblib`; no Uvicorn process is needed.

## 2. Create the workflow file

**Why:** GitHub reads YAML files from `.github/workflows/` at the repository root to find the automation.

Create the directory.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force .github/workflows
```

macOS/Linux:

```bash
mkdir -p .github/workflows
```

In your editor, create `.github/workflows/ci.yml`. Paste this starter, keeping its spaces and indentation:

```yaml
name: SMS API CI

on: [TODO_TRIGGER]

permissions:
  contents: read

jobs:
  check-and-build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v7.0.1

      - name: Set up Python
        uses: actions/setup-python@v7.1.0
        with:
          python-version: "TODO_PYTHON_VERSION"

      - name: Install dependencies
        run: python -m pip install -r requirements-dev.txt

      - name: Run API tests
        run: TODO_TEST_COMMAND

      - name: Build Docker image
        run: TODO_BUILD_COMMAND
```

The starter is intentionally incomplete. Complete its four TODO values **before** committing and pushing it. Do not expect this unfinished version to be accepted as a functioning workflow.

## 3. Complete the trigger and Python version

**Trigger:** Replace `TODO_TRIGGER` with `push`. The workflow will run when a push reaches this repository. We are not adding branch filters, schedules, or manual triggers.

**Python:** Replace `TODO_PYTHON_VERSION` with `3.10`, keeping the quotes. This matches the shared-model handoff and the existing Dockerfile. It does not change your laptop's Python installation.

The two `uses` lines call official actions:

- `checkout` brings the pushed repository files onto the runner.
- `setup-python` makes the selected Python available for the next commands.

The runner is the machine executing the job. The `check-and-build` job groups our steps on one GitHub-hosted Ubuntu runner. The action release tags shown here were checked against their official releases for the final teaching materials; use the instructor's reviewed version rather than replacing them with versions from an unrelated tutorial.

The small `permissions` block gives the workflow read access to the repository. There is no token or password for you to paste into the YAML.

## 4. Complete the test and build commands

**Dependencies:** The supplied install step uses `requirements-dev.txt`. That file includes the runtime requirements plus pytest and HTTPX, so the fresh runner receives both the application packages and the testing tools.

**Tests:** Replace `TODO_TEST_COMMAND` with:

```bash
python -m pytest -q
```

This is the same command and the same five tests used locally. The workflow does not create new tests or train the model.

**Build:** Replace `TODO_BUILD_COMMAND` with:

```bash
docker build -f dockerfile -t sms-api:ci .
```

The command has three important parts:

- `-f dockerfile` selects the existing lowercase filename explicitly.
- `-t sms-api:ci` names the image built on this runner.
- The final `.` supplies the current project root as the build context.

The Dockerfile's `COPY` instructions need `requirements.txt`, `main.py`, and `model.joblib` in that context. The existing `.dockerignore` permits those files. It intentionally leaves the tests and development environment out of the runtime image; the tests have already run on the runner.

In this one-job workflow, the ordinary build step follows pytest and runs only if the preceding work succeeds. Keep the failure behavior: do not add anything that hides a failed test just to reach the build.

## Complete reference workflow

Compare your completed file with this reference. Read what each step does rather than checking only that the text matches.

```yaml
name: SMS API CI

on: [push]

permissions:
  contents: read

jobs:
  check-and-build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v7.0.1

      - name: Set up Python
        uses: actions/setup-python@v7.1.0
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: python -m pip install -r requirements-dev.txt

      - name: Run API tests
        run: python -m pytest -q

      - name: Build Docker image
        run: docker build -f dockerfile -t sms-api:ci .
```

This contains one push trigger, one job, and five steps that we define. GitHub may display additional automatic setup or cleanup entries around those steps.

## 5. Check files, commit, and push

**Why:** A fresh runner has the files in the pushed commit. It cannot load a model that was left only in your local folder.

Initialize the new local repository and stage the project files:

```bash
git init
git branch -M main
git add .
```

Check that the important inputs are tracked/staged:

```bash
git ls-files --error-unmatch model.joblib test_api.py dockerfile requirements.txt requirements-dev.txt .dockerignore .github/workflows/ci.yml
git status --short
```

The first command should list every named file. Review `git status`: project source and the workflow should be present; `.venv/` and Python/pytest cache directories should be excluded by the copied `.gitignore`.

If the provided model is ignored, inspect the matching rule:

```bash
git check-ignore -v model.joblib
```

Ask the instructor to help correct the rule that hides the supplied artifact, then stage the file again. Do not replace the missing-model problem with an automatic training step.

Commit:

```bash
git commit -m "Add CI for the SMS API"
```

Copy the actual remote URL from the empty repository you created on GitHub. Replace the entire quoted placeholder below with that URL; the placeholder itself is not a working remote:

```bash
git remote add origin "PASTE_YOUR_REPOSITORY_URL_HERE"
git push -u origin main
```

Use your normal GitHub authentication if Git requests it. We do not put your sign-in details into the workflow.

On the repository's **Code** page, verify that `model.joblib`, the service/test files, and `.github/workflows/ci.yml` are visible. This is an important check of what the runner will actually receive.

## 6. Inspect the GitHub Actions run

**Why:** The result tells you which part of the automation worked or failed.

Open **Actions** in your repository, choose **SMS API CI**, and select the run associated with your pushed commit. Open the **check-and-build** job.

Inspect the named steps:

| Step | Evidence to look for |
| --- | --- |
| Check out repository | The pushed project files were checked out successfully |
| Set up Python | Python 3.10 was selected |
| Install dependencies | Runtime and testing dependencies installed without errors |
| Run API tests | `5 passed` |
| Build Docker image | The build completed and named the image `sms-api:ci` |

Confirm that the overall job and workflow succeeded. Build output formatting and execution times may vary.

If the run fails, open the first relevant failed step and read its error before changing code. Use the troubleshooting table below. Your task is a guided working workflow; you are not required to create the instructor's deliberate failure yourself.

After a correction, commit and push it to create a run for the new code:

```bash
git add .
git commit -m "Fix the SMS CI workflow"
git push
```

Use a correction commit only when you actually changed a file. Re-running an old failed run checks that old commit again; it does not automatically test unpushed edits.

## 7. Explain what passed

You are finished when you can show:

- The workflow in your own repository, with all TODO values completed.
- The saved model and required source files in the pushed commit.
- Five passing API tests in the run's logs.
- A successful Docker build after the tests.
- A successful overall job, with the same API and model from Part 2.

Be ready to explain these limits:

- The image was built on the runner. It was not pushed to a registry or deployed.
- The workflow does not start the service in a container to test container behavior.
- The image is not automatically retained as a downloadable release artifact after the job ends.
- API tests do not prove good accuracy, precision, or recall, and this workflow does not retrain the model.

Keep these project files for the later parts. The independent challenge comes in Part 5; it is not an extra task in this guided lab.

## Troubleshooting

| Symptom | Likely cause and guided fix |
| --- | --- |
| No workflow appears | Check the path `.github/workflows/ci.yml` from the repository root and confirm the file was committed and pushed. A file named `ci.yml.txt` is not the intended YAML file. |
| No manual Run workflow button | This example uses `push`, not `workflow_dispatch`. Push the completed workflow or a correction. |
| Invalid workflow/YAML message | Check indentation, spaces instead of tabs, colons, list dashes, and any remaining TODO values. Compare with the complete reference. |
| Setup Python fails | Check that the quoted version is `"3.10"` and the official action identifier matches the reviewed reference. |
| `requirements-dev.txt` not found | Check that it is at this student's repository root. Do not use the distribution path from the full course repository. |
| `pytest` or HTTPX missing | Install from `requirements-dev.txt`, not only the runtime requirements. |
| `model.joblib` missing during import | Confirm it is in the pushed commit beside `main.py`; local presence is insufficient. Inspect ignore rules and file placement. |
| Prediction test still reports TODO | Finish the Part 2 allowed-label assertion and push the corrected file. |
| Overlong-input test fails | Confirm the completed Part 2 schema with `max_length=500` was copied, saved, committed, and pushed. Do not change the test to hide the missing rule. |
| Tests pass but Docker build fails | Open the build step. Check lowercase `dockerfile`, explicit `-f`, the final build-context `.`, required files, and any package/pull error. |
| Docker build is skipped after a failed test | This is the intended ordering. Diagnose the pytest failure before expecting the image build. |
| Build cannot fetch its base image or a package | Read the network/package error with the instructor. A fetch failure is different from a failed API assertion. |
| Push authentication fails | Check the repository URL and your normal GitHub access with the instructor. Do not add credentials to the YAML; use the offline exercise while access is resolved. |
| Git asks for a commit identity | Configure your own Git name/email for this repository with instructor help, then retry the commit. This is local Git setup, not a CI secret. |
| Remote already has a README/initial commit | Clone that repository into a separate working folder first, copy the same completed service files into it, then commit and push using the existing history. |
| An old run still fails after a local edit | Push the correction and inspect the new commit's run. An old run does not see unpushed files. |

If PowerShell blocks virtual-environment activation, use `.\.venv\Scripts\python.exe` directly for the local pip/pytest commands, as in the Part 2 guide. Git commands themselves do not require a Python environment.

## Sources and verification status

Workflow location and terms follow [GitHub — Workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows); structure and step behavior follow [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax). Dependency/test setup follows [Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python). The selected releases are [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) and [setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0). Build-context behavior follows [Docker — Build context](https://docs.docker.com/build/concepts/context/).

The expected hosted results are a teaching target. See `../../FINAL_QA_REPORT.md` for local test/build results and static workflow checks. A real GitHub run must be triggered and its logs inspected before reporting hosted CI as verified.
