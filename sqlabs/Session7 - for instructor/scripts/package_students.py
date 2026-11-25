#!/usr/bin/env python3
"""Synchronize the separate student handout from an explicit student file list.

Run from the instructor folder: python scripts/package_students.py
The folder is the distribution format; no duplicate archives are produced.
"""
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
HANDOUT = ROOT.parent / 'Session7 - for students'
COMMON = ['requirements.txt','monitoring.py','run_report.py','TROUBLESHOOTING.md',
          'data/reference_sms.csv','data/current_sms.csv','output/monitoring_report.html',
          'output/FEATURE_SUMMARY.md','output/url_distribution.png']
STUDENT_FILES = {
    1: ['records.csv','WORKSHEET.md'],
    2: ['starter.py','reference.csv','current.csv','requirements.txt','WORKSHEET.md','EXPECTED_RESULTS.md'],
    3: COMMON + ['monitoring_report.ipynb','WORKSHEET.md'],
    4: COMMON + ['monitoring_incident.ipynb','INCIDENT.md','HINTS.md','submission_template.md'],
}


def main():
    HANDOUT.mkdir(exist_ok=True)
    for number, relatives in STUDENT_FILES.items():
        source = ROOT / f'labs/lab{number}'
        target = HANDOUT / f'lab{number}'
        for relative in relatives:
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if number == 2 and relative == 'starter.py':
                path.write_text((source/relative).read_text().replace('See README.md','See ../LAB2.md'))
            else:
                shutil.copyfile(source/relative, path)
        guide = (source/'README.md').read_text()
        guide = re.sub(r'\]\((?!https?://|#)([^)]+)\)', lambda match: f'](lab{number}/{match.group(1)})', guide)
        guide = guide.replace('from this lab folder:', f'from the `lab{number}/` folder:')
        (HANDOUT/f'LAB{number}.md').write_text(guide, encoding='utf-8')
    manifest = json.loads((ROOT/'slides/manifest.json').read_text())
    lines = ['# Session 7 — Start here', '',
             'Use this folder for all four labs. Work on your own copy and keep your answers.', '',
             'All SMS, incidents and service facts are synthetic classroom examples. No live API, trained model, AWS, Docker or GitHub setup is needed.', '',
             '## Parts, objectives and main goals', '',
             '| Part | Objective | Main goals |', '| --- | --- | --- |']
    for entry in manifest['parts']:
        lines.append(f'| {entry["part"]}. {entry["title"]} | {entry["objective"]} | {"; ".join(goal.rstrip(".") for goal in entry["main_goals"])}. |')
    lines += ['', '## Work in this order', '',
              '| Guide | Working folder | Hands-on time | Task |', '| --- | --- | ---: | --- |',
              '| [LAB1.md](LAB1.md) | lab1/ | 10 min | Find incorrect classifications despite HTTP 200. |',
              '| [LAB2.md](LAB2.md) | lab2/ | 15 min | Complete one mean calculation and compare SMS features. |',
              '| [LAB3.md](LAB3.md) | lab3/ | 25 min | Generate or inspect a report and explain one chart. |',
              '| [LAB4.md](LAB4.md) | lab4/ | 45 min | Investigate a new incident and justify an action. |', '',
              'The complete session is 180 minutes, including 95 minutes of hands-on work. Prepare Python 3.10 and the pinned packages before class for Labs 2–4. Lab 1 needs only a spreadsheet or text editor. Use a separate environment from the existing saved model.', '',
              'Open each working folder in your editor and run that guide’s commands there. Keep the supplied folder structure. Notebook cells use their lab folder as the working directory; run_report.py also works from elsewhere.', '',
              '## File guide', '',
              '| Files | Use |', '| --- | --- |',
              '| LAB1.md–LAB4.md | Setup, timing, tasks and fallback instructions. |',
              '| lab1/records.csv, WORKSHEET.md | Six simulated requests and an answer sheet. |',
              '| lab2/starter.py, reference.csv, current.csv | Supplied features with one TODO and two ten-message batches. |',
              '| lab2/requirements.txt, WORKSHEET.md, EXPECTED_RESULTS.md | Setup, interpretation and calculated fallback. |',
              '| lab3/monitoring_report.ipynb, lab4/monitoring_incident.ipynb | Short complete notebooks. |',
              '| lab3/ and lab4/monitoring.py, run_report.py | Feature/report code and complete runnable scripts. |',
              '| lab3/ and lab4/requirements.txt | Same tested packages: Evidently 0.7.23, pandas 2.2.3, NumPy 2.2.6, ipykernel 7.3.0. |',
              '| lab3/ and lab4/data/ | Synthetic reference/current CSVs. |',
              '| lab3/ and lab4/output/ | Prepared HTML, feature summary and actual chart for fallback. |',
              '| lab3/WORKSHEET.md | Short interpretation submission. |',
              '| lab4/INCIDENT.md, HINTS.md, submission_template.md | Incident evidence, optional hints and a 3–5 sentence decision. |',
              '| lab3/ and lab4/TROUBLESHOOTING.md | Brief fixes and the fallback procedure. |', '',
              'If setup fails, inspect the prepared report, chart and summary and answer the same questions. Data drift describes changing inputs; reliable labels and matching predictions are needed to judge quality.', '']
    (HANDOUT/'README.md').write_text('\n'.join(lines), encoding='utf-8')
    expected = {'README.md', *[f'LAB{n}.md' for n in STUDENT_FILES]}
    expected.update(f'lab{n}/{name}' for n,names in STUDENT_FILES.items() for name in names)
    actual = {str(path.relative_to(HANDOUT)) for path in HANDOUT.rglob('*') if path.is_file()}
    extras = sorted(actual - expected)
    print(f'Synchronized {len(expected)} student files in {HANDOUT}.')
    if extras:
        print('Existing files outside the student manifest (not deleted by this script):', extras)


if __name__ == '__main__':
    main()
