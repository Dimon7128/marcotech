# Part 4 — What happens after an alert?

> Generated from slides.json. Edit the JSON and rebuild to preserve reproducibility.

**Timing:** 30 minutes, including 0 hands-on.

## Slide 29 — What happens after an alert?

**ID:** p4-objectives  
**Layout:** objectives  
**Minutes:** 1; **hands-on:** 0

### Student-facing content

```text
Objective
Choose a response to a monitoring alert.
Main goals
Inspect data and processing.
Assess available quality evidence.
Justify monitoring, investigation or retraining.
```

### Embedded Hebrew notes

**משך:** דקה אחת. לפתוח בשם החלק, במטרה ובשלוש תוצאות הלמידה.

**מטרה:** להציג את מטרת החלק: לבחור תגובה להתראה על בסיס ראיות. נבדוק נתונים ועיבוד, נבחן אם קיימת ראיית איכות וננמק המשך ניטור, חקירה או שקילת אימון מחדש.

**הנחיית הוראה:** זהו חלק של הסבר ודיון, ללא מעבדה או חישוב מדדים חדשים. אין תגובה אוטומטית של אימון ופריסה; ההחלטה תותאם למה שידוע ולמה שחסר.

**מעבר:** לעבור לשאלה: קיבלנו התראה, מה בודקים עכשיו?

## Slide 30 — We Detected Drift. Now What?

**ID:** p4-01  
**Layout:** plain_takeaway  
**Minutes:** 4; **hands-on:** 0

### Student-facing content

```text
The report flags changed input patterns.
Is the change expected, harmful, or a bug?
Treat the alert as a reason to inspect.
```

### Embedded Hebrew notes

**משך:** 4 דקות לפי התכנון. זמן פתיחת המטרות נכלל במשך החלק ואינו תוספת למעבדה.

**פתיחה:** לקשר לדוח הקודם: ידוע שהנתונים השתנו לפי שתי תכונות; לא ידוע למה והאם התחזיות נפגעו. יחד עם פתיחת המטרות, אלו חמש דקות להבנת ההתראה; אין כאן מעבדה נוספת.

**דוגמה:** יותר הודעות עדכון עם קישורים עשויות להיות שינוי שימוש אמיתי, שינוי דגימה, או בעיה בדרך עיבוד הנתונים. אלו השערות אפשריות, לא אבחנה שהדוח מספק.

**שאלת הוראה:** איזו ראיה תעזור להבדיל בין ההסברים? לקבל הצעות כמו בדיקת דוגמאות סינתטיות, גרסאות עיבוד, דגימה ותוויות. להזכיר שהרצה התקינה לא מוכיחה איכות.

**מעבר:** נשתמש בארבעה צעדים קצרים כדי למנוע קפיצה מהתראה ישר לאימון מחדש.

## Slide 31 — Inspect Before Acting

**ID:** p4-02  
**Layout:** diagram_takeaway  
**Minutes:** 3; **hands-on:** 0

### Student-facing content

```text
Detect
a warning
Inspect
the evidence
Understand
possible causes
Decide
the next action
Match each action to the evidence you actually have.
```

### Embedded Hebrew notes

**משך:** 3 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** לעבור על `Detect → Inspect → Understand → Decide`. זיהוי אומר שיש אות, בדיקה אוספת ראיות, הבנה משווה הסברים, וההחלטה מותאמת לרמת הביטחון. אפשר לחזור משלב ההבנה לבדיקה נוספת.

**דוגמה:** לבדוק איזה מאפיין ואיזו תקופה השתנו, האם מקור הדגימה זהה והאם עוד חלקים בשירות מצביעים על תקלה. לוודא שלא החלפנו בטעות Reference ו־Current.

**שאלה ותשובה:** האם שלב Decide תמיד אומר לשנות את המודל? לא; גם המשך ניטור או חקירה הם פעולות מנומקות.

**מעבר:** נפריד בין שינוי אמיתי בקלט לבין בעיה בתהליך המדידה או העיבוד.

## Slide 32 — Input Change or Processing Bug?

**ID:** p4-03  
**Layout:** diagram_takeaway  
**Minutes:** 4; **hands-on:** 0

### Student-facing content

```text
Real input change
Different incoming
messages
Collection or processing bug
Different sampling
or feature calculation
Verify the pipeline before proposing model changes.
```

### Embedded Hebrew notes

**משך:** 4 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** משמאל יש שינוי אמיתי בסוג ההודעות הנכנסות, למשל יותר תזכורות עם קישורים. מימין יש דגימה אחרת או חישוב מאפיין שהשתנה, למשל חיבור שתי הודעות יחד. אלו הסברים אפשריים שיכולים גם להופיע יחד.

**בדיקות מעשיות:** להשוות חלון זמן, מקור, סכמת CSV, ערכים חסרים וכלל הספירה של URL ואורך. לבדוק שינויי קוד סביב זמן ההתראה ולהשתמש בדוגמאות סינתטיות להשוואת שלבים.

**שאלה ותשובה:** מצאנו באג בספירה — האם צריך קודם לאמן מודל? לא; לתקן את המדידה ולחשב מחדש, ואז לבדוק מה נשאר לא מוסבר.

**מעבר:** גם מיקום חישוב המאפיינים קובע אילו תקלות בכלל אפשר לראות.

## Slide 33 — Where Did We Measure?

**ID:** p4-04  
**Layout:** diagram_takeaway  
**Minutes:** 3; **hands-on:** 0

### Student-facing content

```text
Captured input text
Length and URL checks
happen here
Inside the model pipeline
A later processing bug
may stay invisible
A monitor sees only the stage it measures.
```

### Embedded Hebrew notes

**משך:** 3 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** במעבדות מחשבים מאפיינים מהטקסט שנשמר לפני עיבוד ה־TF-IDF. אם באג נמצא בהמשך, למשל עיבוד טקסט שונה בתוך צינור המודל, מאפייני הטקסט הגולמי יכולים להישאר ללא שינוי.

**דוגמה:** אם הלוג חיבר שתי הודעות לטקסט אחד, ייתכן שהאורך במדידה כן ישתנה. אם התקלה רק בהמרה מאוחרת לתכונות המודל, בדיקת קלט לבדה עלולה להחמיץ אותה. המיקום והמסלול המשותף קובעים.

**שאלת הוראה:** דוח drift רגוע — האם כל העיבוד בהכרח תקין? לא; נדרשות בדיקות נוספות ושלמות נתיב העיבוד.

**מעבר:** אחרי בדיקת הנתונים והעיבוד, נשאל אם יש ראיה ישירה לאיכות תחזיות.

## Slide 34 — Do We Have Quality Evidence?

**ID:** p4-05  
**Layout:** plain_takeaway  
**Minutes:** 3; **hands-on:** 0

### Student-facing content

```text
Match predictions to reliable correct labels.
Missed spam hurts recall.
Legitimate messages blocked as spam hurt precision.
Check a representative sample before judging quality.
```

### Embedded Hebrew notes

**משך:** 3 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** אין חישוב מדדים חדש בחלק הזה. להשתמש רק במשמעות איכותית של `precision` ו־`recall`, כאשר המחלקה החיובית היא spam. להזכיר את Lab 1: `sms-01` היה spam אמיתי שנחזה ham; `sms-04` היה ham אמיתי שנחזה spam.

**ראיה נדרשת:** לתעד תחזית ותווית אמינה לאותה הודעה ובאותה תקופה, לבדוק מדגם מייצג ולהשוות לקו בסיס מתאים. מקרים בודדים הם סיבה לבדיקה ולא הוכחה לשינוי עקבי.

**טעות נפוצה:** יותר תחזיות spam או יותר קישורים אינם מדד איכות ללא אמת להשוואה. אם התוויות עדיין חסרות, נאמר במפורש שאיכות התחזיות לא ידועה.

**מעבר:** כעת נבחר בין שלוש תגובות אפשריות לפי מה שכן ידוע.

## Slide 35 — Three Possible Actions

**ID:** p4-06  
**Layout:** diagram_takeaway  
**Minutes:** 4; **hands-on:** 0

### Student-facing content

```text
Keep
monitoring
Stable quality;
change understood
Investigate
further
Missing evidence;
cause unclear
Consider
retraining
Quality loss
needs a remedy
Retraining is a considered response, never an automatic one.
```

### Embedded Hebrew notes

**משך:** 4 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** להמשיך לנטר כשמבינים את השינוי וראיות האיכות יציבות. לחקור כשהסיבה או איכות התחזיות אינן ידועות. לשקול אימון מחדש כאשר יש ראיה לפגיעה באיכות ושינוי מודל הוא פתרון סביר לאחר בדיקת תקלות.

**ניואנס:** הקטגוריות אינן פקודה לכבות שירות. אפשר להשאיר את המודל הקיים פעיל בזמן חקירה, בהתאם להשפעה ולראיות. המשך ניטור פעיל שונה מהתעלמות מהתראה.

**שאלה ותשובה:** האם drift לבדו מספיק כדי להחליף מודל? לא. אם נמצא באג יש לתקן אותו; אם איכות נפגעה צריך עדיין להבין למה ולבדוק פתרון.

**מעבר:** גם כשיש הצדקה למועמד חדש, הוא צריך לעבור בדיקה לפני שחרור.

## Slide 36 — A Candidate Must Earn Its Release

**ID:** p4-07  
**Layout:** diagram_takeaway  
**Minutes:** 3; **hands-on:** 0

### Student-facing content

```text
Candidate
model
Evaluate
& compare
Approve
the evidence
Deploy
a candidate
Monitor
after release
Compare on suitable validation data before approving release.
```

### Embedded Hebrew notes

**משך:** 3 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** התהליך העקרוני הוא מועמד, הערכה והשוואה למודל הקיים, אישור, פריסה וניטור. בחלק הזה אין אימון או פקודות פריסה. ההערכה צריכה להשתמש בנתוני validation מתאימים, כולל דוגמאות רלוונטיות לשימוש החדש וקריטריונים מוסכמים.

**דגש:** לא לבחור או לאשר מועמד לפי סט המבחן הסופי של UCI שנשמר ללא מגע. המטרה היא להימנע מהתאמת החלטות למבחן. גם מועמד טוב יותר דורש אישור ובדיקה אחרי שחרור.

**שאלה ותשובה:** מועמד נראה טוב במדגם קטן — האם נשחרר מיד? לא; נבדוק ראיות מתאימות, השוואה וקריטריונים לפני אישור.

**מעבר:** ניישם את שיקול הדעת על אירוע קצר, ללא קוד חדש.

## Slide 37 — Choose the Next Action

**ID:** p4-08  
**Layout:** plain_takeaway  
**Minutes:** 5; **hands-on:** 0

### Student-facing content

```text
HTTP 200. Normal latency. More URL-like messages.
Reliable labels are not available.
A: Ignore. B: Investigate. C: Retrain and deploy.
Choose an action and name the missing evidence.
```

### Embedded Hebrew notes

**משך:** 5 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**תרחיש:** אירוע סינתטי: השירות זמין וזמן התגובה רגיל, דוח מצביע על יותר דפוסי קישור, אין עדיין תוויות אמינות ואין באג שאומת. אין ראיה ישירה לירידה באיכות.

**הנחיית דיון:** דקה לקריאה ובחירה, שתי דקות להצדקה, דקה לשאלה מה ישנה את ההחלטה, ודקת סיכום. לבקש הצבעה לפני חשיפת התשובה. זו פעילות דיון בתוך 30 דקות החלק, ללא מעבדה נפרדת.

**תשובה צפויה:** B: לחקור, לבדוק דגימה ועיבוד ולאסוף תוויות ותחזיות תואמות. אפשר להמשיך לשרת בקיים תוך חקירה פעילה. A מתעלמת מהמידע ו־C קופצת לפתרון ללא ראיה ואישור.

**שאלת המשך:** מה ישנה את ההחלטה? באג מאומת יוביל לתיקון; איכות יציבה ושינוי מוסבר יכולים להצדיק ניטור; פגיעה עקבית באיכות יכולה להצדיק שקילת מועמד והערכה.

**מעבר:** במעבדה האחרונה כל אחד יחקור אירוע אחר וימסור המלצה קצרה עם אי־הוודאות שלה.

