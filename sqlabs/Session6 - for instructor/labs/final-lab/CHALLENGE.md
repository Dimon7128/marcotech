# Lab 2 — Independent CI Challenge

**Instructor reference:** Expanded teaching material. Distribute the compact [student guide](<../../../Session6 - for students/LAB2.md>) with the student folder.

Your team maintains the SMS spam/ham API from Labs 1A–1B. CI already tests it and builds an image. Some important behavior is still unchecked. Choose **one** mission, improve the same project, and prove your improvement works.

**Time:** 47 minutes of independent work, following the introduction. The instructor may allow 15 extra minutes. Sharing and recap follow separately.

## Starting point

Use your completed Part 3 repository, including the saved fitted model, the five baseline API tests, the 500-character input rule, and the working tests-and-build workflow. Keep compatible dependencies and synthetic SMS examples. Do not retrain, publish an image, deploy, or add a new service.

Work on a feature branch in your own training repository. You do not need to break or merge into a shared main branch.

## Choose one mission

### A — Make unexpected request fields visible

A client sends a valid `message` together with an unexpected JSON field. The API currently ignores extra fields. The team now wants such requests rejected, so client mistakes are visible.

Your improvement must:

- Reject a request containing an unexpected field with HTTP 422.
- Keep normal prediction requests and the existing input rules working.
- Include a meaningful automated check and evidence that it detects the missing policy before the fix.

Choose how to express and enforce the policy. This is a new requirement, not a claim that ignoring extra fields was previously a bug.

### B — Check the prediction response format

The existing tests parse the prediction body but do not check its declared media type. A response can contain readable JSON and still advertise the wrong Content-Type.

Your improvement must:

- Verify that a valid prediction declares the JSON media type, `application/json`; valid media-type parameters may also be present.
- Preserve the current status, response field and allowed-label checks.
- Demonstrate that your new check catches an unsuitable response media type, using a controlled training-only example, and finish with the correct behavior restored.

You decide how to construct the check and its evidence. Do not require a particular spam/ham result for an arbitrary synthetic message.

### C — Prove that CI checks pull requests

The current workflow runs after pushes. The team also wants changes proposed in pull requests to receive the same tests and image build.

Your improvement must:

- Retain push checks and add checks for pull requests in your own repository.
- Demonstrate an actual run triggered by pull-request activity; an ordinary push run alone does not prove the new behavior.
- Show that a controlled failed check blocks the later build, then restore passing tests and a successful build for the updated pull request.

Choose a simple implementation using the tools already introduced. No new credentials, external services, advanced workflow patterns, or deployment are required.

## Common acceptance criteria

- Define the gap and one meaningful improvement.
- Retain the baseline checks and the same saved model.
- Show detection of the chosen problem, or before/after event verification plus a controlled failed check. An unrelated setup error is not proof of the selected improvement.
- Finish with all local pytest checks passing.
- Show a successful final GitHub Actions run and Docker image build for the final commit.
- Explain what changed, why it helps, and what your evidence does not prove.

Different implementations can be valid. One mission meeting these criteria is enough. A second compatible check is an optional stretch, not a required extra lab.

## Deliverables

Keep your changes in your training repository and add a short `CHALLENGE_REPORT.md` containing:

- Your chosen mission and the gap you addressed.
- A brief explanation of the change.
- Links or captured results for the relevant failing/detection and passing evidence, with commit identifiers where available.
- Final local pytest result and the CI build result.
- Any limitations or verification still outstanding.

Be ready to show the relevant logs and explain your choices briefly. You do not need a slide deck, production deployment, or a full incident report.

## Documentation and help

- [Pydantic configuration](https://pydantic.dev/docs/validation/latest/api/pydantic/config/)
- [FastAPI response headers](https://fastapi.tiangolo.com/advanced/response-headers/)
- [pytest assertions](https://docs.pytest.org/en/stable/how-to/assert.html)
- [GitHub workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

Read the existing project, experiment, and ask the instructor for one hint at a time if you get stuck. You are not expected to remember every library option.

## If GitHub access is unavailable

Keep solving the chosen problem independently. Use local pytest and Docker where available, and keep your own detection/pass results. The example logs from Lab 1 are reading aids, not evidence that your improvement worked.

For mission C, explain the proposed event behavior and verification plan, and show any local failure/pass check you completed. Clearly mark hosted event verification and hosted build evidence as **not verified** until you can push and inspect the actual run. Do not claim the full hosted acceptance criteria were met by local execution alone.
