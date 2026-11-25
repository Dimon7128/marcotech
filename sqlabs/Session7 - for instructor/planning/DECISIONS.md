# Session 7 — Current decisions

Updated 21 November 2026. The latest request authorizes adding each part’s objective/name/main goals, creating the instructor folder alongside the existing student folder, and removing irrelevant files using Session 6 as the reference.

1. Preserve the Session 6 visual style: white 16:9 slides, Aptos typography, restrained green accents and native editable content.
2. Use English slides and practical embedded Hebrew instructor notes with RTL paragraphs and English technical terms.
3. Start each part with its exact name, objective and three main goals. Use the same outcomes in SESSION7_OVERVIEW.md and the student README.
4. Keep all 40 existing teaching/lab slides. Add five one-minute objectives slides and renumber continuously to 45. Transfer one minute from existing teaching time in each part; the 180-minute total and 95 hands-on minutes remain unchanged.
5. Keep the four-lab progression and existing SMS project. Do not train a model, configure infrastructure or touch the final UCI test set. All new data and incidents are synthetic.
6. Use the tested Evidently 0.7.23 reporting implementation with only character count and URL-like presence. Data drift alone does not prove worse predictions or justify automatic retraining.
7. Use two teaching folders, as in Session 6: Session7 - for instructor and Session7 - for students. Root README is the entry point. Instructor keys, speaker notes and authoring tools stay in the instructor folder.
8. Retain the final PPTX/PDF, current sources, actual reports, required data, answers and small QA records. Remove disposable local environments, caches, duplicate archives, obsolete partial decks and generated inspection files. The original teaching files were backed up outside the course folder before cleanup.
9. Keep a local copy of the current Session 6 reference so presentation regeneration works after both sessions’ reorganizations. Retain editable notebooks and a focused deterministic Lab 4 CSV generator; remove superseded one-off authoring scripts.

Technical QA and visual review are recorded in FINAL_QA_REPORT.md. No PowerPoint desktop, student Windows/macOS execution or live classroom timing is inferred from those checks.
