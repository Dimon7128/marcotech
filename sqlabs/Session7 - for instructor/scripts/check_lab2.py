#!/usr/bin/env python3
"""Execute Lab 2's original and completed student exercise; verify real results.

Run with the lab environment: python scripts/check_lab2.py --write-materials
Use --write-materials to refresh data-derived fallback files and expected output.
"""

import argparse
from collections import Counter
import csv
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT/'labs/lab2'
QA = ROOT/'output/qa/labs'
MARKERS = ('http://','https://','www.')
STUDENT_FILES = ['README.md','starter.py','reference.csv','current.csv','requirements.txt',
                 'WORKSHEET.md','EXPECTED_RESULTS.md']


def independent_batch(filename):
    with (LAB/filename).open(encoding='utf-8',newline='') as handle:
        reader=csv.DictReader(handle)
        assert reader.fieldnames==['record_id','message']
        rows=list(reader)
    assert len(rows)==10 and len({row['record_id'] for row in rows})==10
    assert all(row['message'].isascii() and 0<len(row['message'])<=500 for row in rows)
    values=[{'record_id':row['record_id'],'message_length':len(row['message']),
             'has_url_like':any(marker in row['message'].lower() for marker in MARKERS)} for row in rows]
    return {
        'rows':len(rows),
        'average_length':sum(row['message_length'] for row in values)/len(values),
        'url_like_count':sum(row['has_url_like'] for row in values),
        'url_like_percentage':100*sum(row['has_url_like'] for row in values)/len(values),
        'features':values,
    }


def run_script(path,cwd):
    result=subprocess.run([sys.executable,str(path)],cwd=cwd,text=True,capture_output=True)
    assert result.returncode==0,(path,result.stdout,result.stderr)
    assert not result.stderr,result.stderr
    return result.stdout


def fallback_text(results):
    reference,current=results['Reference'],results['Current']
    lines=['# Lab 2 — Prepared results and fallback','',
           '**Synthetic teaching scenarios only.** Values below come from executing the completed student exercise on the supplied CSVs. The batches contain no true labels or model predictions.','',
           'If Python is unavailable, inspect one original message from each CSV, compare the following values, and answer WORKSHEET.md.','',
           '| Feature | Reference | Current |','| --- | ---: | ---: |',
           f'| Messages | {reference["rows"]} | {current["rows"]} |',
           f'| Average message length, characters | {reference["average_length"]:.1f} | {current["average_length"]:.1f} |',
           f'| URL-like messages, count | {reference["url_like_count"]} | {current["url_like_count"]} |',
           f'| URL-like messages, % | {reference["url_like_percentage"]:.1f} | {current["url_like_percentage"]:.1f} |','',
           'Lengths include spaces and punctuation. URL-like means a case-insensitive substring match for `http://`, `https://` or `www.`. It is an approximate input descriptor.','',
           '## Check individual records','',
           '| Batch | Record | Length, characters | URL-like |','| --- | --- | ---: | --- |']
    for name,batch in results.items():
        for row in batch['features']:
            lines.append(f'| {name} | {row["record_id"]} | {row["message_length"]} | {row["has_url_like"]} |')
    lines.extend(['','## Your interpretation','',
                  'Use the same questions as the Python path: what changed; whether this supports data drift; whether accuracy or concept drift is established; and what additional evidence would help.','',
                  'These are descriptive results for two small planned scenarios. They are not a statistical test or measurements of changes in UCI or production traffic.',''])
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-materials',action='store_true')
    args=parser.parse_args()
    QA.mkdir(parents=True,exist_ok=True)
    source=(LAB/'starter.py').read_text()
    assert source.count('average_length = None')==1
    before=run_script(LAB/'starter.py',LAB)
    assert 'TODO' in before and '20.0' in before and '80.0' in before
    results={name:independent_batch(filename) for name,filename in [('Reference','reference.csv'),('Current','current.csv')]}
    assert results['Current']['average_length']>results['Reference']['average_length']
    assert results['Reference']['url_like_count']==2 and results['Current']['url_like_count']==8
    completed=source.replace('average_length = None','average_length = features["message_length"].mean()')
    with tempfile.TemporaryDirectory(prefix='session7-lab2-student-') as directory:
        folder=Path(directory)
        (folder/'starter.py').write_text(completed)
        for filename in ['reference.csv','current.csv']:
            shutil.copyfile(LAB/filename,folder/filename)
        after=run_script(folder/'starter.py',folder.parent)
        assert 'TODO' not in after
        namespace=runpy.run_path(str(folder/'starter.py'),run_name='student_check')
        for name,filename in [('Reference','reference.csv'),('Current','current.csv')]:
            features=namespace['load_features'](filename)
            actual=namespace['summarize'](features)
            assert float(actual['Average length (characters)'])==results[name]['average_length']
            assert float(actual['URL-like messages (%)'])==results[name]['url_like_percentage']
            assert features[['record_id','message_length','has_url_like']].to_dict('records')==results[name]['features']
        cases={'plain message':False,'HTTPS://example.com/info':True,'WWW.example.com/info':True,
               'http://example.com':True,'example.com':False,'www.':True}
        for message,expected in cases.items():
            assert namespace['has_url_like'](message)==expected,(message,expected)
    assert (LAB/'starter.py').read_text()==source,'Student source was changed during QA'
    expected={name:{key:value for key,value in batch.items() if key!='features'} for name,batch in results.items()}
    fallback=fallback_text(results)
    if args.write_materials:
        (LAB/'expected_results.json').write_text(json.dumps(expected,indent=2)+'\n')
        (LAB/'EXPECTED_RESULTS.md').write_text(fallback,encoding='utf-8')
    assert json.loads((LAB/'expected_results.json').read_text())==expected
    assert (LAB/'EXPECTED_RESULTS.md').read_text(encoding='utf-8')==fallback
    (QA/'lab2-student-start.txt').write_text(before)
    (QA/'lab2-student-completed.txt').write_text(after)
    evidence={
        'status':'PASS','python':sys.version.split()[0],
        'dependencies':{name:version(name) for name in ['pandas','numpy','python-dateutil','pytz','six','tzdata']},
        'source_sha256':{filename:hashlib.sha256((LAB/filename).read_bytes()).hexdigest() for filename in
                         ['starter.py','reference.csv','current.csv','requirements.txt','README.md',
                          'WORKSHEET.md','EXPECTED_RESULTS.md','expected_results.json']},
        'checks':['original starter executes with intentional TODO','completed student copy executes',
                  'execution works outside script directory','pandas results equal independent CSV calculations',
                  'all per-record features agree','URL rule and its documented limitations',
                  'fallback and expected results match real data','original starter preserved'],
        'results':expected,
        'classroom_timing':'15-minute teaching plan; not measured with students',
        'platform':'Linux execution; Windows/macOS commands reviewed, not executed',
    }
    (QA/'lab2-checks.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('PASS: original starter, completed student copy, all features, independent calculations and fallback.')
    print(json.dumps(expected,indent=2))


if __name__=='__main__':
    main()
