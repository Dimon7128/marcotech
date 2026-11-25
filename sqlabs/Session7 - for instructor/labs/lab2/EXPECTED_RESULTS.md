# Lab 2 — Prepared results and fallback

**Synthetic teaching scenarios only.** Values below come from executing the completed student exercise on the supplied CSVs. The batches contain no true labels or model predictions.

If Python is unavailable, inspect one original message from each CSV, compare the following values, and answer WORKSHEET.md.

| Feature | Reference | Current |
| --- | ---: | ---: |
| Messages | 10 | 10 |
| Average message length, characters | 25.4 | 109.0 |
| URL-like messages, count | 2 | 8 |
| URL-like messages, % | 20.0 | 80.0 |

Lengths include spaces and punctuation. URL-like means a case-insensitive substring match for `http://`, `https://` or `www.`. It is an approximate input descriptor.

## Check individual records

| Batch | Record | Length, characters | URL-like |
| --- | --- | ---: | --- |
| Reference | ref-01 | 13 | False |
| Reference | ref-02 | 17 | False |
| Reference | ref-03 | 25 | False |
| Reference | ref-04 | 26 | False |
| Reference | ref-05 | 22 | False |
| Reference | ref-06 | 21 | False |
| Reference | ref-07 | 27 | False |
| Reference | ref-08 | 32 | False |
| Reference | ref-09 | 31 | True |
| Reference | ref-10 | 40 | True |
| Current | cur-01 | 46 | True |
| Current | cur-02 | 47 | True |
| Current | cur-03 | 127 | True |
| Current | cur-04 | 122 | True |
| Current | cur-05 | 122 | True |
| Current | cur-06 | 121 | True |
| Current | cur-07 | 125 | True |
| Current | cur-08 | 128 | True |
| Current | cur-09 | 128 | False |
| Current | cur-10 | 124 | False |

## Your interpretation

Use the same questions as the Python path: what changed; whether this supports data drift; whether accuracy or concept drift is established; and what additional evidence would help.

These are descriptive results for two small planned scenarios. They are not a statistical test or measurements of changes in UCI or production traffic.
