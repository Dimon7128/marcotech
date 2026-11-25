# Part 5 — Guided lab and recap

> Generated from slides.json. Edit the JSON and rebuild to preserve reproducibility.

**Timing:** 55 minutes, including 45 hands-on.

## Slide 38 — Guided lab and recap

**ID:** p5-objectives  
**Layout:** objectives  
**Minutes:** 1; **hands-on:** 0

### Student-facing content

```text
Objective
Investigate an SMS incident and justify an action.
Main goals
Compare batches and interpret drift.
Separate observations from unknowns.
Submit a report and decision.
```

### Embedded Hebrew notes

**משך:** דקה אחת. לפתוח בשם החלק, במטרה ובשלוש תוצאות הלמידה.

**מטרה:** להציג את מטרת החלק: לחקור אירוע SMS חדש באופן עצמאי ולנמק פעולה. נשווה נתונים ודוח, נפריד בין תצפיות לבין אי־ודאות ונגיש דוח עם החלטה קצרה.

**הנחיית הוראה:** יש קוד עובד, דוח מוכן לחלופה ורמזים מדורגים. לא לחשוף את הפתרון. העבודה העצמאית נשארת 45 דקות, וההגשה היא דוח ופסקת החלטה קצרה.

**מעבר:** לעבור לכרטיס האירוע החדש ולהסביר מה המצב הידוע לפני החקירה.

## Slide 39 — Your Monitoring Incident

**ID:** p5-01  
**Layout:** diagram_takeaway  
**Minutes:** 1; **hands-on:** 0

### Student-facing content

```text
API healthy
HTTP 200
Normal response time
Monitoring warning
New input patterns
Quality still unknown
Investigate a new synthetic SMS incident independently.
```

### Embedded Hebrew notes

**משך:** דקה אחת לפי התכנון. זמן פתיחת המטרות נכלל במשך החלק ואינו תוספת למעבדה.

**הצגת האירוע:** זהו אירוע אחר מ־Lab 3. בכרטיס כתוב שהשירות זמין, המודל לא השתנה ואין תוויות אמינות או תחזיות תואמות. דגימה ועיבוד טרם אומתו. לא לחשוף את המספרים או ההחלטה הרצויה לפני העבודה.

**הכנה:** הקבצים והסביבה של Lab 3 מוכנים, או שהדוח והתמונות המוכנים זמינים. עבודה אישית ואפשרות לשיחה קצרה לאחר כתיבת מסקנה עצמאית. אין צורך בשירות פעיל או במודל מאומן נוסף.

**מעבר:** נגדיר מה מגישים ואיך מחלקים את 45 דקות החקירה.

## Slide 40 — Mission and Deliverables

**ID:** p5-02  
**Layout:** plain_takeaway  
**Minutes:** 3; **hands-on:** 0

### Student-facing content

```text
Inspect the incident and compare both batches.
Submit one report and a short decision worksheet.
Use evidence, acknowledge uncertainty, name a next step.
```

### Embedded Hebrew notes

**משך:** 3 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**מטרה והגשה:** לפתוח `labs/lab4/README.md`, `INCIDENT.md` ו־`submission_template.md`. להגיש HTML שהופק או נבדק ועוד כ־3–5 משפטים בחמשת השדות: שינוי, ראיה, מה לא ידוע, החלטה וצעד הבא.

**חלוקת זמן:** 45 דקות עבודה בחמישה שלבים: 5 הבנת האירוע, 10 בדיקת הנתונים, 10 הפקת דוח, 10 פירוש, 10 החלטה. שלושת שקפי העבודה הבאים מכסים 15, 20 ו־10 דקות. חמש דקות הסיום יישארו לשיתוף ולמעבר.

**תמיכה:** הקוד מלא; מוקד העבודה הוא החשיבה. להציע את `HINTS.md` רמז אחד בכל פעם, ולהשתמש בדוח המוכן אם ההתקנה מתעכבת. לציין אם השתמשו בחלופה.

**מעבר:** להתחיל בקריאה ובנתונים עצמם; לשמור את המסקנה פתוחה עד שיבחנו ראיות.

## Slide 41 — Read the Incident, Inspect the Data

**ID:** p5-03  
**Layout:** lab  
**Minutes:** 15; **hands-on:** 15

### Student-facing content

```text
Read what is known and unknown.
Compare counts, character length and URL-like share.
Lab 4: incident card and data inspection
15 minutes
```

### Embedded Hebrew notes

**משך:** 15 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**פעולות:** 5 דקות לקריאת כרטיס האירוע וזיהוי מה עובד ומה חסר, ואז 10 לטעינת שני קבצי ה־CSV ולסיכום. להשתמש במחברת או בסקריפט שסופקו; אין להשלים אלגוריתם חדש.

**תוצאה צפויה למרצה:** 200 הודעות בכל קבוצה, אורך ממוצע 75.7 תווים בשתיהן, URL ב־20 מתוך 200 לעומת 140 מתוך 200: 10% לעומת 70%. הנתונים נבנו כך שכל התפלגות האורך נשארת זהה; זו אינה טענה על אוכלוסייה אמיתית.

**רמז והתערבות:** אם מעתיקים את תשובת Lab 3, לשאול האם גם האורך השתנה כאן. אם משווים רק ספירות בלי גודל קבוצה, לבקש מכנה. דפוס קישור אינו תווית spam.

**תקלות וחלופה:** נתיב שגוי או kernel חסר: לבדוק שהנתונים בתיקיית data ושהמחברת רצה בתיקיית המעבדה. אם לא נפתר מהר, לפתוח `output/FEATURE_SUMMARY.md`.

**מעבר:** לשמור תצפית אחת ושאלה פתוחה לפני שמפיקים את הדוח.

## Slide 42 — Generate, Then Explain the Report

**ID:** p5-04  
**Layout:** lab  
**Minutes:** 20; **hands-on:** 20

### Student-facing content

```text
Open the report and inspect each feature.
Separate the observation from possible explanations.
Lab 4: 10 minutes to generate; 10 minutes to interpret
20 minutes
```

### Embedded Hebrew notes

**משך:** 20 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**פעולות:** 10 דקות להרצת הקוד ולפתיחת HTML, ואז 10 לפירוש. זו אותה גרסת `Evidently 0.7.23` ואותו helper כמו Lab 3; לא ללמד API חדש. להרחיב את השורות ולבדוק את המקרא.

**תוצאה צפויה למרצה:** הדוח בפועל מסמן `has_url` כ־`Detected` ו־`message_length` כ־`Not Detected`. עמודה אחת מתוך שתיים אינה 50% תחזיות שגויות. תרשים URL מציג `yes`: 140 ב־Current לעומת 20 ב־Reference.

**שאלות הנחיה:** מה באמת נצפה? מה עשוי להסביר אותו? האם דגימה או עיבוד נבדקו? האם יש תוויות אמינות ותחזיות תואמות? המראה של הודעת עדכון אינו תווית אמת.

**רמז והתערבות:** לתת קודם את רמז המיקום בדוח, אחר כך להשוות את שני המאפיינים, ולבסוף להזכיר את גבול הראיה. לא למסור את הפתרון המלא; לבקש מהסטודנט להפריד תצפית מהסבר.

**חלופה ומעבר:** להשתמש ב־HTML ובתמונה המוכנים אם ההפקה נכשלת. אותן שאלות ואותה הגשה. כעת לבחור פעולה עם צעד הבא קונקרטי.

## Slide 43 — Choose and Justify an Action

**ID:** p5-05  
**Layout:** lab  
**Minutes:** 10; **hands-on:** 10

### Student-facing content

```text
Keep monitoring, investigate, or consider retraining?
Give evidence, one uncertainty and a concrete next step.
Lab 4 decision worksheet: 3–5 sentences
10 minutes
```

### Embedded Hebrew notes

**משך:** 10 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**פעולות והגשה:** כל סטודנט משלים את חמשת שדות `submission_template.md` בכ־3–5 משפטים בסך הכול ושומר את הדוח שהופק או נבדק. להקדיש כשבע דקות לכתיבה ושלוש לבדיקה עצמית או שיתוף קצר.

**תשובה צפויה למרצה:** לחקור: יש יותר דפוסי קישור בלי שינוי אורך, אבל איכות התחזיות לא ידועה. לאסוף תוויות אמינות למדגם מייצג עם תחזיות ולבדוק איסוף/עיבוד. אפשר להשאיר את המודל פעיל בזמן החקירה; זה אינו התעלמות.

**קריטריונים:** לחפש שינוי נכון, ראיה עם יחידות, מגבלה מפורשת, פעולה מנומקת וצעד הבא. מי שמציע אימון מחדש צריך להסביר את הראיות שעוד חסרות ואת השוואת המועמד לפני שחרור; אין לאמן בפועל.

**תמיכה וחלופה:** אם הכתיבה מתארכת, משפט אחד יכול לכסות שני שדות. להשתמש בדוח המוכן בדיוק באותה דרך ולסמן זאת. אם נותר זמן, לשאול מה היה משנה את ההחלטה.

**מעבר:** להכין שיתוף של משפט אחד: מה ראינו, מה לא ידענו ומה נעשה.

## Slide 44 — Share Findings and Recap

**ID:** p5-06  
**Layout:** diagram_takeaway  
**Minutes:** 3; **hands-on:** 0

### Student-facing content

```text
Check
service
Compare
data
Read
the report
Investigate
the cause
Decide
and monitor
Share one finding, one uncertainty and one justified action.
```

### Embedded Hebrew notes

**משך:** 3 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**שיתוף:** לבקש שני סיכומים קצרים ולחזור על המסלול: שירות, נתונים, דוח, חקירה והחלטה. בתרחיש החדש שיעור URL עלה מ־10% ל־70% והאורך נשאר 75.7; אין נתוני איכות.

**סיכום מעשי:** HTTP 200 אינו הוכחה לתחזית נכונה. drift אינו הוכחה לירידה באיכות. בדיקת סיבה ותוויות יכולה לשנות החלטה, ואימון מחדש הוא אפשרות מותנית ולא תגובה אוטומטית.

**שאלת המשך:** איזו ראיה חדשה עשויה להצדיק פעולה אחרת? באג מאומת, איכות יציבה לאורך מדגם מתאים, או פגיעה מתמשכת באיכות. לא לדרוש מסקנה חזקה יותר מהראיות.

**מעבר:** ההגשה הקצרה הופכת למסמך החלטה שאפשר להמשיך ממנו בשלב הבא בקורס.

## Slide 45 — Carry Evidence into Session 8

**ID:** p5-07  
**Layout:** plain_takeaway  
**Minutes:** 2; **hands-on:** 0

### Student-facing content

```text
Keep your report and decision worksheet.
Record the next check and who should own it.
Monitoring decisions connect evidence to the next lifecycle step.
```

### Embedded Hebrew notes

**משך:** 2 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**סיום והעברה:** לבקש לשמור את הדוח ואת ההמלצה יחד, לציין איזו בדיקה תבוצע ומי אחראי. אלו הראיות והאי־ודאות שנעביר למפגש 8; אין להמציא כאן סדר יום שלא סוכם למפגש הבא.

**שאלת יציאה:** מהי בדיקה אחת שתבצעו לפני שינוי מודל? לקבל תשובה קונקרטית כגון אימות דגימה ועיבוד או איסוף תוויות אמינות ותחזיות תואמות.

**בדיקת הבנה:** להזכיר שההחלטה יכולה להשתנות עם ראיות חדשות. להודות על ההגשות ולסיים בזמן; הרחבה או הפסקות הן מעבר ל־180 הדקות המתוכננות.

