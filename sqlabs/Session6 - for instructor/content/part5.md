# Part 5 — Independent CI Challenge & Recap

**Course:** MLOps Essentials: AI Lifecycle Management  
**Session:** 6 — CI/CD for Machine Learning  
**Status:** Final assembly source, completed from the supplied Part 5 brief with the instructor's explicit authorization.  
**Slides:** 33–39.  
**Duration:** 60 minutes: 5 introduction, 47 independent work, 8 sharing/recap. An optional 15 minutes extends independent work only.  
**Lab placement:** Lab 2 — Independent Challenge. Reuse the student's completed Parts 2–3 SMS project and repository.

The final assembly schedule is 205 minutes: 25 + 40 + 50 + 30 + 60. Hands-on implementation is 107 minutes: 25 + 35 + 47. Introduction and recap are not counted as hands-on work.

The title after each slide number and its `text` block are exact English student-facing content. Visual descriptions, Hebrew notes, and timing are instructor/production material. Keep solutions and hint levels out of the student slides.

## Confirmed completion choices

- Provide three focused paths with different valid implementations: reject unexpected request fields; verify the prediction response's JSON media type; or verify CI for pull requests as well as pushes.
- The new extra-field policy is specific to Option A, not a change to every student's starting project. The baseline currently ignores extra fields.
- Require a short `CHALLENGE_REPORT.md` with the gap, change, evidence, final results, and explanation. This is a report requirement, not an implementation recipe.
- Preserve all baseline tests, the saved model, runtime dependencies, and the existing tests-before-build ordering. Do not require retraining, deployment, publishing, new credentials, or new testing frameworks.
- Students choose one main path. Additional improvements are optional, not separate labs.

## Timing overview

| Slide | Title | Minutes | Activity |
| --- | --- | ---: | --- |
| 33 | Your CI Challenge | 1 | Scenario |
| 34 | Choose Your Mission | 1.5 | Three paths |
| 35 | What Does Success Look Like? | 1 | Acceptance criteria |
| 36 | Prove Your Solution | 1.5 | Evidence expectations |
| 37 | Work Independently | 47 | Independent student work |
| 38 | Share Your Approach | 5 | Compare solutions |
| 39 | Session 6 Recap | 3 | Recap and transition |
| Total | | 60 | 5 introduction + 47 implementation + 8 review |

---

## Slide 33 — Your CI Challenge

**Estimated duration:** 1 minute.

### Exact student-facing text

```text
Our SMS CI pipeline works.
Choose one gap and make CI detect it.
Improve the same project.
```

### Visual and layout

Use three short, large statements. Emphasize “one gap” and “same project.” Do not add a new architecture, a code example, or an implementation sequence.

### Hebrew instructor notes

**זמן משוער: דקה.**

- לחבר ל-Lab 1: כבר יש לנו שירות, מודל שמור, בדיקות ו-workflow שבונה image. כעת מחפשים פער אחד בכיסוי או בהתנהגות של האוטומציה.
- לומר: ״עד עכשיו עבדנו לפי מדריך. עכשיו תקבלו בעיה וקריטריונים להצלחה, ואתם תבחרו איך לפתור ולהוכיח אותה״.
- אין להקים אפליקציה חדשה או לאמן מודל. עובדים באותו פרויקט ובמאגר האימון האישי, על branch של התרגיל.
- לעבור לשלוש המשימות בלי להציג את פתרונות המרצה או את שלושת הרמזים מראש.

---

## Slide 34 — Choose Your Mission

**Estimated duration:** 1.5 minutes.

### Exact student-facing text

```text
A: Reject unexpected request fields.
B: Verify JSON response format.
C: Verify CI on pull requests.
```

### Visual and layout

Use three equally weighted text groups. These are choices, not sequential stages. No code, YAML keys, or solution hints on the slide.

### Hebrew instructor notes

**זמן משוער: דקה וחצי.**

- **A:** לקוח עשוי לשלוח שדה לא צפוי. הדרישה החדשה היא לדחות אותו, תוך שמירה על כל הבקשות התקינות והכללים שכבר בדקנו. זהו שינוי מדיניות מכוון; ה-schema ההתחלתי מתעלם משדות נוספים.
- **B:** הבדיקות הקיימות קוראות את ה-JSON, אך אינן בודקות שהתגובה מצהירה על סוג התוכן המתאים. המשימה היא להוסיף בדיקה משמעותית ולהראות שהיא מזהה תגובה עם סוג תוכן שגוי.
- **C:** ב-Lab 1 הגדרנו push. כאן צריך להראות שגם פעילות של pull request מפעילה את אותן בדיקות ובנייה, עם ראיה של האירוע הנכון.
- כל סטודנט בוחר משימה אחת. אין לדרוש מכולם להשלים שלוש משימות, ואין להכתיב עכשיו קובץ או שורת קוד שצריך לערוך. פרטי המטרות נמצאים במדריך הסטודנט.
- **פתרונות אפשריים למרצה בלבד:** ב-A אפשר להשתמש ב-`ConfigDict(extra="forbid")` ולבדוק בקשה שה-message שלה תקין ויש בה שדה נוסף. ב-B בודקים את Content-Type, תוך התרת פרמטרים תקינים; גוף JSON עם כותרת שגויה יכול לשמש ניסוי שלילי זמני. ב-C שומרים על push ומוסיפים pull_request, ואז מוכיחים את סוג האירוע בלוגים. קוד מלא נמצא במדריך המרצה; לא להציג אותו לסטודנטים בתחילת העבודה.

---

## Slide 35 — What Does Success Look Like?

**Estimated duration:** 1 minute.

### Exact student-facing text

```text
Define a meaningful improvement.
Keep existing checks passing.
Finish with passing CI and a successful Docker build.
```

### Visual and layout

Use three short checklist items as editable text. Do not add the full assessment rubric to the slide.

### Hebrew instructor notes

**זמן משוער: דקה.**

- להדגיש שהצלחה היא שיפור עם הסבר וראיות, ולא רק צבע ירוק או מספר גדול יותר של assertions.
- כל הבדיקות מהתרגיל המודרך צריכות להישאר. אין להחליף את תוצאת החיזוי הרצויה ב-TODO, לקבע תווית אקראית, לדלג על בדיקות או להסתיר כישלון כדי להגיע ל-build.
- מספר הבדיקות הסופי תלוי בפתרון: A ו-B עשויים להוסיף פונקציה או מקרים, ואילו C יכול לשמור על חמש הפונקציות ולהרחיב את האירועים שמפעילים אותן.
- הסטודנט צריך להראות גם את לוג הבדיקות וגם את לוג הבנייה של אותו commit סופי.

---

## Slide 36 — Prove Your Solution

**Estimated duration:** 1.5 minutes.

### Exact student-facing text

```text
Show detection or before-and-after verification.
Link the failing and passing evidence.
Explain what changed and why.
```

### Visual and layout

Use three short evidence goals. Keep this as text; the student guide carries the report requirements. No full example solution or terminal transcript on the slide.

### Hebrew instructor notes

**זמן משוער: דקה וחצי.**

- לבקש ראיה שמחוברת לשיפור שנבחר. כישלון מקרי בהתקנת חבילה אינו מוכיח שבדיקת response חדשה מזהה את הבעיה שלה.
- A יכול להראות דרישה חדשה שנכשלת לפני שינוי המדיניות ועוברת אחריו. B יכול להראות שבדיקה חדשה מגלה שינוי מבוקר בסוג התגובה. אין למסור עכשיו את קוד השינוי המבוקר.
- ב-C נדרשת ראיה שההרצה הופעלה על ידי pull request, ולא רק push שהיה קיים מלכתחילה. אפשר לצרף בדיקת כישלון מבוקרת כדי להראות שה-build נחסם ושחוזרים להצלחה לאחר תיקון.
- העבודה נעשית ב-branch ובמאגר האימון האישי. אין צורך להכניס תקלה ל-main משותף, לבצע merge או לפרוס שירות.
- ההסבר והקישורים יישמרו בדוח קצר בשם `CHALLENGE_REPORT.md`. כאשר GitHub אינו זמין, מתעדים תוצאות מקומיות ומציינים במפורש שהראיה מההרצה המתארחת עדיין חסרה.

---

## Slide 37 — Work Independently

**Estimated duration:** 47 minutes of independent student work. An optional 15-minute extension is added here, not to the introductory slides.

### Exact student-facing text

```text
Investigate, experiment, and use documentation.
Ask for a hint when needed.
Work on your own training branch.

47 minutes
```

### Visual and layout

Use three short statements and a small timing label. Keep the slide visible while students use the separate challenge brief. No numbered implementation plan, complete code, or hints on the slide.

### Hebrew instructor notes

**זמן משוער: 47 דקות עבודה עצמאית; אפשר להוסיף עד 15 דקות לפי הצורך.**

- להפנות ל-[מדריך האתגר](<../../Session6 - for students/LAB2.md>). לתת זמן לקריאה ולבחירת מטרה, ואז להימנע מהדגמה כיתתית שמכתיבה את הפתרון.
- בתחילת העבודה לבקש מכל סטודנט לנסח במשפט איזה פער הוא בודק ואיזו תוצאה תוכיח זאת. לעזור להקטין משימה גדולה מדי למשימה אחת עם ראיה ברורה.
- לא לחשוף מראש את הפתרונות. ב-[מדריך המרצה](../labs/final-lab/INSTRUCTOR_GUIDE.md) יש שלושה רמזים לכל אפשרות: כיוון, מושג, ורמז ממוקד. לתת רמז אחד לפי הצורך, אחרי שניתנה אפשרות לחקור, ולבקש מהסטודנט להמשיך משם.
- בזמן שעוברים בין הסטודנטים, לשאול מה נשלח, למה ציפו, ומה התקבל; או איזה אירוע הפעיל את ההרצה ואיזה commit נבדק. לא לערוך עבורם מיד את כל הקוד.
- להזכיר במהלך הזמן שנותר לשמור ראיות ולוודא שהגרסה הסופית עוברת. אין צורך בפתרונות זהים, ואין להכריח סטודנט מהיר לקחת משימה נוספת; אפשר להציע שיפור תואם כרמת stretch.
- אם אין GitHub, לשמור על פתרון עצמאי עם pytest ו-Docker מקומיים היכן שאפשר. דוגמאות הלוגים מ-Lab 1 הן חומר קריאה בלבד, לא הוכחה שהשיפור של הסטודנט עבד. ב-C לתעד את התנהגות האירוע שעדיין טעונה בדיקה מתארחת.
- כאשר הזמן מסתיים, עוברים לשיתוף פתרונות. אין להוסיף משימת deployment, אימון או הגדרת secrets.
- **רמז ראשון — כיוון:** ב-A לשאול מה קורה לשדה הנוסף כיום; ב-B מה ההבדל בין גוף לתיאור שלו בכותרות; ב-C איזה אירוע הפעיל את ההרצה שמוצגת.
- **רמז שני — מושג:** להפנות לפי הבחירה להגדרות extra של Pydantic, ל-response.headers, או לרשימת האירועים של GitHub. לתת זמן לחפש ולנסות לפני הרמז הבא.
- **רמז שלישי — ממוקד:** ב-A לבדוק את מדיניות forbid בלי למחוק כללי אורך; ב-B להשוות את סוג המדיה לפני `;`; ב-C להוסיף pull_request ל-on ולבחור ראיה מהרצת PR. לא להדביק את הפתרון המלא במקום הסטודנט.

---

## Slide 38 — Share Your Approach

**Estimated duration:** 5 minutes.

### Exact student-facing text

```text
What did you improve?
What evidence proves it works?
Compare different valid solutions.
```

### Visual and layout

Use three large discussion prompts. Do not show the instructor's code solution while students are explaining their own choices.

### Hebrew instructor notes

**זמן משוער: 5 דקות.**

- לבחור שתיים או שלוש הצגות קצרות, רצוי ממשימות שונות. לבקש מכל מציג לתאר את הפער, את הבחירה שעשה ואת הראיה החשובה ביותר.
- להשוות בין פתרונות לפי התוצאה והבדיקות, ולא לפי התאמה לשורות של פתרון המרצה. אם שני פתרונות עומדים בדרישות, להראות מה כל אחד מדגיש.
- שאלות מועילות: ״מה הבדיקה החדשה תפסה שהקוד הקודם לא בדק?״, ״איך יודעים שזו הרצת pull request?״, ״מה קרה ל-build כשהבדיקה נכשלה?״.
- להבהיר אם מישהו השלים רק הוכחה מקומית ולא ריצת GitHub. זו הבחנה בראיות, לא סיבה להמציא תוצאת CI.
- לסיים בחיבור לרעיון של CI: שינוי קטן, ציפייה ברורה ומשוב שאפשר לחזור עליו.

---

## Slide 39 — Session 6 Recap

**Estimated duration:** 3 minutes.

### Exact student-facing text

```text
CI checks changes.
CD concerns releases.
CT retrains models.
Tests protect API behavior; GitHub Actions runs checks and builds images.
Next: monitoring.
```

### Visual and layout

Use the three short acronym definitions as one compact group, the testing/automation sentence beneath, and the next-topic line at the bottom of the body area. Preserve readability; do not add new theory or a large summary table.

### Hebrew instructor notes

**זמן משוער: 3 דקות.**

- לחזור לשאלה המרכזית: איך בודקים ואורזים את שירות החיזוי אוטומטית אחרי שינוי קוד. היום חיברנו בין ציפיות מה-API, בדיקות pytest, הרצה ב-GitHub Actions ובניית Docker image.
- CI נותן משוב על שינויים; CD עוסק בהכנה ושחרור; CT עוסק באימון מחדש. ב-workflow של השיעור לא אימנו מודל ולא פרסנו שירות.
- להזכיר שבדיקות API אינן מדידת precision או recall, ושהרצה ירוקה אינה מבטיחה שכל בעיה בסביבת ההפעלה התגלתה. זו הסיבה לקשר שהכרנו בין CI לשחרור ולבדיקות אחרי שחרור.
- להדגיש את המעבר מליווי מלא לפתרון עצמאי: הסטודנטים בחרו בעיה, יצרו ראיה שהבדיקה או ה-workflow מזהים אותה, ותיעדו תוצאה סופית.
- המעבר למפגש הבא: ניטור יעזור לזהות בעיות כאשר השירות כבר פועל ומשתמשים שולחים אליו נתונים. לא מוסיפים כאן כלי ניטור או תרגיל חדש.

---

## Independent lab materials

- [Student challenge](../labs/final-lab/CHALLENGE.md): goals, choices, acceptance criteria, evidence and documentation; no solution recipe.
- [Hebrew instructor guide](../labs/final-lab/INSTRUCTOR_GUIDE.md): reference approaches, code examples, three progressive hints per path, expected behavior and discussion questions.

Reference checks must be recorded honestly in `FINAL_QA_REPORT.md`. Local tests, local Docker builds, static YAML inspection and actual hosted runs are separate evidence categories. No hosted run may be claimed from a sample log.
