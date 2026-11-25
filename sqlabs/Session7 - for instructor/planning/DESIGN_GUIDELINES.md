# Session 7 — Design Guidelines

**Updated:** 21 November 2026, Asia/Jerusalem  
**Basis:** Inspected Session 6 PPTX and the instructor's six confirmed A selections.  
**Status:** Applied across the final 45-slide sources. Parts 1–2 remain the preserved design baseline. The latest final-presentation request authorizes completing and integrating Parts 3–5.

Use with [SESSION7_PLAN.md](SESSION7_PLAN.md) and [DECISIONS.md](DECISIONS.md). Honor later instructor decisions and preserve approved part designs unless a change is authorized.

## Visual identity and geometry

Follow `reference/session6.pptx` closely. Preserve its restrained identity and add a subtle `Part n/5` marker to help students locate the current section. A marker is navigation, not an additional content panel.

| Property | Reference measurement / Session 7 rule |
| --- | --- |
| Canvas | 16:9, approximately 13.333 × 7.5 inches. |
| Background | White. |
| Main alignment | Left aligned, with a consistent content grid and generous whitespace. |
| Horizontal margins | Approximately 0.72 inches; usable content width about 11.89 inches. |
| Title | Aptos Display, bold, 40 pt; reference begins near x=0.72, y=0.58 inches. |
| Title accent | Short green line below title, near y=1.68 inches; approximately 0.65 inches long. |
| Body | Aptos, normally 31 pt; reference content commonly begins near y=2.2 inches. |
| Diagram/chart text | Target at least 24 pt; shorten labels or simplify the visual when needed. |
| Code/data typography | Aptos Mono when helpful; runnable code stays in lab materials. |
| Slide number | Muted, 13 pt, lower right, following the reference. |
| Part marker | Small muted or green text in consistent unused space above the title; verify fit during rendering. |
| Hebrew notes | Arial, normally 11–12 pt for notes-page rendering, with correct RTL paragraphs. |

These coordinates guide reusable layouts. Adjust within a part only when content requires it and preserve the overall grid. Do not reduce student-facing text below the target size to force excess content onto a slide. Page numbers and part markers are navigation exceptions to the content font target.

| Color role | Hex |
| --- | --- |
| Main text | `#24292D` |
| Green accent | `#196B24` |
| Secondary text | `#596269` |
| Pale green panels | `#F1F7F2` |
| Neutral panels | `#F5F6F7` |
| Light borders | `#D5DDD6` |
| Background | `#FFFFFF` |

Keep panels flat with thin borders and no decorative shadows. Use color consistently, and pair warning/action colors with text labels. Avoid using red/green alone to communicate meaning.

## Slide content and teaching language

- One slide has one main idea. Use a short, concrete title and normally 1–3 short statements or bullets.
- Target approximately 10–30 student-facing body words on ordinary slides, excluding title, slide number and part marker. The reference averages about 18. Count meaningful visual labels as content when assessing density.
- Write simple English. Reuse familiar terms and explain a new monitoring term with an SMS example before adding more terminology.
- Prefer a small comparison, a useful example or a simple chart when it clarifies the idea. Avoid decorative graphics and visually repetitive sequences that add no explanation.
- Keep large tables, full reports, long paragraphs, setup instructions, complete code and advanced statistical detail outside slides.
- Follow the later Part 4 brief: discuss precision and recall qualitatively, using Lab 1 mistake types without new metric calculations. Treat spam as the positive class.
- Keep thresholds and synthetic results clearly identified as classroom examples. Avoid universal numerical retraining rules.
- Maintain distinctions among service health, data drift, concept drift and labeled prediction quality. Do not label a feature comparison as proof of concept drift or model degradation.

## Reusable layout set

Choose layouts by teaching purpose, using named shared functions rather than slide-number-specific branches.

| Layout | Intended use | Limits |
| --- | --- | --- |
| Short text | Introduce a problem, distinction, takeaway or question. | 1–3 brief statements; avoid filling whitespace for its own sake. |
| Two cards | Service/quality or reference/current comparisons. | Short labels and comparable evidence; one comparison per slide. |
| Small workflow | Explain report preparation or the response to an alert. | Prefer 3–5 short stages; use a sixth only if it remains readable. |
| SMS example | Inspect a classification or a controlled change. | Clearly synthetic text; predicted versus correct labels must be distinct. |
| Simple chart | Compare length distributions or URL-like-pattern shares. | Clear units, reference/current labels and meaningful scale; no 3D effects. |
| Report excerpt | Orient students within the actual Evidently output. | Crop to the relevant section; use editable annotations and retain the full report externally. |
| Lab brief | State goal, expected evidence and working time. | Short objective statements and a consistent time badge; instructions in the lab guide. |
| Discussion / recap | Ask students to interpret evidence or connect ideas. | Give space to the question; keep expected answers in notes or instructor materials. |

A report screenshot may illustrate the actual tool interface. Use native editable charts and shapes for teaching comparisons whenever practical; do not use screenshots to replace the complete slide.

## Native editability and reusable diagrams

- Use native PowerPoint text boxes, shapes, charts, groups and connectors wherever practical. Keep diagram labels editable; group related components for convenient reuse.
- Each meaningful teaching diagram must have an individual SVG or PNG export in `assets/diagrams/`. Prefer SVG for simple vector diagrams and retain diagram source definitions.
- Use one shared definition for native and exported diagram versions so wording, relationships and labels agree.
- Use descriptive filenames such as `part1-service-health-vs-prediction-quality.svg`, `part2-reference-vs-current.svg` or `part4-alert-response-decision.svg`. These are proposed asset names, not files already produced.
- Keep exported assets self-contained. Retain source data for charts and source definitions for workflows. Avoid external image/style dependencies in SVGs.
- Export meaningful teaching visuals, including comparison or decision diagrams, even when they also exist natively in the deck. Decorative title accents and time badges do not need separate exports.

## Embedded Hebrew instructor notes

Every teaching slide must have actual PowerPoint speaker notes. External Markdown is the authoring source and additional instructor reference; it does not replace the Notes content inside the PPTX.

Match Session 6's teaching depth while using shorter, labeled blocks. Use the following structure where it adds value:

1. **משך:** suggested time, matching the shared timing manifest.
2. **הסבר:** a simple explanation beyond the slide's visible text.
3. **דוגמה:** an SMS example, analogy or short story when useful.
4. **שאלה:** a question to ask students when useful.
5. **תשובה צפויה / טעות נפוצה:** expected answer and the relevant misunderstanding.
6. **מעבר:** the bridge to the next idea or activity.

For lab slides, also include **מטרה**, **פעולות**, **תוצר צפוי**, **תקלות נפוצות** and **חלופה**: goal, expected actions, observable completion evidence, common problems and fallback. Explain how to support students without revealing the independent investigation's answer.

Use Hebrew explanations with English technical terms and file/field names. Format RTL paragraphs and LTR technical runs carefully; inspect mixed-language ordering. Retain teaching depth in concise blocks rather than reducing the notes to a translation of slide text. Put lengthy commands, reference solutions and troubleshooting procedures in the instructor guide and point to them from notes.

The Part 1 builder protects numeric ranges with LTR markers and hyphenated technical identifiers with invisible word joiners. This keeps time ranges in order and avoids splitting record IDs across lines. Preserve that behavior when authoring later Hebrew notes, and inspect the actual rendered Notes pages.

Mark hyphenated English terms such as `URL-like` with inline backticks in the notes source to apply that protection. For standalone part decks, actual Notes pages must keep the course-wide slide numbers. The shared builder materializes the number placeholder as ordinary editable text so Part 2's Notes pages continue 8–17 rather than restarting at 1.

## Lab materials and continuity

- Target local Python. Provide Windows PowerShell and macOS/Linux setup instructions, using an isolated environment with tested dependencies.
- Use the same SMS project context and existing fitted model if execution requires predictions. Distinguish simulated response records from actual computed model output.
- Clearly mark all monitoring scenarios and SMS examples as synthetic. Use deterministic generation and document scenario intent and expected observations.
- Maintain a consistent feature definition: `message_length` counts characters; `has_url_like` records the chosen simple pattern consistently across batches. Explain the pattern's limits in lab materials.
- Keep student tasks, acceptance criteria and data separate from instructor answers. Label planned instructor files clearly, for example `INSTRUCTOR_GUIDE_HE.md` and a separate `solutions/` folder.
- Progress from fully guided Lab 1 to mostly guided Lab 2, guided tool use with independent interpretation in Lab 3, and independent investigation in Lab 4.
- Lab 4 has clear evidence deliverables and three optional hints in instructor materials. Its main success criterion is a justified decision with limitations identified, rather than a predetermined choice to retrain.
- Provide prepared HTML reports and readable data/chart fallbacks. Fallbacks support interpretation without Python execution; distinguish that path from report generation in student evidence.

## Source organization and review

Author each part under `slides/partN/`, using stable slide IDs and fields for title, student text, layout, notes, duration and asset references. Keep one shared manifest for slide order, part names and timing. The final sources contain 45 slides across five parts: 8/11/9/9/8 slides. Never hardcode the builder or checker to a fixed deck length.

The builder should share theme/layout functions across parts and support review of the currently authorized part. Preserve approved content and reconcile any manual PowerPoint edits before regeneration. Update shared decisions when the instructor changes scope or approves a part; do not redesign approved parts silently.

During review, verify:

- English slide text, readable sizes, one main idea, appropriate density, alignment and contrast.
- Exact part names, continuous numbering, the 180-minute core total and 95 minutes of actual hands-on work.
- Native editability, consistent exported diagrams and retained source definitions.
- Useful Hebrew notes on every teaching slide, correct actual Notes content and readable mixed-language rendering.
- Executed lab behavior, accurate scenario provenance, tested dependency pins and usable fallback materials.
- Rendered slides and notes pages where a renderer is available, with no clipping, overlap or unintended font substitution.

Record checks actually performed, their tools and any material limits. Never report fresh rendering, PowerPoint desktop verification or dependency compatibility based only on previous Session 6 evidence.


## Part opening slides

Each part starts with its exact name, one short objective and three main goals. The native objectives layout uses 24 pt green labels and 31 pt editable objective/goal text. Keep the opening to one minute within the existing part allocation. The same outcomes are recorded in slides/manifest.json, SESSION7_OVERVIEW.md and the student README.
