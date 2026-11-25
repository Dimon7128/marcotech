# Part 3 — A simple monitoring report

> Generated from slides.json. Edit the JSON and rebuild to preserve reproducibility.

**Timing:** 35 minutes, including 25 hands-on.

## Slide 20 — A simple monitoring report

**ID:** p3-objectives  
**Layout:** objectives  
**Minutes:** 1; **hands-on:** 0

### Student-facing content

```text
Objective
Generate and interpret a simple monitoring report.
Main goals
Prepare two monitoring features.
Run Evidently and explain one chart.
State what remains unknown.
```

### Embedded Hebrew notes

**משך:** דקה אחת. לפתוח בשם החלק, במטרה ובשלוש תוצאות הלמידה.

**מטרה:** להציג את מטרת החלק: להפיק דוח ניטור ולפרש אותו. נכין שני מאפיינים מוכרים, נריץ Evidently ונזהה מה עדיין לא ידוע על תחזיות המודל.

**הנחיית הוראה:** להזכיר שהקוד מסופק ושהמיקוד הוא קריאת תרשים ומסקנה עם מגבלה. נשתמש באותם נתוני Lab 2, ללא מודל חדש וללא תוויות איכות חדשות.

**מעבר:** לעבור מההשוואה הידנית למסלול האוטומטי של הפקת דוח.

## Slide 21 — From Checks to Monitoring Reports

**ID:** p3-01  
**Layout:** diagram_takeaway  
**Minutes:** 1; **hands-on:** 0

### Student-facing content

```text
Reference SMS
+ Current SMS
Two familiar
features
Evidently
HTML report
Automated comparisons make changes easier to inspect.
```

### Embedded Hebrew notes

**משך:** דקה אחת לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** לחבר בקצרה למעבדה 2: שם השווינו שני סיכומים ידנית. כאן אותם קבצים ואותם כללי מאפיינים נכנסים לדוח. `Reference` הוא הבסיס המוקדם ו־`Current` הוא האצווה החדשה; אינם סטי אימון ומבחן.

**שאלת הוראה:** מה כלי ההשוואה יכול לחסוך? תשובה צפויה: חישוב והצגה עקביים, בלי לקבוע לבדו מה הפעולה הנכונה.

**מעבר:** נכיר ספרייה אחת, ואז נקרא דוח אמיתי שנוצר מהנתונים שלנו.

## Slide 22 — Meet Evidently

**ID:** p3-02  
**Layout:** plain_takeaway  
**Minutes:** 1; **hands-on:** 0

### Student-facing content

```text
A Python library for evaluating data and models.
Today: compare two batches using a drift report.
Start with the same two familiar features.
```

### Embedded Hebrew notes

**משך:** דקה אחת לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** `Evidently` היא ספריית Python להערכת נתונים והתנהגות מודלים, כולל שינויים בנתונים. היום משתמשים רק בדוח `DataDriftPreset` מקומי. הסביבה שנבדקה משתמשת בגרסה `0.7.23`; ההתקנה מוכנה מראש.

**גבול השיעור:** לא לפתוח שירות ענן, תשתית ניטור, מבחנים סטטיסטיים או ספים מותאמים. הקוד המלא מחכה במחברת; אין צורך לזכור את ה־API.

**מעבר:** לפני קריאת הדוח נוודא מה בדיוק הכלי מקבל.

## Slide 23 — Two Batches, Two Features

**ID:** p3-03  
**Layout:** diagram_takeaway  
**Minutes:** 1; **hands-on:** 0

### Student-facing content

```text
message_length
Numerical
Character count
has_url
Categorical
URL-like: yes / no
Use the same rules for reference and current.
```

### Embedded Hebrew notes

**משך:** דקה אחת לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** שני הקבצים הועתקו מ־Lab 2 ללא שינוי. לכל הודעה מחשבים `message_length` כמספר התווים השמורים, ו־`has_url` כ־`yes` אם הטקסט באותיות קטנות מכיל `http://`, `https://` או `www.`. זה בדיוק אותו כלל של `has_url_like`.

**דגש:** האורך מוגדר מספרי והקישור קטגוריאלי. רק שתי העמודות האלה נכנסות לכלי; לא הטקסט הגולמי, מזהים, תוויות או תחזיות. אין כאן אימון מסווג טקסט נוסף.

**מעבר:** נראה היכן שני המאפיינים מופיעים בתוצאת הרצה אמיתית.

## Slide 24 — Read the Real Report

**ID:** p3-04  
**Layout:** report_overview  
**Minutes:** 1; **hands-on:** 0

### Student-facing content

```text
Reference: earlier batch. Current: newer batch.
Both features are flagged in this prepared example.
A drift warning asks us to investigate.
```

### Embedded Hebrew notes

**משך:** דקה אחת לפי התכנון. זמן פתיחת המטרות נכלל במשך החלק ואינו תוספת למעבדה.

**הדגמה:** זו תמונה מתוך HTML שהופק בפועל עם `Evidently 0.7.23`, ולא תוצאה מאוירת. לפתוח גם את `labs/lab3/output/monitoring_report.html`. להצביע על `has_url`, `message_length`, התפלגות הבסיס, ההתפלגות החדשה וסימון `Detected`.

**שאלת הוראה:** 100% מהעמודות מסומנות — האם 100% מהתחזיות שגויות? תשובה: לא; אלו שתי עמודות נתונים בלבד, לא תחזיות עם תוויות.

**טעות נפוצה:** הממשק המלא מציג גם שיטה וציון. לא להסביר חישובים או ספים; התוצאה תלויה בשיטת הכלי ובמדגם הסינתטי הקטן.

**מעבר:** נפתח מאפיין אחד ונקרא את העמודות עם המקרא.

## Slide 25 — Explain One Chart

**ID:** p3-05  
**Layout:** report_chart  
**Minutes:** 2; **hands-on:** 0

### Student-facing content

```text
URL-like messages
Reference: 2 of 10
Current: 8 of 10
More URL-like patterns; prediction quality remains unknown.
```

### Embedded Hebrew notes

**משך:** 2 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הדגמה:** התרשים מציג את השורה `has_url` לאחר פתיחתה. ציר הספירה הוא מספר הודעות, והקטגוריה `yes` היא דפוס דמוי URL. המקרא מסמן אדום כ־`current` ואפור כ־`reference`. ב־`yes` רואים 8 לעומת 2; בשתי הקבוצות 10 הודעות, כלומר 80% לעומת 20%.

**שאלה ותשובה:** האם כל הודעה עם קישור היא spam? לא. גם הודעת שירות או עדכון מבוקש יכולה להכיל קישור; זו תכונת קלט בלבד.

**דגש:** אלה עשר הודעות סינתטיות בכל קבוצה. לא לטעון שזה שיעור אמיתי באוכלוסייה או שדיוק המודל השתנה.

**מעבר:** נסכם בדיוק איזה סוג ראיה חסר לנו.

## Slide 26 — Changed Data, Unknown Accuracy

**ID:** p3-06  
**Layout:** diagram_takeaway  
**Minutes:** 1; **hands-on:** 0

### Student-facing content

```text
Observed input change
Different feature
distributions
Prediction quality?
Need matching predictions
and reliable labels
A data drift report is not an accuracy report.
```

### Embedded Hebrew notes

**משך:** דקה אחת לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**הסבר:** הדוח מודד שינויים במאפייני קלט. כדי להעריך `precision` ו־`recall` צריך לחבר תחזיות לתוויות אמינות של אותן הודעות, במדגם מתאים. בדוח הזה אין אף אחת משתי הראיות האלה.

**שאלה ותשובה:** יותר קישורים היום — האם המודל פחות מדויק? אין מספיק מידע. אפשר לבדוק דגימה ועיבוד ולאסוף תוויות לתחזיות; לא לחשב איכות מהתרשים.

**מעבר:** עכשיו כל סטודנט יפיק או יפתח את הדוח ויכתוב פירוש קצר בעצמו.

## Slide 27 — Lab 3: Generate and Interpret

**ID:** p3-07  
**Layout:** lab  
**Minutes:** 25; **hands-on:** 25

### Student-facing content

```text
Run the supplied report.
Explain one chart and its limits.
Name the next evidence to collect.
Lab 3 guide and notebook
25 minutes
```

### Embedded Hebrew notes

**משך:** 25 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**מטרה והכנה:** להפיק דוח או לבדוק את הדוח המוכן ולהסביר שינוי אחד. להשתמש ב־`labs/lab3/README.md` ובמחברת או ב־`run_report.py`; הסביבה מותקנת לפני השיעור. אין השלמת קוד או אימון.

**חלוקת זמן:** 5 דקות טעינה וסקירת מאפיינים, 10 הפקה ופתיחת HTML, 7 פירוש התרשים ו־3 הצעת ראיה הבאה. לא להוסיף הקדמה נפרדת לזמן העבודה.

**תוצאה צפויה:** 10 הודעות בכל קבוצה; אורך ממוצע 25.4 לעומת 109.0; דפוס קישור ב־2 מתוך 10 לעומת 8 מתוך 10. שני המאפיינים מסומנים. ההגשה היא דוח שנוצר או נבדק ו־`WORKSHEET.md` קצר.

**תקלות וחלופה:** בחירת kernel שגוי או נתיב קובץ שגוי הן תקלות סבירות. אחרי כמה דקות לפתוח את ה־HTML, התמונה וסיכום המאפיינים שכבר נמצאים ב־output ולהמשיך באותן שאלות.

**התערבות ומעבר:** לשאול מה רואים ומה עדיין לא יודעים, בלי לכתוב את התשובה עבורם. בסיום לבקש ראיה קונקרטית אחת להערכת איכות ולעבור לתגובה אחרי התראה.

## Slide 28 — What Evidence Comes Next?

**ID:** p3-08  
**Layout:** plain  
**Minutes:** 2; **hands-on:** 0

### Student-facing content

```text
What changed in the input?
What would help us judge the predictions?
What should we inspect before acting?
```

### Embedded Hebrew notes

**משך:** 2 דקות לפי התכנון; לא להוסיף את זמן הפעילות שוב.

**דיון:** לבקש משני סטודנטים משפט עם תצפית ומשפט עם מגבלה. תשובה אפשרית: שיעור דפוסי URL עלה; לא ידוע אם סיווגי spam טובים פחות.

**תשובה צפויה:** לבדוק עקביות איסוף ועיבוד, ואז לאסוף תוויות אמינות למדגם מייצג ולחבר לתחזיות תואמות. שינוי בהתפלגות אינו אבחון של הסיבה.

**מעבר:** בחלק 4 לא נכתוב עוד קוד. נבחן מה עושים אחרי שקיבלנו סימן שדורש תשומת לב.

