# Part 2 — Essential Tests

**Course:** MLOps Essentials: AI Lifecycle Management  
**Session:** 6 — CI/CD for Machine Learning  
**Status:** Final assembly source; generation authorized by the final assembly request.  
**Slides:** 8–17.  
**Duration:** 40 minutes: 15 minutes of explanation/live demonstration and 25 minutes of guided student work.  
**Lab placement:** Lab 1 — Guided Learning, Stage A. Part 3 continues the same service, model, and tests.

The final assembly request sets Part 2 to 40 minutes. Explanation and demonstration take 15 minutes; the full 25-minute guided exercise is preserved. The complete session is 205 minutes, including 107 minutes of hands-on implementation (52.2%).

The title after each slide number and the contents of its `text` block are the exact English slide text. Layout descriptions, timings, Hebrew notes, and source checks are production/instructor material. Code explicitly identified in a layout remains editable text in the approved PPTX. Only slide numbers may be added as footers.

## Interview decisions and proposed validation extension

- Use a self-contained copy of the Session 5 API and one shared saved model under `Session6 - for students/sms-service/`.
- Provide Windows PowerShell and macOS/Linux setup instructions.
- Expand schema teaching: required fields, expected types, trimming, length constraints, and the difference between valid JSON and valid API input.
- Preserve the MLOPS worksheet's existing `message` field, `min_length=1`, routes, response fields, and `spam`/`ham` labels.
- **Guided application policy:** add `max_length=500` after whitespace trimming. This is an application policy chosen for the exercise, not an SMS standard or a model-quality threshold. The existing API does not currently enforce this maximum.
- Cover missing, empty, whitespace-only, null, and numeric input, then test the new length boundary: 500 accepted, 501 rejected.
- Finish with three core test functions plus two boundary test functions: **five passing tests**. Multiple invalid payloads are checked inside one simple test function; they are not separately collected pytest cases.

## Design

Continue Part 1's visual direction: 16:9, white background, dark Aptos body text, Aptos Display titles, predictable left alignment, generous whitespace, and restrained green accents. Prefer 40–44 pt titles and 28–32 pt body text. Use a monospace font for the few essential code lines. No large code blocks, screenshots, or new workflow diagram are needed in this part.

## Timing overview

| Slide | Title | Minutes | Activity |
| --- | --- | ---: | --- |
| 8 | API Tests vs Model Evaluation | 1.5 | Explanation |
| 9 | A Schema Defines Valid Input | 1.5 | Explanation |
| 10 | Add an API Input Limit | 1.5 | Explanation |
| 11 | Test 1: Health Check | 1 | Explain expected behavior |
| 12 | Test 2: Valid Prediction | 1.5 | Explain expected behavior |
| 13 | Test 3: Invalid Input | 1.5 | Explain schema cases |
| 14 | Meet pytest | 1.5 | Introduce assertions |
| 15 | FastAPI TestClient | 2 | Explain the test setup |
| 16 | Run and Understand Your Tests | 3 | Live passing/failing demonstration |
| 17 | Guided Lab 1: Test the SMS API | 25 | Guided student implementation |
| Total | | 40 | 15 minutes explanation/demo + 25 minutes hands-on |

---

## Slide 8 — API Tests vs Model Evaluation

**Estimated duration:** 1.5 minutes.

### Exact student-facing text

```text
API tests: Does the service behave correctly?
Model evaluation: How well does it classify SMS messages?
A good model can have a broken API.
```

### Visual and layout

Use two short, stacked comparison statements and a brief takeaway below. Emphasize “API tests” and “Model evaluation.” No table, diagram, or metric calculations.

### Hebrew instructor notes

**זמן משוער: דקה וחצי.**

- לחזור לדוגמת `label` מ-Part 1: המודל עשוי לסווג נכון, אבל שינוי בשם השדה עלול למנוע מהלקוח לקרוא את התשובה. זהו כישלון של ממשק השירות.
- להבחין בין שתי שאלות: האם השירות מקבל בקשה ומחזיר תשובה לפי הכללים, והאם החיזויים שלו טובים על אוסף הודעות מתויגות. accuracy, precision ו-recall שייכים לשאלה השנייה; לא נחשב אותם בחלק הזה.
- לומר: ״היום נבדוק שהשירות מגיב, מחזיר מבנה צפוי ודוחה קלט לא מתאים. אלה בדיקות חשובות, אבל הן לא מבטיחות איכות חיזוי״.
- להדגיש שהחזרת אחת התוויות המותרות אינה מוכיחה שההודעה סווגה נכון. לעבור לכללים שמגדירים מה השירות אמור לקבל.

---

## Slide 9 — A Schema Defines Valid Input

**Estimated duration:** 1.5 minutes.

### Exact student-facing text

```text
A schema defines accepted fields, types, and rules.
message: required text.
Trim spaces; reject empty text.
```

### Visual and layout

Use one definition followed by two short rules. Emphasize `message` as a field name. Do not show the complete Pydantic class here; it belongs in the lab guide.

### Hebrew instructor notes

**זמן משוער: דקה וחצי.**

- להסביר schema בתור תיאור של הקלט שה-API מקבל: אילו שדות נדרשים, איזה סוג ערך מותר, ואילו מגבלות חלות עליו. אפשר להשוות לטופס עם שדה חובה וכללי מילוי.
- בפרויקט שלנו `SMSRequest` הוא מודל Pydantic שמתאר את הבקשה. `message` הוא שדה נדרש מסוג `str`. מספר או `null` אינם הודעת טקסט תקינה עבור המודל הזה.
- `strip_whitespace=True` מסיר רווחים מהקצוות. לאחר מכן `min_length=1` דורש שיישאר לפחות תו אחד. לכן הודעה של רווחים בלבד נדחית גם אם מחרוזת ה-JSON המקורית אינה ריקה.
- להבהיר: JSON יכול להיות תקין מבחינה תחבירית ובכל זאת לא להתאים ל-schema. לדוגמה, גוף עם `message` מספרי אינו עומד בסוג המצופה. כאן אין צורך ב-regex או בכתיבת validator מותאם.
- מעבר: נוסיף כלל אפליקטיבי אחד ונכתוב בדיקות שמוכיחות שהוא נאכף.

**Source check, not slide text:** The string type and whitespace/length constraints follow [Pydantic — StringConstraints](https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints). The existing project uses the class shown in the [Session 5 API worksheet](../../../lab4/part2.md).

---

## Slide 10 — Add an API Input Limit

**Estimated duration:** 1.5 minutes.

### Exact student-facing text

```text
Our API allows up to 500 characters after trimming.
Test the boundary: 500 accepted; 501 rejected.
```

### Visual and layout

Use two large statements. Emphasize 500 and 501. This slide describes the proposed lab policy; it does not claim that the Session 5 service already has this rule. No additional diagram or code block.

### Hebrew instructor notes

**זמן משוער: דקה וחצי.**

- להציג את הכלל בתור דרישה חדשה לתרגול: `max_length=500`. זהו גבול שאנחנו בוחרים ל-API של הכיתה. אין להציג אותו בתור מגבלה תקנית של SMS או כלל שמוכיח איכות חיזוי.
- בקוד ההתחלתי יש מינימום אורך, אך אין עדיין מקסימום. הסטודנטים יוסיפו את הכלל בעותק המעבדה בלבד. השמות `message` ו-`label` והמודל השמור יישארו כפי שהם.
- להסביר בדיקת גבול בעזרת מקרה אחד שמותר ומקרה סמוך שאסור: 500 תווים צריכים להתקבל, ו-501 צריכים להידחות. כך אפשר לגלות גם טעות שבה הגבול עצמו נדחה בטעות.
- בספירת האורך משתמשים בטקסט אחרי הסרת רווחים מהקצוות. בבדיקות נשתמש במחרוזות סינתטיות ללא רווחים כדי שהגבול יהיה ברור.
- מעבר: נתחיל משלוש ההתנהגויות הבסיסיות, ואז נרחיב את הבדיקות לכלל החדש.

---

## Slide 11 — Test 1: Health Check

**Estimated duration:** 1 minute.

### Exact student-facing text

```text
Confirm the API responds.
GET /health returns HTTP 200 and status: ok.
```

### Visual and layout

Use one purpose statement and one expected result. Format `/health` and `status: ok` consistently as technical text. No full test function on the slide.

### Hebrew instructor notes

**זמן משוער: דקה.**

- להסביר שזו הבדיקה הפשוטה ביותר לקריאה: שולחים בקשה ל-`/health`, ואז בודקים את קוד התגובה ואת גוף ה-JSON המצופה, `{"status": "ok"}`.
- להפריד בין שליחת בקשה לבין בדיקה: שליחת הבקשה נותנת תוצאה; ה-assertions משווים אותה לציפייה שהגדרנו.
- להדגיש ש-HTTP 200 אומר שהבקשה הצליחה. בדיקת שדה `status` מוסיפה בדיקה של התוכן, אבל גם היא אינה מודדת דיוק של מודל או מוכיחה שכל השירותים בעולם זמינים.
- במימוש שלנו המודל נטען בעת import של האפליקציה. אם הקובץ חסר, הבעיה תופיע עוד לפני הרצת בדיקת ה-health. נחזור לכך בהכנת סביבת המעבדה.

---

## Slide 12 — Test 2: Valid Prediction

**Estimated duration:** 1.5 minutes.

### Exact student-facing text

```text
Send a synthetic SMS to POST /predict.
Expect HTTP 200 and label: spam or ham.
```

### Visual and layout

Use two short statements. Emphasize the required response field `label`. Keep the complete request and test code in the lab guide.

### Hebrew instructor notes

**זמן משוער: דקה וחצי.**

- להשתמש בדוגמה הסינתטית ״Meeting at five״. ה-TestClient ישלח אותה בגוף JSON עם השדה `message`.
- להציג בעל פה שלוש ציפיות: התקבל HTTP 200, בתשובה קיים `label`, וערכו הוא אחת משתי התוויות המותרות, `spam` או `ham`.
- אין לדרוש מהמשפט הזה דווקא `ham`. זו בדיקת תקינות של השירות והערכים שהוא מחזיר, ולא בדיקה של ביצועי מודל מסוים על דוגמה עם תווית אמת ידועה.
- לקשר לדוגמה מ-Part 1: אם השרת יחזיר `prediction` במקום `label`, הבדיקה תגלה שהחוזה עם הלקוח השתנה.
- במעבדה הסטודנטים ישלימו בעצמם את קבוצת התוויות ב-assertion קצר. להסביר שהקבוצה מתארת את שני הערכים המותרים ולא את איכות הניבוי.

---

## Slide 13 — Test 3: Invalid Input

**Estimated duration:** 1.5 minutes.

### Exact student-facing text

```text
Missing or null message: HTTP 422.
Numbers instead of text: HTTP 422.
Blank or overlong text: HTTP 422.
```

### Visual and layout

Use three bullets grouped by the rule being checked. “Overlong” refers to the proposed 500-character lab policy. Keep payload examples and error JSON in the guide or instructor demonstration.

### Hebrew instructor notes

**זמן משוער: דקה וחצי.**

- לקשר כל סוג קלט לכלל: שדה חסר מפר דרישת חובה; `null` או מספר אינם `str`; טקסט ריק או רווחים בלבד מפרים את המינימום אחרי trimming.
- הודעה ארוכה מדי תידחה רק אחרי שנוסיף במעבדה את `max_length=500`. לפני השינוי זו אינה מגבלה קיימת, ולכן נצפה שבדיקת הדרישה החדשה תיכשל.
- FastAPI משתמש ב-schema של הבקשה כדי להחזיר HTTP 422 כאשר הקלט אינו עומד בכללים. דחיית בקשה לא תקינה היא ההתנהגות הרצויה, ולכן בדיקה שמצפה ל-422 יכולה לעבור.
- בשגיאת validation אפשר לראות על איזה שדה הייתה הבעיה. אין צורך להעתיק לבדיקה את כל טקסט השגיאה, שעלול להשתנות בין גרסאות.
- במעבדה נריץ אותו מבנה של בקשה ו-assertion על כמה payloads באמצעות לולאה פשוטה. לא נלמד כאן parametrization או validators מתקדמים.

**Source check, not slide text:** Validation uses the inspected application schema and [FastAPI — Handling errors](https://fastapi.tiangolo.com/tutorial/handling-errors/). Missing/empty/whitespace-only HTTP 422 responses were observed on the completed Session 5 service; type and candidate length constraints were also checked directly with the installed Pydantic version. The new maximum has not been applied to any project API.

---

## Slide 14 — Meet pytest

**Estimated duration:** 1.5 minutes.

### Exact student-facing text

```text
pytest runs functions named test_*.
assert checks an expectation.
assert response.status_code == 200
```

### Visual and layout

Use two explanatory lines and one native editable monospace code line. The code line is an example, not a complete test function. Keep it large and left-aligned.

### Hebrew instructor notes

**זמן משוער: דקה וחצי.**

- להציג pytest בתור הכלי שמוצא ומריץ את הבדיקות ומסכם את התוצאות. בקבצים שלנו שמות הפונקציות מתחילים ב-`test_`, ושם הקובץ יהיה `test_api.py`.
- להסביר את השורה בשפה פשוטה: ״אנחנו מצפים שקוד התגובה יהיה 200״. `==` משווה ערכים; הוא אינו קובע מה ה-API יחזיר.
- אם הציפייה מתקיימת, הפונקציה ממשיכה. אם assertion נכשל, pytest מסמן את הבדיקה כ-Fail ומראה את ההשוואה. בדיקה עם כמה assertions עוברת רק אם כולם עוברים.
- להדגיש את ההבדל בין `assert` לבין `print`: הדפסה יכולה לעזור לראות תוצאה, אבל אינה מגדירה בעצמה תנאי הצלחה לבדיקה.
- אין צורך במחלקות, fixtures או תיאוריה כללית של סוגי בדיקות. מיד נחבר את הציפיות לבקשות ל-FastAPI.

**Source check, not slide text:** Test discovery and assertion reporting follow [pytest — Get started](https://docs.pytest.org/en/stable/getting-started.html).

---

## Slide 15 — FastAPI TestClient

**Estimated duration:** 2 minutes.

### Exact student-facing text

```text
TestClient calls our app without starting Uvicorn.
The saved model is still required.
client = TestClient(app)
```

### Visual and layout

Use two explanatory lines and one native editable monospace setup line. No network diagram or server screenshot is needed.

### Hebrew instructor notes

**זמן משוער: 2 דקות.**

- להציג את TestClient כלקוח בדיקה שפונה ישירות לאובייקט `app`. הוא מאפשר להשתמש בבקשות כמו `get` ו-`post`, בלי להפעיל Uvicorn ובלי לבחור port.
- בשונה מהבדיקה הידנית ב-`/docs`, כאן הבקשה והציפיות כתובות בקובץ וניתנות להרצה חוזרת. נשתמש בפונקציות `def` רגילות ובבקשות סינכרוניות.
- להדגיש שזהו השירות האמיתי שלנו בתהליך הבדיקה, עם המודל השמור. TestClient אינו מבטל את הצורך בקובץ `model.joblib`, ואיננו מחליפים את המודל ב-mock או מאמנים אותו מחדש.
- ב-starter נייבא `app` מתוך `main.py`. ה-import טוען גם את המודל. לכן בודקים מראש שהקובץ קיים ושהתלויות תואמות לסביבת האימון.
- סביבת התרגול תוסיף pytest ואת `httpx`, שבו TestClient משתמש. אין צורך להתקין כלי API נוסף או להפעיל Docker בחלק הזה.

**Source check, not slide text:** Setup and synchronous request examples follow [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/), including the `httpx` dependency.

---

## Slide 16 — Run and Understand Your Tests

**Estimated duration:** 3 minutes, live demonstration.

### Exact student-facing text

```text
Run python -m pytest -q.
A failure shows the test, assertion, and actual value.
Read the mismatch before editing.
```

### Visual and layout

Use three short text lines. Keep command text editable. Show actual execution in the instructor's terminal rather than embedding a terminal screenshot or a long failure trace in the slide.

### Hebrew instructor notes

**זמן משוער: 3 דקות.**

- **הכנה מראש:** לפתוח terminal בתיקיית ה-starter `sms-service/` ולהפעיל את סביבת ה-Python. קובצי ה-starter נמצאים בחומרי המעבדה; לבדוק מראש את סביבת ההדגמה. ההוראות המלאות נמצאות ב-[מדריך המרצה](../labs/lab1/instructor_notes_he.md).
- **כ-40 שניות:** להראות את `test_health` ולהריץ `python -m pytest -q test_api.py::test_health`. להצביע על שליחת הבקשה ועל שתי הציפיות. התוצאה צריכה להיות `1 passed`.
- **כ-45 שניות:** לשנות זמנית רק את הציפייה של קוד התגובה מ-200 ל-201. להריץ שוב את אותה בדיקה. נקבל כישלון: השירות החזיר 200, בעוד הבדיקה ציפתה ל-201. השירות לא שונה; בכוונה כתבנו ציפייה שגויה.
- **כ-40 שניות:** לקרוא יחד את שם הבדיקה, שורת ה-assert ואת הערכים שהושוו. להדגיש שתוצאת כישלון היא ראיה לבדיקה, ולא הוראה לשנות את השרת באופן אוטומטי.
- **כ-55 שניות:** להחזיר את הציפייה ל-200, להריץ שוב ולהראות הצלחה. להסביר שבמהלך המעבדה נראה גם כישלון אחר: בדיקה של כלל אורך חדש לפני שהוספנו אותו. שם הציפייה מייצגת דרישה חדשה, ולכן נעדכן את ה-schema בעותק המעבדה.
- לא להריץ בשלב הזה בטעות את כל ה-starter ולהציג את ה-TODO של בדיקת החיזוי בתור באג ב-API. זו משימה שהסטודנטים ישלימו כעת.

---

## Slide 17 — Guided Lab 1: Test the SMS API

**Estimated duration:** 25 minutes of guided student work. This includes reading the lab goals, implementation, checkpoints, and the final local run; do not add another 25-minute lab block after this slide.

### Exact student-facing text

```text
Complete the label assertion.
Add and test the message-length limit.
Finish with five passing tests.

25 minutes
```

### Visual and layout

Use the first three lines as clear goals and place “25 minutes” in a small timing label. Keep the slide visible while students use the separate lab guide. No full instructions, code, QR placeholder, or unverified external lab URL on the slide.

### Hebrew instructor notes

**זמן משוער: 25 דקות של עבודה מודרכת.**

- **המטרה:** כל סטודנט עובד בעותק עצמאי של אותו API ובאותו מודל שסופק לכיתה. מסיימים עם שלוש בדיקות בסיסיות ושתי בדיקות גבול, כולן עוברות. זהו Stage A של Lab 1, ולא מעבדה חדשה נפרדת ממה שנמשיך ב-Part 3.
- **חלוקת זמן:** 3 דקות להכנה ול-import של האפליקציה, 4 דקות לבדיקת health, 5 דקות להשלמת בדיקת החיזוי, 6 דקות לבדיקות schema קיימות, ו-7 דקות להוספת כלל האורך ולבדיקת הגבולות. להפנות ל-[מדריך הסטודנט](<../../Session6 - for students/LAB1.md>), ולשמור את [מדריך המרצה](../labs/lab1/instructor_notes_he.md) פתוח לעזרה.
- **הדרכה:** תחילה לוודא שהסטודנטים מבינים מה כל assertion מוכיח. אם יש קושי, לבקש מהם לזהות את הבקשה, את התגובה ואת הערך המצופה לפני שמציעים תיקון. אין צורך שכל אחד יקליד מחדש קוד שכבר סופק; משימת ההשלמה וכלל האורך דורשים פעולה והסבר מצדם.
- **תוצאות ביניים:** תחילה `1 passed` לבדיקת health בלבד. לאחר תיקון קבוצת התוויות ובדיקת הקלט הקיים נקבל `3 passed`. שתי בדיקות הגבול מוסיפות שתי פונקציות; לפני `max_length=500` נצפה ל-`1 failed, 4 passed`, ואחריו ל-`5 passed`.
- **עזרה נפוצה:** כישלון בזמן import הוא בדרך כלל בעיית קובץ מודל, תיקייה או תלות, ולא assertion שגוי. בקשות ריקות אמורות לקבל HTTP 422; זהו מצב תקין כאשר לכך הבדיקה מצפה. הדוגמה הסינתטית אינה חייבת לקבל דווקא `ham`.
- **סיום ומעבר:** לוודא שה-TODO הוחלף, שהציפייה הזמנית 201 הוסרה, ושנשמרו `main.py`, `test_api.py` והתלויות. ב-Part 3 נריץ את אותם קבצים ב-GitHub Actions ונבנה Docker image. לא משנים מודל או schema נוסף בין החלקים.
- אם יש תקלה בתשתית או צורך בתרגול נוסף, להאריך את העבודה ולתעד את הזמן. אין לקצר את האתגר העצמאי ב-Part 5 כדי להשלים כאן פערים.

---

## Starter-file specification

The starter paths in this specification are relative to the outer `session6/` folder.

These are proposed files for the generation stage. Only Markdown documents are being created now.

| File | Proposed source or change |
| --- | --- |
| `Session6 - for students/sms-service/main.py` | Start with the complete API code from `MLOPS/lab4/part2.md`, including `min_length=1`. Students add the proposed `max_length=500` in the guided exercise. Do not modify the historical Session 5 sources. |
| `Session6 - for students/sms-service/model.joblib` | Provide the already trained shared artifact from the inspected completed Session 5 service. Its Pipeline contains `TfidfVectorizer` and `MultinomialNB`; no training is added. |
| `Session6 - for students/sms-service/requirements.txt` | Preserve the existing Session 5 runtime pins, including the ML package versions. |
| `Session6 - for students/sms-service/requirements-dev.txt` | Include the runtime requirements and add proposed development pins `pytest==8.4.2` and `httpx==0.28.1`. Both releases exist on PyPI and were tested with the supplied runtime requirements; see the QA report. |
| `Session6 - for students/sms-service/test_api.py` | Three core starter functions, with one deliberate label-assertion TODO. Students add two boundary tests from the guide. |
| `Session6 - for students/sms-service/dockerfile` | Preserve the existing Session 5 Dockerfile for continuation in Part 3; no Docker commands are taught in Part 2. |
| `Session6 - for students/sms-service/.dockerignore` | Preserve the inspected Session 5 file alongside the Dockerfile. |
| `Session6 - for students/sms-service/.gitignore` | Exclude `.venv/`, `__pycache__/`, and `.pytest_cache/` in preparation for Part 3. |

## Technical review and scope checks

- The starter follows `MLOPS/lab4/part2.md`, preserving `min_length=1`. The separate completed historical service uses 2; its schema was not silently copied.
- The supplied saved Pipeline and existing runtime dependency pins are reused without retraining. The lab's starter and completed solution are separate, so the original Session 5 sources remain intact.
- The five completed pytest functions, deliberate TODO failure, pre-limit boundary failure and controlled health-assertion failure were executed in an isolated Python 3.10 Docker environment. All produced the expected results.
- The 500-character policy is measured after trimming and was verified with additional padded-boundary requests. It is an application policy, not an SMS standard.
- The final requested Part 2 schedule is 40 minutes: 15 explanation/demo and 25 hands-on. Exact English slide text is preserved from the earlier draft.
- [Final QA report](../FINAL_QA_REPORT.md) records executed checks, dependency versions and verification limits.

---

## Production appendix — starter content

This appendix records the distributed starter. It is production source, not an additional student exercise. The generated files are in `Session6 - for students/sms-service/`.

### Starting `main.py`

Use the complete MLOPS Session 5 worksheet code, with no maximum initially:

```python
from pathlib import Path
from typing import Annotated

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints

app = FastAPI(title="SMS Classifier")
pipeline = joblib.load(Path(__file__).with_name("model.joblib"))


class SMSRequest(BaseModel):
    message: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=1
    )]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: SMSRequest):
    label = str(pipeline.predict([payload.message])[0])
    return {"label": label}
```

The final student version differs only by adding `max_length=500` to the constraint list. The selected model is already trained; it is not created by this exercise.

### Starting `test_api.py`

The generated starter has exactly three core functions and one deliberate TODO. The two boundary functions are added during the guided exercise.

```python
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_prediction():
    response = client.post("/predict", json={"message": "Meeting at five"})
    assert response.status_code == 200
    assert "label" in response.json()
    assert response.json()["label"] in {"TODO"}, "Complete the allowed-label assertion"


def test_invalid_input():
    invalid_payloads = [
        {},
        {"message": ""},
        {"message": "   "},
    ]
    for payload in invalid_payloads:
        response = client.post("/predict", json=payload)
        assert response.status_code == 422, payload
```

### Dependency files and carry-over files

Keep the existing runtime pins in `requirements.txt`:

```text
pandas==2.2.3
scikit-learn==1.7.2
joblib==1.5.3
fastapi==0.128.2
uvicorn==0.48.0
```

Add `requirements-dev.txt` with the same three lines used in [Step 1 of the student guide](../labs/lab1/part2_api_testing.md#1-prepare-the-test-environment):

```text
-r requirements.txt
pytest==8.4.2
httpx==0.28.1
```

These development pins refer to the verified releases [pytest 8.4.2](https://pypi.org/project/pytest/8.4.2/) and [HTTPX 0.28.1](https://pypi.org/project/httpx/0.28.1/); they are reproducibility choices, not claims to be the latest versions.

Copy `model.joblib`, lowercase `dockerfile`, and `.dockerignore` from the inspected completed Session 5 service at `/home/dima/git/marcotech/sqlabs/lab4/docker/sms-service/`. Preserve the Docker files for Part 3 without teaching or running Docker commands here.

The reviewed shared model has SHA-256 `265bd0ba388c1e7ba3c827593d15dda611ea1b57696668658f311fd8c83326b0`. Recheck provenance and compatibility if that source artifact changes before generation.

Create `.gitignore` with:

```text
.venv/
__pycache__/
.pytest_cache/
```

### Verification checklist

- Generate the approved files in the new lab folder; preserve the original Session 5 service and model.
- Verify installation and TestClient behavior in a clean Python 3.10 environment without using packages from the existing instructor environment.
- Confirm the health-only pass, deliberate TODO failure, three-core-test pass after completion, length-rule failure before implementation, and final five-test pass.
- Confirm that missing/empty/whitespace-only/null/numeric/overlong payloads produce HTTP 422 and the exact maximum remains accepted.
- Verify that the setup instructions point to the real generated working folder and the carried-over Dockerfile still packages the same service/model.
- Keep full solutions and instructor guidance separate from the student starter. Part 3 must reuse these files and the final schema.
