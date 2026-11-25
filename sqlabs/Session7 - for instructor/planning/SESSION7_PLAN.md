# Session 7 — Current teaching plan

**Scope:** beginner monitoring and maintenance for the existing SMS spam project. English slides and embedded Hebrew notes. All exercise data and operational facts are synthetic; no training, deployment or untouched UCI test-set use.

**Timing:** 180 minutes, including 95 minutes hands-on. The one-minute objectives slide in each part uses that part’s existing teaching allocation. Breaks and setup are additional.

## Objectives and goals

See [SESSION7_OVERVIEW.md](../SESSION7_OVERVIEW.md) for each part’s name, objective and three main goals.

## Slide order and timing

| Slide | Stable ID | Title | Minutes | Hands-on |
| ---: | --- | --- | ---: | ---: |
| 1 | p1-objectives | What should we monitor? | 1 | 0 |
| 2 | p1-01 | Is the API Healthy? | 2 | 0 |
| 3 | p1-02 | HTTP 200, Wrong Prediction | 3 | 0 |
| 4 | p1-03 | Service Health vs Prediction Quality | 2 | 0 |
| 5 | p1-04 | Signals Beyond HTTP | 2 | 0 |
| 6 | p1-05 | Monitor Without Private Messages | 2 | 0 |
| 7 | p1-06 | Lab 1: Healthy API, Wrong Prediction | 11 | 10 |
| 8 | p1-07 | What Did Health Checks Miss? | 2 | 0 |
| 9 | p2-objectives | Drift in SMS messages | 1 | 0 |
| 10 | p2-01 | Today's SMS Looks Different | 1 | 0 |
| 11 | p2-02 | Data Drift | 2 | 0 |
| 12 | p2-03 | Concept Drift | 2 | 0 |
| 13 | p2-04 | A Pattern, Different Labels | 3 | 0 |
| 14 | p2-05 | Two Different Changes | 2 | 0 |
| 15 | p2-06 | Drift Is a Warning | 2 | 0 |
| 16 | p2-07 | Message Length | 1 | 0 |
| 17 | p2-08 | URL-like Patterns | 1 | 0 |
| 18 | p2-09 | Lab 2: Spot the Drift | 16 | 15 |
| 19 | p2-10 | What Changed? What Is Still Unknown? | 4 | 0 |
| 20 | p3-objectives | A simple monitoring report | 1 | 0 |
| 21 | p3-01 | From Checks to Monitoring Reports | 1 | 0 |
| 22 | p3-02 | Meet Evidently | 1 | 0 |
| 23 | p3-03 | Two Batches, Two Features | 1 | 0 |
| 24 | p3-04 | Read the Real Report | 1 | 0 |
| 25 | p3-05 | Explain One Chart | 2 | 0 |
| 26 | p3-06 | Changed Data, Unknown Accuracy | 1 | 0 |
| 27 | p3-07 | Lab 3: Generate and Interpret | 25 | 25 |
| 28 | p3-08 | What Evidence Comes Next? | 2 | 0 |
| 29 | p4-objectives | What happens after an alert? | 1 | 0 |
| 30 | p4-01 | We Detected Drift. Now What? | 4 | 0 |
| 31 | p4-02 | Inspect Before Acting | 3 | 0 |
| 32 | p4-03 | Input Change or Processing Bug? | 4 | 0 |
| 33 | p4-04 | Where Did We Measure? | 3 | 0 |
| 34 | p4-05 | Do We Have Quality Evidence? | 3 | 0 |
| 35 | p4-06 | Three Possible Actions | 4 | 0 |
| 36 | p4-07 | A Candidate Must Earn Its Release | 3 | 0 |
| 37 | p4-08 | Choose the Next Action | 5 | 0 |
| 38 | p5-objectives | Guided lab and recap | 1 | 0 |
| 39 | p5-01 | Your Monitoring Incident | 1 | 0 |
| 40 | p5-02 | Mission and Deliverables | 3 | 0 |
| 41 | p5-03 | Read the Incident, Inspect the Data | 15 | 15 |
| 42 | p5-04 | Generate, Then Explain the Report | 20 | 20 |
| 43 | p5-05 | Choose and Justify an Action | 10 | 10 |
| 44 | p5-06 | Share Findings and Recap | 3 | 0 |
| 45 | p5-07 | Carry Evidence into Session 8 | 2 | 0 |

## Lab progression

1. Lab 1: 10 minutes inspecting simulated responses against known scenario labels.
2. Lab 2: 15 minutes comparing message length and URL-like frequency, with one supplied mean calculation to complete.
3. Lab 3: 25 minutes generating and interpreting a report; stages 5/10/7/3 minutes.
4. Lab 4: 45 minutes independently investigating a distinct incident; stages 5/10/10/10/10 minutes. Submit a report and a 3–5 sentence decision.

## Evidence and decision boundaries

Service health is not prediction quality. Feature drift does not establish concept drift or worse accuracy. New quality evaluation requires matching predictions and reliable labels. Check collection, processing and monitoring location before acting. Keep monitoring, investigate or consider retraining according to evidence; never automatically train or release a candidate. Part 4 discusses precision/recall qualitatively without new calculations. Evaluate any future candidate using appropriate validation data, approval and monitoring; do not select using the untouched final test set.
