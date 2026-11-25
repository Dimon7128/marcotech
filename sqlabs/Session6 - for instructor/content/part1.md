# Part 1 — CI/CD in an ML Project

**Course:** MLOps Essentials: AI Lifecycle Management  
**Session:** 6 — CI/CD for Machine Learning  
**Status:** Final assembly source; generation authorized by the final assembly request.  
**Duration:** 25 minutes, including one short whole-class discussion.  
**Slides:** 1–7.  
**Lab placement:** None in Part 1. Lab 1 — Guided Learning starts in Part 2 and continues in Part 3. Lab 2 — Independent Challenge takes place in Part 5.

The text inside each `text` block is the exact English student-facing body text. The slide title is the heading after its slide number. Layout descriptions, timing, source checks, and Hebrew notes are instructor or production material; do not place them on slides. Only slide numbers may be added as footers.

## Approved interview choices

- Use **Continuous Delivery** on the student-facing slide. Clarify **Continuous Deployment** briefly in the Hebrew notes only.
- Use a hypothetical change from the response field `label` to `prediction` as the running example. The existing API has not been changed.
- Use one short whole-class discussion, on Slide 2.
- Apply the updated two-lab progression: guided demonstration and implementation in Parts 2–3, followed by independent problem-solving and a debrief in Part 5.

## Design and teaching boundaries

Follow the Session 5 visual identity: 16:9, white background, dark Aptos text, Aptos Display titles, consistent left alignment, generous whitespace, and restrained green accents. Plan approximately 40–44 pt titles and 28–32 pt body text; diagram labels may use 24–28 pt. Keep all text native and editable when generating the approved PPTX.

Slide 6 contains this part's only workflow diagram. Other slides use text or simple concept columns. No code blocks, commands, live implementation, or lab appear in this part. In the later PPTX stage, place each Hebrew notes section in the actual PowerPoint Notes section.

## Timing overview

| Slide | Title | Minutes |
| --- | --- | ---: |
| 1 | From Working Code to Reliable Changes | 3 |
| 2 | Why Do We Need Automation? | 3 |
| 3 | Continuous Integration (CI) | 3 |
| 4 | CI vs CD vs CT | 5 |
| 5 | What Can Change in an ML Project? | 4 |
| 6 | Our First CI Pipeline | 5 |
| 7 | What Will We Build Today? | 2 |
| Total | | 25 |

---

## Slide 1 — From Working Code to Reliable Changes

**Estimated duration:** 3 minutes.

### Exact student-facing text

```text
Our SMS classifier runs with FastAPI and Docker.
Every code change needs fresh checks.
```

### Visual and layout

Use the standard title position and two short, left-aligned statements below it. Emphasize “Every code change” with bold text. No diagram, icon, or additional subtitle.

### Hebrew instructor notes

**זמן משוער: 3 דקות.**

- **חיבור ל-Session 5 — כ-45 שניות:** להזכיר את מה שכבר בנינו: FastAPI מקבל הודעת SMS, מעביר אותה ל-Pipeline השמור ומחזיר `spam` או `ham`. Docker אורז את השירות והתלויות. אין צורך לפתוח שוב את הקוד או להריץ הדגמה.
- **הבעיה החדשה — כדקה ורבע:** לומר: ״עד עכשיו הוכחנו שהגרסה שבנינו עובדת. עכשיו נחשוב על העדכון הבא: מישהו משנה קוד, ואנחנו צריכים לדעת שהשירות עדיין מתנהג כפי שהלקוח מצפה״. אפשר להזכיר שגם תיקון קטן בתשובת ה-API עלול להשפיע על יישום שמשתמש בה, אף שהמודל עצמו נשאר זהה.
- **מטרת המפגש והמעבר — כדקה:** היום נוסיף תהליך שמבצע בדיקות חוזרות ומנסה לבנות Docker image אחרי שינוי. ההצלחה של אתמול אינה תוצאת בדיקה של הקוד החדש. להדגיש שהמטרה היא לקבל משוב מוקדם על הגרסה החדשה. לעבור לדוגמה אחת קטנה שתלווה אותנו בחלק הזה: שינוי בשם של שדה בתשובה.

---

## Slide 2 — Why Do We Need Automation?

**Estimated duration:** 3 minutes, including a one-minute whole-class discussion.

### Exact student-facing text

```text
A developer renames label to prediction.
The client still expects label.
An automated check can catch the mismatch.
```

### Visual and layout

Use three short lines in one text area. Format `label` and `prediction` consistently as emphasized field names. Keep the first two lines dark; use a restrained green emphasis for “automated check.” Do not add response JSON, an arrow diagram, or a screenshot.

### Hebrew instructor notes

**זמן משוער: 3 דקות — דקה לדוגמה, דקה לדיון, ודקה לסיכום.**

- **הדוגמה:** זהו תרחיש דמיוני. בפרויקט שלנו `POST /predict` מחזיר שדה בשם `label`. נניח שמפתח משנה רק את שם השדה ל-`prediction`, אבל הלקוח ממשיך לחפש `label`. המודל יכול להחזיר בדיוק אותו סיווג, ובכל זאת הלקוח לא יוכל להשתמש בתשובה כפי שהוא רגיל.
- **שאלה אחת לכל הכיתה:** ״ה-API עדיין מחזיר HTTP 200, אבל שם השדה השתנה. מה עלול להישבר אצל הלקוח?״ לתת זמן קצר לחשוב ולקבל שתיים או שלוש תשובות. אין צורך בעבודה בזוגות או בפתיחת מחשבים.
- **תשובה צפויה:** הלקוח לא מוצא את השדה שהוא צריך, ולכן הצגת התוצאה עלולה להיכשל. HTTP 200 לבדו אינו בודק את מבנה התשובה. זו התאמה בין יישומים, לא שאלה של איכות החיזוי.
- **הסיכום:** אפשר לבדוק את זה ידנית בכל עדכון, אבל קל לשכוח שלב. בדיקה אוטומטית שמוודאת שקיים `label` יכולה לגלות את השינוי בכל הרצה. שינוי מכוון בממשק דורש תיאום ועדכון של הלקוחות והבדיקות; הדוגמה שלנו עוסקת בשינוי שלא תואם עם הלקוח.
- **מעבר:** לתהליך שבו משלבים שינויים ומקבלים עליהם בדיקות אוטומטיות קוראים CI.

---

## Slide 3 — Continuous Integration (CI)

**Estimated duration:** 3 minutes.

### Exact student-facing text

```text
Automatically check code changes as they are shared.
For our SMS API: verify responses still match expectations.
```

### Visual and layout

Use the title to introduce the full term and acronym. Put the plain-language explanation on the first line and the SMS example below it. Use a simple text layout, without another process diagram.

### Hebrew instructor notes

**זמן משוער: 3 דקות.**

- **המושג — כדקה:** CI הוא קיצור של Continuous Integration. משלבים שינויים קטנים לעיתים קרובות במאגר קוד משותף, ומריצים בדיקות אוטומטיות כדי לגלות בעיות מוקדם. ההרגל של שילוב שינויים חשוב; בחלק הזה נתמקד במשוב האוטומטי שמקבלים עליהם.
- **הדוגמה מהפרויקט — כדקה:** נרצה שאחרי `push` ל-GitHub תורץ בדיקה שמוודאת שתשובת החיזוי כוללת `label`, ושערכו הוא `spam` או `ham`. אם החלפנו את השם ל-`prediction`, הבדיקה תגלה שהציפייה כבר אינה מתקיימת. בהמשך נכיר את GitHub Actions ככלי שמריץ את התהליך.
- **מה חשוב להבהיר — כדקה:** האוטומציה רצה בעקבות טריגר שנגדיר; היא אינה נוצרת מעצם השמירה של קובץ במחשב. הבדיקות בודקות את הכללים שכתבנו, ולכן כדאי לבחור כללים שמייצגים את מה שהלקוח צריך. כאן בודקים את התנהגות השירות; בהמשך נבדיל זאת מבדיקת איכות המודל. לעבור לשלושת המונחים הדומים שנפגוש: CI, CD ו-CT.

**Terminology check, not slide text:** CI includes frequent integration and automated build/test feedback. See [GitHub Docs — Continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration).

---

## Slide 4 — CI vs CD vs CT

**Estimated duration:** 5 minutes.

### Exact student-facing text

```text
CI
Continuous Integration
Check changes.
SMS API tests.

CD
Continuous Delivery
Prepare releases.
SMS service ready for approval.

CT
Continuous Training
Retrain models automatically.
Updated SMS model.
```

### Visual and layout

Arrange the three text groups in three equal columns. Each column contains an acronym, its expansion, one short explanation, and one SMS example. Use consistent typography and ample space between columns. Allow the full terms to wrap naturally. No arrows, table grid, or extra diagram. “Continuous Deployment” appears only in the instructor notes.

### Hebrew instructor notes

**זמן משוער: 5 דקות — כדקה ל-CI, שתי דקות ל-CD, דקה וחצי ל-CT, וחצי דקה לסיכום.**

- **CI:** לחזור לדוגמה המוכרת: שינוי בקוד ה-API מפעיל בדיקות. התוצאה נותנת לצוות משוב על השינוי לפני שמסתמכים עליו בגרסה חדשה. המוקד הוא בדיקת השינויים והשילוב שלהם בפרויקט.
- **CD — Continuous Delivery:** הרעיון הוא להחזיק גרסה שאפשר לשחרר כשמחליטים. בפרויקט שלנו זו יכולה להיות גרסת שירות בדוקה וארוזה שממתינה להחלטת שחרור. בקורס נשתמש באישור אנושי כדי להמחיש שחרור מבוקר. בניית Docker image היא צעד שימושי בדרך; היא לבדה אינה תהליך CD מלא ואינה אומרת שהשירות החדש כבר רץ עבור משתמשים.
- **הבהרה קצרה למרצה:** CD יכול להתייחס גם ל-Continuous Deployment: פריסה אוטומטית ל-production אחרי שהבדיקות והתנאים שנקבעו עברו. על השקף ובדיון שלנו CD פירושו Continuous Delivery. להקדיש להבחנה הזאת משפט אחד או שניים, בלי להוסיף ארכיטקטורה או מושגים חדשים לשקף.
- **CT — Continuous Training:** זהו תהליך שמאמן מחדש מודלים באופן אוטומטי בעקבות טריגר שהוגדר, למשל זמינות של נתוני SMS מתויגים חדשים. התוצר הוא מודל מעודכן שצריך להעריך לפני שימוש. בחלק הזה רק מכירים את הרעיון; בשיעור הזה נשתמש במודל שכבר אומן.
- **סיכום ומעבר:** שלושת המונחים מתארים מטרות שונות שיכולות להשתלב באותו פרויקט. אפשר להריץ CI בלי לפרוס ובלי לאמן מחדש. כעת נחבר בין המטרות לבין סוגי השינוי שיכולים להגיע לפרויקט.

**Concept checks, not slide text:** The ML-specific CI/CD/CT background follows [Google Cloud — MLOps: Continuous delivery and automation pipelines in machine learning](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning). The release-on-demand meaning of Continuous Delivery and its distinction from Continuous Deployment follow [DORA — Continuous delivery](https://dora.dev/capabilities/continuous-delivery/). The human approval step is our course example, not a universal requirement of CD.

---

## Slide 5 — What Can Change in an ML Project?

**Estimated duration:** 4 minutes.

### Exact student-facing text

```text
Application code changes: run checks.
New trained model: evaluate before release.
New labeled SMS data: validate before retraining.
```

### Visual and layout

Use three widely spaced bullets. Bold only the event at the start of each bullet. These are three examples of changes, not three sequential stages; do not connect them with arrows.

### Hebrew instructor notes

**זמן משוער: 4 דקות — כדקה לכל סוג שינוי, ועוד דקה להבחנה ביניהם ולמעבר.**

- **שינוי בקוד:** לחזור לשם השדה `label`. אפשר לשנות את מבנה התשובה ב-FastAPI בלי לגעת בקובץ המודל. במקרה הזה נרצה לבדוק שה-API עדיין עומד בציפיות של הלקוח ושאפשר לארוז את השירות.
- **מודל מאומן חדש:** ייתכן שהתקבלה גרסה חדשה של ה-Pipeline השמור, בעוד קוד ה-API נשאר זהה. לפני שחרור צריך לבחון גם את איכות החיזוי וגם את התאמת המודל לשירות. להזכיר בקצרה את precision ו-recall מהמפגשים הקודמים; לא לחשב מדדים ולא לחזור על תהליך האימון. העובדה שה-API מחזיר JSON תקין אינה מוכיחה שהמודל החדש טוב יותר.
- **נתוני SMS מתויגים חדשים:** הנתונים מצטרפים למאגר האימון, אבל המודל השמור אינו לומד מהם מעצמו. צריך לבדוק שהנתונים מתאימים, ואז להחליט מתי ואיך להפעיל אימון מחדש. בתהליך CT ההפעלה יכולה להיות אוטומטית לפי מדיניות שהוגדרה. אין כאן החלטה שכל הגעה של נתונים מפעילה מיד אימון.
- **ההבחנה:** האירוע שמגיע לפרויקט והתהליך שמופעל אחריו הם שתי החלטות שונות. שינוי בקוד ה-API, החלפת מודל ונתונים חדשים אינם מחייבים את אותה פעולה. בשיעור הזה נתרכז בנתיב הראשון: קוד שירות שהשתנה, בדיקות ובניית image עם המודל הקיים.
- **מעבר:** עכשיו אפשר להראות את המסלול המצומצם שנרצה להפעיל אוטומטית.

**Concept check, not slide text:** Different training triggers and data/model validation are discussed in [Google Cloud — ML pipeline triggers and validation](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning#ml-pipeline-triggers). The three event examples above are a teaching adaptation for this SMS project, not a universal trigger policy.

---

## Slide 6 — Our First CI Pipeline

**Estimated duration:** 5 minutes.

### Exact student-facing text

```text
Code Push
Install Dependencies
Run Tests
Build Docker Image
CI Result
Pass / Fail

Check health, response format, and invalid input.
Build after tests pass. No deployment or retraining.
```

### Visual and layout

This is the part's only workflow diagram. Use five native PowerPoint rectangles joined by four simple arrows, in this order:

`Code Push → Install Dependencies → Run Tests → Build Docker Image → CI Result`

Place “Pass / Fail” inside the final rectangle as its second line. Place the two explanatory sentences below the row, with generous spacing. The outcome rectangle summarizes the whole run: an earlier failure also produces a failed CI result; the drawing is the intended successful path, not a claim that every step executes after a failure.

Use dark labels, light neutral fills, and restrained green outlines. Do not use green alone to mean success: keep the visible outcome words. Use natural line breaks inside longer labels. Export a matching reusable SVG to `assets/diagrams/part1-ci-pipeline.svg` and keep all PPTX elements editable.

### Hebrew instructor notes

**זמן משוער: 5 דקות — דקה לסקירת המסלול, שתי דקות לבדיקות, דקה לכישלון, ודקה למשמעות התוצאה.**

- **המסלול:** `push` מפעיל את התהליך שנגדיר. סביבת הבדיקה מקבלת את הקוד ואת המודל השמור ומתקינה את התלויות המתאימות. אחר כך מריצים בדיקות, ורק אם הן עברו מנסים לבנות Docker image. זו תמונה מפושטת; הכנת Python והבאת קוד הפרויקט יופיעו כשנלמד את המימוש, בלי להוסיף עכשיו תיבות לשקף.
- **מה נבדוק:** `GET /health` צריך להחזיר HTTP 200 ו-`status` שערכו `ok`. בקשה תקינה ל-`POST /predict` צריכה להחזיר HTTP 200 ושדה `label` עם `spam` או `ham`. הודעה ריקה או הודעה שמכילה רק רווחים צריכה להידחות עם HTTP 422. להציג זאת בעל פה כשלוש ציפיות פשוטות, בלי לכתוב בדיקות או פקודות.
- **הדוגמה שמחברת הכול:** להשתמש רק ב-SMS סינתטי, למשל ״Meeting at five״. אין צורך להבטיח שהמודל יסווג את המשפט דווקא כ-`ham`. הבדיקה שאנחנו מתארים כאן בודקת שהשירות מחזיר תשובה במבנה ובטווח הערכים שהוגדרו.
- **אם משהו נכשל:** אם שינוי מ-`label` ל-`prediction` מפיל את הבדיקה, התוצאה תהיה Fail ושלב הבנייה יידלג. גם התקנת תלויות או בניית image יכולות להיכשל; לכן מעבר הבדיקות לבדו עדיין אינו אומר שכל ריצת ה-CI עברה.
- **מה אומר Pass:** הבדיקות שהוגדרו עברו וה-image נבנה בהצלחה. בנייה אינה הפעלה של container ואינה בדיקת כל התנהגות השירות בתוכו. לא פרסנו שירות חדש ולא אימנו מודל. בדיקות ה-API גם אינן מחליפות הערכת precision ו-recall על נתונים מתויגים.
- **מעבר:** זהו היעד שנבנה לאורך המפגש. לפני אוטומציה, נלמד להגדיר ציפיות ברורות בתור בדיקות.

**Project and workflow checks, not slide text:** API expectations come from the [existing Session 5 SMS API lab](../../../lab4/part2.md). Automated event-triggered build/test workflows are supported by [GitHub Docs — Understanding GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions). The tests-before-build order and skipping the build on test failure are the intended design of our course workflow, not a claim that all CI systems use this order. This draft does not claim that an image is published or retained as a release artifact.

---

## Slide 7 — What Will We Build Today?

**Estimated duration:** 2 minutes.

### Exact student-facing text

```text
Write SMS API tests with guidance.
Automate tests and the Docker build.
Solve a CI challenge independently.
```

### Visual and layout

Use three short bullets in the standard body position. Keep this as a text preview of the learning activities, with no arrows or additional workflow diagram. Emphasize the verbs “Write,” “Automate,” and “Solve.” The first two bullets belong to the same guided Lab 1; the third previews independent Lab 2.

### Hebrew instructor notes

**זמן משוער: 2 דקות.**

- **Lab 1 בהדרכה — כדקה:** להסביר ששתי השורות הראשונות הן שני שלבים של אותה מעבדה מודרכת. ב-Part 2 נדגים בדיקה קטנה, ואז הסטודנטים יכתבו ויריצו בדיקות ל-SMS API עם דוגמאות ותוצאות צפויות. ב-Part 3 נמשיך מאותם קבצים וניצור יחד workflow ב-GitHub Actions שמריץ בדיקות ובונה Docker image. בסיום Lab 1 לכל סטודנט צריך להיות CI עובד. דוגמת `label` ממחישה ציפייה שאפשר לבדוק.
- **Lab 2 עצמאי ודיון — כחצי דקה:** ב-Part 5 הסטודנטים יבחרו אתגר CI מבין כמה אפשרויות ברמת קושי דומה. הם יקבלו בעיה, מטרות וקריטריונים להצלחה, ויחליטו בעצמם איך להגיע לפתרון. אפשר להיעזר בתיעוד ולבקש רמזים בהדרגה. בסוף נשווה פתרונות ונבדוק אילו ראיות מראות שהם עובדים. אין צורך להבטיח שכולם ישברו או יתקנו בדיוק את אותו הדבר.
- **מעבר ל-Part 2 — כחצי דקה:** לומר: ״כדי שהמחשב יבדוק את השירות, קודם צריך לומר לו למה אנחנו מצפים. נתחיל בשלוש ציפיות קטנות: שירות שמגיב, תשובת חיזוי תקינה וקלט שגוי שנדחה״. כאן מסתיים Part 1. Lab 1 יתחיל ב-Part 2 וימשיך ב-Part 3; את הבעיה העצמאית נשמור ל-Part 5.

---

## Review checks

- Seven slides; the estimated durations sum to exactly 25 minutes.
- One main idea per slide and one workflow diagram, on Slide 6.
- English student-facing text; Hebrew instructor notes for every slide.
- Continuous Delivery on Slide 4; Continuous Deployment clarified only in notes.
- The hypothetical `label`/`prediction` mismatch illustrates API compatibility, without claiming that a real project change has occurred.
- One planned whole-class discussion, on Slide 2; its time is included in the 25 minutes.
- No lab, code syntax, commands, deployment implementation, or model training in Part 1.
- Slide 7 previews one guided lab across Parts 2–3 and one independent challenge with a debrief in Part 5; it does not prescribe a single final challenge implementation.
- API checks are distinguished from model-quality evaluation.
- A successful Docker build is distinguished from container execution and service deployment.
- The reference is a visual guide. Editable slides, embedded notes and matching SVGs are included in the final assembly.

**Assembly status:** Included in the final assembly. See `../FINAL_QA_REPORT.md` for executed checks and remaining hosted verification.
