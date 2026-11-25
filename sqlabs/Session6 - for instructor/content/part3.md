# Part 3 — GitHub Actions Basics

**Course:** MLOps Essentials: AI Lifecycle Management  
**Session:** 6 — CI/CD for Machine Learning  
**Status:** Final assembly source; generation authorized by the final assembly request.  
**Slides:** 18–26.  
**Duration:** 50 minutes: 15 minutes of explanation/live demonstration and 35 minutes of guided student work.  
**Lab placement:** Lab 1 — Guided Learning, Stage B. Reuse Stage A's completed API, fitted model, dependencies, and five test functions.

The final assembly schedule is 205 minutes, including 107 minutes of student hands-on implementation (52.2%). Part 2 takes 40 minutes; this part retains its requested allocation.

The heading after each slide number and its `text` block are the exact English student-facing title and body. Timings, layouts, source checks, and Hebrew notes are instructor/production material. Code excerpts must remain native editable text in the approved PowerPoint. Only slide numbers may be added as footers.

## Interview decisions

- Every student creates their own GitHub repository. Put their completed Part 2 service files at its root and the workflow at `.github/workflows/ci.yml`.
- GitHub accounts and sign-in should be ready before class. Include repository creation, committing, and pushing in the guided lab.
- The instructor demonstrates the familiar temporary health assertion change from 200 to 201. Students are not required to create a deliberate failure in this guided stage; help them diagnose any incidental failure.
- Provide Windows PowerShell and macOS/Linux paths where commands differ, continuing the earlier setup decision.
- Keep this stage fully guided. Do not introduce or solve Part 5's independent challenge.

## Design

Continue the reference style: 16:9, white background, dark Aptos text, Aptos Display titles, large readable text, left alignment, generous whitespace, and restrained green accents. Use native text boxes, basic shapes, and arrows. Slide 22 contains the main CI workflow diagram. Slide 20 uses simple grouping to explain terminology; it is not a second pipeline.

Use editable teaching excerpts for logs rather than fabricated interface screenshots. Clearly identify example output. Show real GitHub interface behavior through the instructor's prepared runs only after those runs have actually been executed and inspected.

## Timing overview

| Slide | Title | Minutes | Activity |
| --- | --- | ---: | --- |
| 18 | From Manual to Automatic Tests | 1 | Reconnect to Part 2 |
| 19 | What Is GitHub Actions? | 1 | Definition and SMS example |
| 20 | Four Important Terms | 2 | Trigger, workflow, job, step |
| 21 | Where Does the Workflow Live? | 1 | Repository file placement |
| 22 | Our CI Workflow | 2 | One pipeline diagram |
| 23 | Read the YAML Structure | 2 | Essential keys only |
| 24 | When a Step Fails | 3 | Instructor failed-run demonstration |
| 25 | When Everything Passes | 3 | Instructor successful-run demonstration |
| 26 | Guided Lab 1: Automate the SMS API | 35 | Guided student implementation |
| Total | | 50 | 15 minutes explanation/demo + 35 minutes hands-on |

---

## Slide 18 — From Manual to Automatic Tests

**Estimated duration:** 1 minute.

### Exact student-facing text

```text
In Part 2, we ran pytest ourselves.
Our workflow will run the same tests after each push.
```

### Visual and layout

Use two large statements in the standard body position. Emphasize “ourselves” and “after each push.” No new workflow diagram on this slide.

### Hebrew instructor notes

**זמן משוער: דקה.**

- להזכיר שב-Part 2 הסטודנטים סיימו עם חמש פונקציות בדיקה שעוברות מקומית, כולל בדיקות הגבול של כלל האורך.
- לומר: ״אנחנו לא כותבים היום מחדש את הבדיקות. נלמד לבקש מ-GitHub להריץ את אותם קבצים אחרי push״.
- האוטומציה תתחיל רק לאחר שנוסיף workflow תקין למאגר. ה-GitHub repository לבדו אינו יוצר את הבדיקות או מחליף את הקוד מהחלק הקודם.
- מעבר: להציג את GitHub Actions ככלי שמפעיל את התהליך.

---

## Slide 19 — What Is GitHub Actions?

**Estimated duration:** 1 minute.

### Exact student-facing text

```text
GitHub Actions runs automation defined in our repository.
For our SMS API: run tests and build an image.
```

### Visual and layout

Use one plain-language definition and one SMS example. No logo, screenshot, or extra terminology.

### Hebrew instructor notes

**זמן משוער: דקה.**

- להסביר ש-GitHub Actions מבצע הוראות אוטומציה ששמורות יחד עם הפרויקט. בדוגמה שלנו ההוראות יפעילו בדיקות וינסו לבנות Docker image.
- את העבודה יבצע runner: מחשב שמריץ את ה-job. במעבדה נשתמש ב-runner של GitHub, ולא במחשב הפרטי של הסטודנט.
- המחשב הזה יקבל את קובצי המאגר. הוא לא יכול לראות מודל שנשאר רק בתיקייה מקומית במחשב שלנו.
- מעבר: נפריד בין ארבעה שמות שמופיעים בקובץ ובהרצה.

**Source check, not slide text:** The terminology follows [GitHub — Workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows). Runner software and image availability are checked separately when preparing the runnable lab.

---

## Slide 20 — Four Important Terms

**Estimated duration:** 2 minutes.

### Exact student-facing text

```text
Trigger: when it runs.
Workflow: the automation.
Job: a group of steps.
Step: one task.
```

### Visual and layout

Use four short definition groups. Show trigger separately and indent workflow, job, and step to suggest their relationship. Simple native outlines may group the text. Do not add unlisted labels, icons, or another process-arrow chain.

### Hebrew instructor notes

**זמן משוער: 2 דקות.**

- **Trigger:** האירוע שמתחיל הרצה. אצלנו זה `push` למאגר של הסטודנט.
- **Workflow:** האוטומציה כולה. ניתן לה את השם `SMS API CI`, כדי שנזהה אותה ב-GitHub.
- **Job:** קבוצה של steps שרצים על אותו runner. במעבדה יהיה job אחד בשם `check-and-build`. ה-job הוא קבוצת העבודה; ה-runner הוא המחשב שמבצע אותה.
- **Step:** משימה אחת, למשל התקנת dependencies, הרצת pytest או בניית image. חלק מה-steps משתמשים ב-action מוכן, ואחרים מריצים פקודה.
- לחבר למשפט אחד: push מפעיל workflow, ה-workflow מכיל job אחד, וה-job מריץ את ה-steps לפי הסדר. אין צורך לדבר על כמה jobs, תלות ביניהם או הרצות מקבילות.

---

## Slide 21 — Where Does the Workflow Live?

**Estimated duration:** 1 minute.

### Exact student-facing text

```text
Repository root
.github/workflows/ci.yml
main.py · model.joblib · test_api.py
GitHub reads the YAML to run our checks.
```

### Visual and layout

Use a compact native file-placement layout. Put the workflow path and the three service filenames under “Repository root”; they are all paths relative to that root. The workflow lives inside `.github/workflows/`, while the service files are direct children of the root. Keep all labels editable.

### Hebrew instructor notes

**זמן משוער: דקה.**

- להסביר שלכל סטודנט יהיה מאגר משלו, ובו קובצי השירות שסיים ב-Part 2. איננו מכניסים למאגר החדש את כל חומרי הקורס.
- GitHub מחפש workflow files בתיקיית `.github/workflows/` של שורש המאגר. שם הקובץ במעבדה יהיה `ci.yml`.
- להבחין בין שורש המאגר החדש לבין הנתיב שבו סיפקנו את ה-starter בחומרי הקורס. לאחר העברת אותם קבצים לשורש המאגר, הפקודות פשוטות וקובץ המודל נשאר ליד `main.py`.
- להזכיר שהעברת הקבצים אינה שינוי ב-API או במודל. אנחנו מוסיפים ניהול קוד ואוטומציה לאותו פרויקט.

**Source check, not slide text:** Repository-root workflow discovery is documented in [GitHub — Workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).

---

## Slide 22 — Our CI Workflow

**Estimated duration:** 2 minutes.

### Exact student-facing text

```text
Push
Checkout
Set up Python
Install Dependencies
pytest
Docker Build

Tests must pass before Docker builds.
Use the same saved SMS model.
```

### Visual and layout

Create the part's main workflow diagram using six native rectangles and five arrows, left to right in the listed order. Use line breaks inside longer labels, readable 24–28 pt diagram text, light neutral fills, and dark text. Put the two short statements underneath. The diagram describes the intended path, not an observed run.

Export a matching SVG to `assets/diagrams/part3-ci-workflow.svg`. Preserve native shapes and labels inside PowerPoint.

### Hebrew instructor notes

**זמן משוער: 2 דקות.**

- לעבור במשפט קצר על כל שלב: push מפעיל; checkout מביא את הקבצים; setup מכין Python תואם; ההתקנה מוסיפה את תלויות הפרויקט והבדיקות; pytest מריץ את חמש הבדיקות; Docker בונה image.
- ה-runner מקבל checkout חדש. לכן גם `model.joblib`, קובצי requirements וה-`dockerfile` צריכים להיות במאגר. אין העתקה אוטומטית של קבצים שלא בוצע להם commit.
- נשמור Python 3.10 ואת אותן גרסאות ML שמתאימות למודל. לא נוסיף שלב אימון כדי לפצות על מודל חסר.
- ב-job שלנו steps רגילים רצים לפי הסדר, ושלב הבנייה לא יופעל אם שלב הבדיקות נכשל. לא נוסיף מנגנון שמסתיר כישלון כדי להגיע ל-build.
- ה-Dockerfile הקיים נקרא `dockerfile` באותיות קטנות. הפקודה במדריך מציינת אותו במפורש, ו-build context יהיה שורש פרויקט השירות.

---

## Slide 23 — Read the YAML Structure

**Estimated duration:** 2 minutes.

### Exact student-facing text

```text
on: [push]
jobs:
  check-and-build:
    runs-on: ubuntu-latest
    steps:

Trigger, job, runner, then steps.
Full workflow: see the lab guide.
```

### Visual and layout

Show the five-line YAML excerpt as large native monospace text, with its two explanatory sentences below. This is an intentionally incomplete structural excerpt, not a runnable workflow. Keep full action definitions and commands in the guide.

### Hebrew instructor notes

**זמן משוער: 2 דקות.**

- להתחיל מהמפתחות: `on` מתאר מתי מתחילים, `jobs` מחזיק את העבודה, `runs-on` בוחר את סוג ה-runner, ו-`steps` מכיל את המשימות.
- להצביע על ההזחה: ה-job שייך ל-`jobs`, וה-steps שייכים ל-job. לשמור על spaces ולא tabs. אין צורך בשיעור YAML כללי.
- במדריך יופיעו `uses` עבור checkout ו-setup-python, ו-`run` עבור הפקודות שלנו. הסטודנטים ישלימו ארבעה ערכים מסומנים, ולא יכתבו הכול מהזיכרון.
- `ubuntu-latest` מתאר את מחשב הבדיקה ב-GitHub; הוא אינו משנה את מערכת ההפעלה של הסטודנט. נבחר את גרסת Python בנפרד כדי לשמור על התאמה למודל.
- השקף מציג רק מבנה. לא להעתיק אותו לבדו ולצפות להרצה תקינה; קובץ ה-workflow השלם נמצא במדריך.

**Source check, not slide text:** Key meanings and ordinary step behavior follow [GitHub — Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax). Python selection follows [GitHub — Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).

---

## Slide 24 — When a Step Fails

**Estimated duration:** 3 minutes, instructor demonstration.

### Exact student-facing text

```text
Example failure
Run API tests: FAILED
assert 200 == 201
Docker build: SKIPPED
Find the failing assertion in the logs.
```

### Visual and layout

Use an editable text excerpt, with “Example failure” clearly visible. Emphasize FAILED and SKIPPED with words and restrained color. This is a teaching summary, not a screenshot or claimed capture of an actual CI run.

### Hebrew instructor notes

**זמן משוער: 3 דקות.**

- **הכנה מראש:** לאחר יצירת המעבדה המאושרת, להכין במאגר הדגמה נפרד ריצת GitHub שנכשלה בעקבות שינוי זמני בציפיית health מ-200 ל-201. להכין גם את הריצה שתוקנה. ההוראות ב-[מדריך המרצה](../labs/lab1/part3_instructor_notes_he.md). אין להמתין בזמן ההסבר לתור או לבנייה חדשה.
- לפתוח את לשונית Actions, לבחור את ההרצה המתאימה לפי commit, להיכנס ל-job ולפתוח את `Run API tests`.
- להראות את `test_health`, את שורת ה-assert ואת הערכים 200 ו-201. זו אותה טעות מכוונת שהכרנו מקומית; הפעם הלוג מגיע מה-runner של GitHub.
- להראות שה-build דולג. כישלון בשלב הבדיקות הוא עדיין כישלון של ה-job, גם אם checkout והתקנת dependencies עברו.
- זו הדגמת מרצה בלבד. הסטודנטים יתמקדו בהשלמת workflow שעובר; אם ייתקלו בכישלון, יעבדו עם אותה שיטת קריאה של שם השלב, ההודעה והערכים.
- אם אין ריצות GitHub מוכנות, להשתמש ב-[תרגיל הצפייה החלופי](../labs/lab1/part3_offline_inspection.md) ולומר במפורש שמדובר בסיכומים להמחשה, לא בתוצאות CI שנבדקו בפועל.

---

## Slide 25 — When Everything Passes

**Estimated duration:** 3 minutes, instructor demonstration and explanation.

### Exact student-facing text

```text
A green run means:
Five API tests passed.
The Docker image built successfully.
The image was not published or deployed.
```

### Visual and layout

Use a short lead-in and three outcome statements. Use a restrained green emphasis for passed/successful, keeping the outcome words visible. Show the instructor's real prepared passing run in the browser where available; do not embed an invented UI screenshot.

### Hebrew instructor notes

**זמן משוער: 3 דקות.**

- להציג את הריצה המתוקנת ב-GitHub, לבחור את ה-commit הנכון ולפתוח גם את שלב pytest וגם את שלב הבנייה. להראות `5 passed` ואת סיום ה-build בהצלחה.
- להסביר שירוק הוא סיכום של המשימות שהגדרנו: חמש בדיקות עברו וה-image נבנה. חשוב לפתוח את הלוגים, ולא להסתפק בסמל ירוק בלי לדעת מה נבדק.
- הבדיקות רצות בתהליך Python על ה-runner, לפני בניית ה-image. לא הפעלנו את השירות בתוך container במסגרת workflow זה. ה-image נבנה על ה-runner; הוא לא נשלח ל-registry ולא נשמר אוטומטית כתוצר להפצה אחרי סיום ה-job.
- אין כאן הוכחה ל-precision או recall טובים, ואין אימון או deployment. את הקשר לשחרור מבוקר נלמד ב-Part 4 כאשר יתבקש.
- להוסיף בקצרה של-production CI יש עוד שיקולים: action versions, הרשאות, בטיחות dependencies ו-secrets. לא פותחים עליהם תרגיל נוסף. במעבדה הזאת לא מגדירים secrets או credentials משלנו ל-workflow; הגישה הרגילה של הסטודנט למאגר נדרשת לצורך push.
- מעבר: כעת כל סטודנט ייצור את המאגר שלו וישלים את אותו workflow בהדרכה.

---

## Slide 26 — Guided Lab 1: Automate the SMS API

**Estimated duration:** 35 minutes of guided student work. This includes repository creation, YAML completion, push, log inspection, and the final checkpoint; do not add another 35-minute exercise block afterward.

### Exact student-facing text

```text
Create your repository.
Complete and push the workflow.
Find five passing tests and a successful Docker build.

35 minutes
```

### Visual and layout

Use the first three lines as goals and put “35 minutes” in a small timing label. Keep the slide visible while students follow the separate guide. No full YAML, command list, QR placeholder, or unverified lab link on the slide.

### Hebrew instructor notes

**זמן משוער: 35 דקות של עבודה מודרכת.**

- לפתוח את [מדריך הסטודנט](<../../Session6 - for students/LAB1.md>). כל סטודנט יוצר מאגר משלו, מעביר אליו את הקבצים שהשלים ב-Part 2 ומשלים ארבעה שדות ב-workflow. אין צורך לשנות את הבדיקות, ה-schema או המודל.
- **חלוקת זמן:** 8 דקות למאגר ולהעברת קבצים, 10 דקות ל-workflow ולשדות החסרים, 6 דקות לבדיקת קבצים מנוהלים ול-commit/push, 8 דקות לבדיקת הריצה והלוגים, ו-3 דקות להסבר התוצאה.
- לפני push לבדוק ש-`model.joblib` נמצא בקבצים שנכנסים ל-commit, שה-TODO של התוויות הושלם ב-Part 2 ושאין עוד TODO בתוך ה-YAML. ה-runner לא ימצא קובץ שנשאר רק במחשב הסטודנט.
- בליווי: לבקש לזהות איזה step נכשל ומה ההודעה הראשונה הרלוונטית. להבדיל בין YAML שאינו מתקבל, התקנת dependencies שנכשלה, assertion שנכשל, ו-Docker build שלא מצא קובץ.
- **תוצאת סיום:** workflow בשם `SMS API CI`, job אחד, `5 passed` בשלב הבדיקות, build מוצלח ו-job שהסתיים בהצלחה. הסטודנט צריך לדעת להראות את הראיות בלוגים.
- אם אין גישת GitHub, להשתמש ב-[חלופה ללא גישה](../labs/lab1/part3_offline_inspection.md). הרצה מקומית או קריאת דוגמה אינן ריצת GitHub Actions. לתעד מה הושלם ומה עוד צריך להריץ כשיש גישה.
- להיעזר ב-[מדריך המרצה](../labs/lab1/part3_instructor_notes_he.md) עבור טעויות נפוצות. להאריך אם התור או ההתקנה מתעכבים, בלי לקצר את העבודה העצמאית ב-Part 5.
- מעבר ל-Part 4: הבדיקות וה-build מסתיימים בהצלחה; עכשיו נברר מה עוד צריך כדי לשחרר גרסה למשתמשים.

---

## Lab materials

Review together:

- [Guided student lab](../labs/lab1/part3_github_actions.md): starter YAML, four guided completions, complete reference workflow, repository setup, expected results, and troubleshooting.
- [Hebrew instructor guidance](../labs/lab1/part3_instructor_notes_he.md): preparation, demonstration, checkpoints, assistance, and reference answers.
- [Offline inspection exercise](../labs/lab1/part3_offline_inspection.md): labeled illustrative failure/success summaries, offline questions, and local reproduction commands.

The starter and complete workflow examples are provided under `labs/lab1/workflows/` for students' own repositories. Do not place an active workflow in the MLOPS repository root merely to create teaching assets. Do not create or push external repositories on students' behalf.

The completed Part 2 project files remain the baseline. Only `.github/workflows/ci.yml` is added to the student's project during this stage; any repository scaffolding must preserve the existing `.gitignore`, `.dockerignore`, model, tests, runtime pins, and input policy.

## Technical review and verification status

- Proposed action pins: [actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) and [actions/setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0). The tagged action manifests were reviewed for their actual inputs/runtime. Recheck release/runner compatibility when generating the final runnable examples.
- Use one GitHub-hosted `ubuntu-latest` job, Python `3.10`, the existing `requirements-dev.txt`, `python -m pytest -q`, and `docker build -f dockerfile -t sms-api:ci .` from the student's repository root.
- The Ubuntu runner software list includes Docker. Review the actual image before class; the `latest` label may move. See [GitHub runner images](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md).
- The existing lowercase Dockerfile copies the runtime requirements, API, and fitted model from its build context. Its `.dockerignore` permits exactly those inputs. Context handling follows [Docker — Build context](https://docs.docker.com/build/concepts/context/).
- The inspected API requires its saved model file at import time and has no application-specific required environment variables. The workflow therefore supplies the same tracked project files and dependencies without adding an environment-configuration exercise.
- The generated Part 2 starter and completed instructor solution are available. Continue from the completed five-test/500-character-policy version.
- The completed YAML was parsed and its trigger, permissions, job, step order, Python version, commands and pinned action releases checked. The app image was built and the five tests executed in an isolated local container.
- No hosted GitHub Actions run was triggered or observed. Local pytest/build evidence is recorded in the final QA report. Sample hosted logs remain explicitly illustrative, and the instructor should prepare real demonstration runs before class.
- Verify English slide text, useful Hebrew notes, 15/35-minute timing, and preservation of earlier parts before PowerPoint generation.

**Assembly status:** Included in the final assembly. See `../FINAL_QA_REPORT.md` for executed checks and remaining hosted verification.
