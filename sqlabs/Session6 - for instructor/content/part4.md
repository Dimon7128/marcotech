# Part 4 — From CI Result to a Release

**Course:** MLOps Essentials: AI Lifecycle Management  
**Session:** 6 — CI/CD for Machine Learning  
**Status:** Final assembly source; generation authorized by the final assembly request.  
**Slides:** 27–32.  
**Duration:** 30 minutes, including the final classroom discussion.  
**Lab placement:** None. This is a conceptual bridge between guided Lab 1 and independent Lab 2.

The supplied brief resolves the teaching decisions: one continuous SMS example, six short slides, a controlled release story, and one decision-based final discussion. No additional interview is needed. The final session plan is 205 effective minutes, with 107 minutes of student hands-on work; the discussion here is not counted as hands-on implementation.

The title after each slide number and the contents of its `text` block are the exact English student-facing text. Layouts, timing, source checks, and Hebrew notes are instructor/production material. Only slide numbers may be added as footers. All diagrams use native editable PowerPoint elements and have reusable SVG versions.

## Continuous example and accuracy boundaries

- Imagine that the team has updated the existing SMS API, its five pytest checks pass, and the image build succeeds. These are scenario assumptions, not a claim that a hosted run has already been executed for the draft materials.
- Use the same FastAPI service, `message` request field, `label` response field, `spam`/`ham` labels, and previously trained `TfidfVectorizer` + `MultinomialNB` Pipeline.
- The illustrative update can be the 500-character input policy from Part 2. In the story, the previous application is `sms-api:v1.0` and the proposed updated application is `sms-api:v1.1`; both can contain the same saved model.
- These version tags are conceptual examples. The Part 3 workflow only builds `sms-api:ci` on its runner; it does not create, retain, publish, or deploy the illustrative release versions.
- A future release process needs to retain and make its selected image available to the release mechanism, including a previously working image for recovery. Mention this dependency without teaching a registry or artifact-storage implementation.
- A tag is a name/reference, not by itself a guarantee of immutable artifact identity. Put this qualification in the instructor notes; do not introduce image-digest details on slides.
- No new YAML, approval configuration, registry commands, deployment commands, rollback commands, infrastructure, or model training in this part.

## Design

Follow the established 16:9 reference identity: white background, dark Aptos text, Aptos Display headings, predictable left alignment, generous whitespace, and restrained green accents. Keep titles approximately 40–44 pt and body text approximately 28–32 pt.

Slide 27 uses a simple separation between the current CI result and a future release. Slide 28 uses two small version cards. Slide 32 contains the main release workflow diagram. No large tables, code blocks, screenshots, or decorative icons are needed.

## Timing overview

| Slide | Title | Minutes | Teaching focus |
| --- | --- | ---: | --- |
| 27 | CI Passed. Are We Live? | 3 | CI stops before release |
| 28 | Identify the Version | 5 | Application tag and separate model identity |
| 29 | Who Approves the Release? | 4 | A deliberate team decision |
| 30 | Smoke Test: Does It Actually Work? | 5 | Check the running released service |
| 31 | Rollback: What If Something Breaks? | 5 | Restore an available, previously working release |
| 32 | The Complete SMS Release Story | 8 | Workflow and decision-based discussion |
| Total | | 30 | Conceptual teaching and discussion; no lab |

---

## Slide 27 — CI Passed. Are We Live?

**Estimated duration:** 3 minutes.

### Exact student-facing text

```text
CI passed
Tests and image build succeeded.

Future release
Make the selected version available to users.

Our workflow stops after the build.
```

### Visual and layout

Use two simple native text-and-shape groups: the CI result on the left and the clearly labeled future release on the right. Separate them with whitespace and a short divider rather than a continuous automatic arrow. Put the final sentence below. Do not add a deploy icon or imply that our workflow crosses the gap.

### Hebrew instructor notes

**זמן משוער: 3 דקות.**

- **חיבור ל-Part 3:** לומר: ״לצורך הסיפור, נניח שההרצה ירוקה: חמש הבדיקות עברו וה-image נבנה. זה אומר שהמשימות שהגדרנו הסתיימו בהצלחה. זה עדיין לא אומר שמשתמשים מקבלים את הגרסה הזאת״.
- ה-workflow שלנו מתקין dependencies, מריץ pytest ובונה `sms-api:ci`. אין בו שלב שמפרסם image, שומר אותו כתוצר release או מפעיל שירות חדש. ה-image שעל runner זמני אינו הופך מעצמו לגרסה שזמינה לפריסה בהמשך.
- בתהליך עתידי נצטרך לשמור את ה-image שנבחר ולהפוך אותו לזמין למנגנון שיפעיל את השירות. היום רק מסבירים את הצורך; לא מוסיפים registry, פקודות או workflow נוסף.
- בסיפור הפשוט שלנו Release הוא ההחלטה והפעולה שמביאות גרסה מסוימת לשימוש המשתמשים. אפשר לחשוב על חבילה שעברה בדיקה ונארזה: עדיין צריך לבחור את החבילה ולהעביר אותה ליעד.
- **מעבר:** לפני שמחליטים לשחרר, צריך לדעת בדיוק לאיזו גרסה מתכוונים. גם את הגרסה הקודמת נרצה להצליח לזהות.

**Project check, not slide text:** The [Part 3 reference workflow](../labs/lab1/part3_github_actions.md#complete-reference-workflow) has test/build steps and no publishing, artifact-retention, release, or deployment step. [GitHub — Workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows) describes workflows as the tasks explicitly defined in their configuration; a deployment task is not implied by build success.

---

## Slide 28 — Identify the Version

**Estimated duration:** 5 minutes.

### Exact student-facing text

```text
A tag names an application image.
sms-api:v1.0
sms-api:v1.1
New API code can use the same saved model.
```

### Visual and layout

Put the definition at the top and two equal native cards below, labeled only `sms-api:v1.0` and `sms-api:v1.1`. Place the final sentence beneath the cards to connect application and model versions. These are illustrative release versions, not images claimed to exist. Avoid an additional release pipeline or a complex version table.

Save a matching reusable version-card SVG as `assets/diagrams/part4-application-versions.svg`.

### Hebrew instructor notes

**זמן משוער: 5 דקות — כשתי דקות ל-tag, שתי דקות לדוגמת API לעומת מודל, ודקה לזיהוי מדויק ולמעבר.**

- **Version Tag:** להסביר ש-`sms-api` הוא שם ה-image בדוגמה, והחלק אחרי הנקודתיים הוא ה-tag. בדוגמה שלנו `v1.0` הוא שם לגרסה קודמת ו-`v1.1` הוא שם לגרסה המוצעת. לא מלמדים כאן כללי semantic versioning או משמעות מחייבת לכל מספר.
- אלה שמות עתידיים לצורך הסיפור. ב-Part 3 הגדרנו רק `sms-api:ci`; לא נוצרו בפועל שתי גרסאות release ולא בוצע עבורן publishing.
- **הקשר לפרויקט:** אפשר לדמיין ש-`v1.1` מכיל את כלל אורך ההודעה שהוספנו בתרגול. קוד ה-API ומדיניות הקלט השתנו, אבל קובץ ה-Pipeline המאומן יכול להיות בדיוק אותו קובץ שהיה ב-`v1.0`.
- לכן יש הבדל בין application version לבין model version. שינוי ב-API אינו מחייב אימון חדש; החלפת מודל אינה מחייבת שינוי בשמות ה-endpoints. בתיעוד release עתידי נרצה לדעת גם איזו אפליקציה נבנתה וגם איזה מודל נארז בתוכה.
- **דגש למרצה:** tag הוא שם שניתן להקצות מחדש. עצם כתיבת `v1.1` אינה מבטיחה שאותו תוכן נשאר מאחוריו לנצח. לצורך שחרור אמין נשמור קשר ברור לבנייה שנבדקה ולעותק ה-image שנבחר. אין צורך להציג digests או להיכנס למנגנון הטכני בשקף.
- גם שינוי שם או tag בלבד אינו מפעיל גרסה אצל המשתמשים. הוא עוזר לזהות מה רוצים לשחרר; הפעלה היא צעד נפרד בסיפור.
- **מעבר:** אחרי שזיהינו את הגרסה, הצוות יכול לקבל החלטה לגביה ולא לדבר באופן עמום על ״העדכון האחרון״.

**Source check, not slide text:** Image tags refer to images as described in [Docker — Image tag](https://docs.docker.com/reference/cli/docker/image/tag/). Mutable versus immutable tag behavior is documented in [Docker — Immutable tags](https://docs.docker.com/docker-hub/repos/manage/hub-images/immutable-tags/). Only the basic naming concept belongs on the slide; no tag-management configuration is taught.

---

## Slide 29 — Who Approves the Release?

**Estimated duration:** 4 minutes.

### Exact student-facing text

```text
Approval: a decision to release a specific version.
Our team chooses when to release the updated SMS service.
```

### Visual and layout

Use two large left-aligned statements. Emphasize “specific version” and “when.” No GitHub Environments screenshot, approval form, role matrix, or configuration example.

### Hebrew instructor notes

**זמן משוער: 4 דקות.**

- **ההסבר:** לומר: ״הבדיקות נותנות לנו ראיות על הגרסה. הצוות עדיין צריך להחליט אם ומתי נכון להפוך אותה לגרסה שמשתמשים מקבלים״. בדוגמה שלנו מדובר בהחלטה על `sms-api:v1.1`, לא באישור כללי לכל שינוי עתידי.
- אפשר להזכיר את מדיניות הקלט החדשה: אולי הכול עובד כמתוכנן, אבל הצוות רוצה לתאם את זמן העדכון ולוודא שמי שמשתמש ב-API מבין את המגבלה החדשה. הסיבה לאישור יכולה להיות תיאום והיערכות, גם בלי כישלון טכני.
- במנגנון השחרור העתידי נרצה לדעת איזו גרסה נבחרה, מי בצוות מחליט להפעיל אותה, אילו בדיקות קצרות נעשה אחרי ההפעלה ולאיזו גרסה אפשר לחזור. אין צורך להפוך את זה לרשימת governance ארוכה או ללמד כלי אישורים.
- בקורס אנחנו בוחרים להמחיש approval אנושי. זו דרך אפשרית ל-Continuous Delivery ולשחרור מבוקר, ולא טענה שכל ארגון חייב לקבל אישור ידני בכל release.
- לא להציג הגדרות של GitHub Environments, permissions או secrets. האישור כאן הוא מושג והחלטה בסיפור; לא פעולה שמבצעים בשיעור.
- **מעבר:** גם אחרי החלטה והפעלה של הגרסה, נרצה לבדוק את השירות שבאמת רץ עבור המשתמשים.

**Conceptual background, not slide text:** The broader CI/CD/CT context follows [Google Cloud — MLOps](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning). The human approval point is our simplified course scenario, not a universal requirement or an implemented GitHub feature.

---

## Slide 30 — Smoke Test: Does It Actually Work?

**Estimated duration:** 5 minutes.

### Exact student-facing text

```text
Smoke test: a quick check of the released service.
GET /health: HTTP 200.
POST /predict: HTTP 200 and label: spam or ham.
```

### Visual and layout

Use one definition and two short request/result lines. Keep endpoint text editable. No full JSON request, shell command, live request, or additional testing taxonomy on the slide.

### Hebrew instructor notes

**זמן משוער: 5 דקות — דקה להגדרה, שתי דקות לדוגמה, ושתי דקות להבדל מול CI ולמגבלות הבדיקה.**

- **המושג:** Smoke Test הוא בדיקה קצרה של הפעולות העיקריות כדי לזהות במהירות תקלה ברורה. בסיפור שלנו מבצעים אותה אחרי שהגרסה הופעלה בסביבה שאליה שחררנו, מול כתובת השירות שרץ שם.
- **בדיקה ראשונה:** לפנות ל-`GET /health` ולבדוק HTTP 200 ו-`status` שערכו `ok`. זה מראה שהנתיב הזה מגיב; הוא אינו מוכיח שכל מסלול החיזוי תקין.
- **בדיקה שנייה:** לשלוח ל-`POST /predict` הודעה סינתטית, למשל ״Meeting at five״, בשדה `message`. לצפות ל-HTTP 200 ולשדה `label` עם `spam` או `ham`. לא מנחשים תווית אחת מדויקת ולא משתמשים ב-SMS פרטי.
- **ההבדל מול CI:** ב-Part 3 ה-TestClient בדק את האפליקציה בתוך תהליך Python על ה-runner, ואז ניסינו לבנות image. כאן בודקים את השירות שהופעל בפועל אחרי release. ב-workflow של Part 3 לא התבצע השלב הזה.
- שני סוגי הבדיקות יכולים לשלוח בקשות דומות, אבל בזמן אחר ולמערכת אחרת שרצה. ההבדל החשוב כאן הוא יעד הבדיקה: הקוד בסביבת CI לעומת השירות בסביבת השחרור.
- בדיקת health לבדה עלולה לעבור בזמן שהחיזוי נכשל. לכן מוסיפים גם בקשת חיזוי תקינה. גם שתי בקשות שעברו אינן מוכיחות precision או recall טובים ואינן מכסות כל קלט.
- ה-API הקיים אינו מחזיר מזהה release ב-`/health`. את הגרסה שהופעלה נוודא דרך רישום השחרור או מנגנון ההפעלה שנבחר בעתיד; לא נניח ששדה כזה כבר קיים בתשובה.
- **מעבר:** אם בדיקה קצרה מגלה תקלה, נרצה אפשרות לחזור למצב שעבד.

**Source and project check, not slide text:** Health and prediction behavior come from the existing SMS API and Parts 2–3. Post-deployment checks of actual application behavior are supported by [Microsoft — Testing strategies](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/testing). The source is instructor background only; no Azure service, deployment architecture, or broader testing strategy is added to the lesson.

---

## Slide 31 — Rollback: What If Something Breaks?

**Estimated duration:** 5 minutes.

### Exact student-facing text

```text
Rollback restores a previously working release.
Example: sms-api:v1.1 back to sms-api:v1.0.
Keep that previous release available.
```

### Visual and layout

Use the definition, one short version example, and one preparation statement. Reuse the typography of Slide 28's version labels. A simple native return arrow between the two illustrative version labels may replace the word “back” visually only if the visible wording remains equivalent. No rollback commands or infrastructure diagram.

### Hebrew instructor notes

**זמן משוער: 5 דקות — שתי דקות לרעיון, שתי דקות לתנאי החזרה ודקה לאימות ולמעבר.**

- **הסיפור:** נניח שהפעלנו את `sms-api:v1.1` ופתאום בקשות חיזוי תקינות נכשלות. אם `v1.0` הוא release ידוע שעבד ומתאים לחזרה, הצוות עשוי לבחור להחזיר אותו כדי לשקם את השירות בזמן שמבררים את התקלה החדשה.
- Rollback הוא החזרת השירות לגרסה קודמת שעבדה. הוא אינו מחיקת הבדיקות, אימון המודל מחדש או שינוי של tag בלי הפעלה של גרסה אחרת.
- כדי לחזור צריך שה-image הקודם והפרטים שמזהים אותו עדיין יהיו זמינים, ושיהיה מנגנון שחרור שמסוגל להפעיל את הגרסה הזאת. לא מספיק לזכור שהיה פעם שם כמו `v1.0`, ולא מניחים שה-image נשמר על runner זמני.
- ״הגרסה הקודמת״ צריכה להיות ידועה כתקינה ומתאימה, ולא רק בעלת מספר קטן יותר. בדוגמה הזאת אנחנו מניחים ש-`v1.0` אכן עבד; במסירה אמיתית צריך להסתמך על מידע מההפעלה הקודמת.
- לאחר החזרה נריץ שוב את בדיקות ה-smoke הקצרות ונבדוק שהחיזוי חזר לעבוד. פעולת rollback שהסתיימה אינה לבדה הוכחה שהבעיה נפתרה.
- חזרה אינה תגובה אוטומטית לכל הודעת שגיאה. אם הבעיה אינה נובעת מהגרסה החדשה או משפיעה גם על הגרסה הישנה, החזרה עלולה לא לעזור. נשקול ראיות והשפעה על המשתמשים, בלי להיכנס כאן לאסטרטגיות deployment מתקדמות.
- **מעבר:** נחבר את כל הסיפור ונחליט יחד מה עושים כשחיזוי מחזיר HTTP 500 אחרי השחרור.

**Concept check, not slide text:** Returning to an identified, previously healthy state and choosing recovery based on the incident are supported by [Microsoft — Incident management](https://learn.microsoft.com/en-us/azure/well-architected/design-guides/incident-management). Only these generic ideas are used; infrastructure, database recovery, and cloud-specific mechanisms remain outside scope.

---

## Slide 32 — The Complete SMS Release Story

**Estimated duration:** 8 minutes, including the class discussion and instructor explanation.

### Exact student-facing text

```text
Future workflow
CI Passes
Identify Version
Approval
Release
Smoke Test
Keep or Roll Back

POST /predict returns HTTP 500.
What should we check, and when might we roll back?
```

### Visual and layout

Use the part's main workflow diagram: six native PowerPoint rectangles connected by five arrows, in the listed order. Place “Future workflow” above the row and the two-line discussion prompt below it. Use natural line breaks in long labels, readable 24–28 pt diagram text, light fills, and dark text. Do not add a second decision tree or an implementation pipeline.

The process is conceptual. It assumes a selected image is retained and available to the future release mechanism; that preparation is explained in notes rather than falsely depicted as a completed Part 3 feature.

Export a matching reusable diagram as `assets/diagrams/part4-release-workflow.svg`, preserving native editability inside PowerPoint.

### Hebrew instructor notes

**זמן משוער: 8 דקות — שתי דקות לחיבור הסיפור, שלוש דקות לתשובות מהכיתה, שתי דקות להסבר המרצה ודקה לסיכום.**

#### הצגת הסיפור — שתי דקות

- לעבור בקצרה על הרצף: CI נתן תוצאה; זיהינו image לגרסה מסוימת; הצוות אישר את השחרור; הגרסה הופעלה; בדקנו את השירות; ולפי התוצאות משאירים אותה או שוקלים חזרה לגרסה תקינה.
- להזכיר שהחלק שממשיך אחרי build הוא תהליך עתידי שאנחנו מתארים, לא workflow שכבר הוספנו ל-GitHub. הוא דורש שהגרסאות הנבחרות יהיו זמינות להפעלה ולחזרה.

#### הדיון — שלוש דקות, לפני הצגת התשובה

- לתאר: ״אחרי release של הגרסה החדשה, משתמשים שולחים הודעות תקינות ל-`/predict` ומקבלים HTTP 500. מה כדאי לבדוק, ומתי נשקול rollback?״.
- לתת לסטודנטים להציע שתיים או שלוש תשובות לפני שמסבירים. לבקש מהם לקשר בין ההצעה לבין ראיה: איזו בקשה, איזו גרסה, איזה לוג או איזו תוצאה של smoke test יעזרו להחליט.
- זהו דיון קצר בקבלת החלטות, לא משימת troubleshooting במחשבים. לא מחלקים פקודות ולא פותחים תרגיל נוסף.

#### הסבר למרצה בלבד — שתי דקות

1. **מה אומר HTTP 500:** השרת נתקל במצב לא צפוי שמנע ממנו להשלים את הבקשה. הסטטוס לבדו אינו אומר מה הסיבה. זו אינה תווית spam שגויה, וגם לא דחיית schema צפויה עם HTTP 422.
2. **מה בודקים תחילה:** לוודא שזו בקשה תקינה, לזהות איזו גרסה הופעלה, לקרוא את הלוג הרלוונטי ולברר אם הבעיה חוזרת ומשפיעה על החיזוי למשתמשים. לבדוק health ובקשת חיזוי סינתטית מול השירות הפעיל. health תקין לצד prediction שנכשל מראה שלא די ב-health בלבד.
3. **למה CI שעבר אינו מבטיח הפעלה תקינה:** הבדיקות כיסו את הציפיות שהגדרנו בסביבת CI, וה-build הראה שאפשר לבנות image. הן לא בדקו אצלנו הפעלה של container בסביבת השחרור, ולא כיסו כל תנאי אפשרי שם. הבדל בסביבת ההפעלה או בעיה שלא נחשפה בבדיקות הם כיווני בירור, לא אבחנה מוכחת לפי 500 בלבד.
4. **מתי חזרה יכולה להתאים:** כאשר חיזויים תקינים נכשלים באופן שחוסם משתמשים אחרי העדכון, יש קשר סביר לגרסה החדשה, וקיימת גרסה תקינה זמינה עם דרך ידועה להפעיל אותה. אפשר לתת עדיפות להשבת השירות גם לפני שסיימנו ניתוח מלא של הסיבה, ואז לבדוק שוב באמצעות smoke test.
5. **למה לא תמיד חוזרים מיד:** ייתכן שהבעיה משפיעה גם על הגרסה הקודמת, שהגרסה בפועל אינה זו שחשבנו, או שיש תיקון ממוקד וברור שמתאים יותר. ההחלטה צריכה להתבסס על המידע הזמין, השפעת התקלה והיכולת לחזור בפועל; לא על כלל אוטומטי של ״כל 500 מחייב rollback״.

#### סיכום ומעבר — דקה

- לומר: ״CI עוזר לנו לבדוק שינוי ולבנות image. שחרור דורש גם זיהוי גרסה, החלטה ובדיקה של השירות שפועל. אם משהו משתבש, נרצה דרך לחזור לגרסה שעבדה״.
- לחבר להמשך: Part 5 יחזיר אותנו לעבודה עצמאית על CI, לא למימוש deployment. עכשיו חוזרים ב-Part 5 ל-CI, הפעם עם בחירה עצמאית של שיפור והוכחתו.

**Technical check, not slide text:** HTTP 500 semantics follow [RFC 9110, section 15.6.1](https://www.rfc-editor.org/rfc/rfc9110.html#name-500-internal-server-error). The diagnostic questions and rollback decision are a teaching adaptation of this SMS scenario, not a diagnosis of a real incident or a claim that deployment occurred.

---

## Review checks and generation plan

- Six slides, numbered 27–32, with estimated durations 3 + 5 + 4 + 5 + 5 + 8 = 30 minutes.
- Exact slide text is English; every slide has Hebrew instructor notes with timing, examples, distinctions, and transitions.
- One continuous SMS story links the CI result, illustrative application tags, approval, smoke testing, and rollback.
- Application and model identity are distinguished without retraining or MLflow implementation.
- The future release is clearly separated from Part 3's runner-local test/build workflow. There is no claim that its image was retained, published, deployed, or made release-ready automatically.
- Tag names are illustrative, with mutability explained only in notes. No digest lesson or release-versioning strategy is introduced.
- The smoke example checks the released API's health and one synthetic prediction, not model quality.
- Rollback requires an available, identified, previously working release and an appropriate mechanism; the class does not implement it.
- The final discussion lets students answer before the instructor explanation, includes all five requested decision points, and stays inside its eight-minute allocation.
- The final assembly includes native editable version-card and release-workflow diagrams, matching SVGs and embedded Hebrew notes. See the final QA report for rendered inspection results.
- Part 4 remains conceptual; no release lab, publishing step or deployment was added. The next part is the independent CI challenge.

**Assembly status:** Included in the final assembly. See `../FINAL_QA_REPORT.md` for executed checks and remaining hosted verification.
