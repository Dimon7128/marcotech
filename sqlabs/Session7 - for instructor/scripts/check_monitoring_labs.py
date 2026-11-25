#!/usr/bin/env python3
"""Execute scripts/notebooks and independently verify both new monitoring labs.

Run with the authoring notebook environment; --lab-python selects a separate
clean environment installed only from the supplied lab requirements.
"""
import argparse
import csv
import hashlib
import importlib.util
from importlib.metadata import version
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab-python',type=Path,required=True)
    args=parser.parse_args()
    # Preserve the venv executable path; resolving its symlink selects system Python.
    python=args.lab_python.absolute()
    qa=ROOT/'output/qa/labs'
    qa.mkdir(parents=True,exist_ok=True)
    spec=importlib.util.spec_from_file_location('monitoring',ROOT/'labs/lab3/monitoring.py')
    monitoring=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(monitoring)
    assert (ROOT/'labs/lab3/monitoring.py').read_bytes()==(ROOT/'labs/lab4/monitoring.py').read_bytes()
    assert (ROOT/'labs/lab3/requirements.txt').read_bytes()==(ROOT/'labs/lab4/requirements.txt').read_bytes()
    for batch in ('reference','current'):
        assert (ROOT/f'labs/lab3/data/{batch}_sms.csv').read_bytes()==(ROOT/f'labs/lab2/{batch}.csv').read_bytes()
    for text,expected in [('HTTPS://example.com',True),('go to WWW.example.com',True),('http://example.com',True),('example.com',False),('www .example.com',False),('Meeting at five',False)]:
        assert monitoring.has_url_like(text)==expected
    invalid={
        'empty':'', 'header_only':'record_id,message\n', 'wrong_schema':'text,label\nhi,ham\n',
        'blank_message':'record_id,message\na,   \n', 'duplicate_ids':'record_id,message\na,Hi\na,Hello\n',
        'blank_id':'record_id,message\n,Hello\n', 'malformed':'record_id,message\na,"unterminated\n',
    }
    with tempfile.TemporaryDirectory(prefix='session7-input-checks-') as folder:
        path=Path(folder)/'bad.csv'
        for label,contents in invalid.items():
            path.write_text(contents)
            try:
                monitoring.load_features(path)
            except ValueError:
                pass
            else:
                raise AssertionError(label)
        try:
            monitoring.load_features(Path(folder)/'missing.csv')
        except ValueError:
            pass
        else:
            raise AssertionError('missing file')
    report={'status':'PASS','labs':{},'input_error_cases':list(invalid)+['missing_file'],
            'url_edge_cases':6,'source_sha256':{},'notes':'No classifier trained, no raw-text drift model, no labels/predictions, no quality metrics.'}
    for number in (3,4):
        lab=ROOT/f'labs/lab{number}'
        values={}
        for batch in ('reference','current'):
            path=lab/f'data/{batch}_sms.csv'
            with path.open(newline='',encoding='utf-8') as handle:
                rows=list(csv.DictReader(handle))
            lengths=[len(row['message']) for row in rows]
            flags=[any(marker in row['message'].lower() for marker in ('http://','https://','www.')) for row in rows]
            features=monitoring.load_features(path)
            assert list(features.columns)==['message_length','has_url']
            assert features.message_length.tolist()==lengths
            assert features.has_url.tolist()==['yes' if value else 'no' for value in flags]
            values[batch]={'messages':len(rows),'average_length':sum(lengths)/len(rows),
                           'url_like_count':sum(flags),'url_like_percentage':100*sum(flags)/len(rows)}
        # Execute the supplied script in the clean environment from another cwd.
        result=subprocess.run([str(python),str(lab/'run_report.py')],cwd='/tmp',text=True,capture_output=True,check=True)
        (qa/f'lab{number}-script.txt').write_text(result.stdout+result.stderr)
        actual=json.loads((lab/'output/feature_summary.json').read_text())
        assert actual['reference']==values['reference'] and actual['current']==values['current']
        assert actual['evidently_version']=='0.7.23'
        metrics=json.loads((lab/'output/evidently_result.json').read_text())['metrics']
        assert metrics[0]['value']['count']==(2 if number==3 else 1)
        assert {m['config']['column'] for m in metrics[1:]}=={'message_length','has_url'}
        name='monitoring_report.ipynb' if number==3 else 'monitoring_incident.ipynb'
        notebook=nbformat.read(lab/name,as_version=4)
        # Keep the distributed notebook clean; execute a copy and save QA evidence.
        with tempfile.TemporaryDirectory(prefix='session7-clean-kernel-') as kernel_root:
            kernel_dir=Path(kernel_root)/'session7-clean'
            kernel_dir.mkdir()
            (kernel_dir/'kernel.json').write_text(json.dumps({
                'argv':[str(python),'-m','ipykernel_launcher','-f','{connection_file}'],
                'display_name':'Session 7 clean test','language':'python'}))
            manager=KernelManager(kernel_name='session7-clean',
                                  kernel_spec_manager=KernelSpecManager(kernel_dirs=[kernel_root]))
            client=NotebookClient(notebook,km=manager,timeout=180,resources={'metadata':{'path':str(lab)}})
            try:
                client.execute()
            finally:
                manager.shutdown_kernel(now=True)
                manager.cleanup_resources()
        assert not any(output.get('output_type')=='error' for cell in notebook.cells if cell.cell_type=='code' for output in cell.outputs)
        nbformat.write(notebook,qa/f'lab{number}-executed.ipynb')
        assert (lab/'output/monitoring_report.html').stat().st_size>100000
        if number==4:
            ref=monitoring.load_features(lab/'data/reference_sms.csv')
            cur=monitoring.load_features(lab/'data/current_sms.csv')
            assert ref.message_length.tolist()==cur.message_length.tolist()
            assert values['reference']['url_like_percentage']==10 and values['current']['url_like_percentage']==70
        report['labs'][str(number)]={'features':values,'evidently_drifted_columns':metrics[0]['value']['count'],
              'script_clean_environment':'PASS','notebook_clean_environment':'PASS','raw_text_submitted':False,
              'clean_python':str(python),'timing':'planned; no classroom timing trial'}
        for path in sorted(lab.rglob('*')):
            if path.is_file() and not any(x in path.parts for x in ('__pycache__','output','instructor')) and path.suffix!='.zip':
                report['source_sha256'][str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    report['authoring_versions']={p:version(p) for p in ('evidently','pandas','numpy','nbformat','nbclient','ipykernel')}
    env=subprocess.check_output([str(python),'-c','import json,importlib.metadata as m;print(json.dumps({p:m.version(p) for p in ("evidently","pandas","numpy","ipykernel")}))'],text=True)
    report['clean_environment_versions']=json.loads(env)
    (qa/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS: both scripts from a clean environment, both notebooks, independent features, argument roles, invalid inputs and observed reports.')


if __name__=='__main__':
    main()
