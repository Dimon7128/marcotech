#!/usr/bin/env python3
"""Render a built part and its actual embedded notes with LibreOffice.

Requires LibreOffice Impress, python3-uno and the intended fonts. Run this with
the system Python that has UNO, separately from the presentation-build venv.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--part', type=int)
    mode.add_argument('--all', action='store_true')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    source = root / ('output/Session7_Monitoring_Maintenance.pptx' if args.all else f'slides/part{args.part}/Session7_Part{args.part}.pptx')
    output = (args.output or root/('output/qa/final' if args.all else f'output/qa/part{args.part}')).resolve()
    output.mkdir(parents=True, exist_ok=True)
    version = subprocess.check_output(['libreoffice', '--version'], text=True).strip()
    fonts = {name: subprocess.check_output(['fc-match', '-f', '%{family}', name], text=True)
             for name in ['Aptos', 'Aptos Display', 'Aptos Mono', 'Arial']}
    print(version, flush=True)
    print('Resolved fonts:', fonts, flush=True)
    with tempfile.TemporaryDirectory(prefix='session7-slides-') as profile:
        subprocess.run(['libreoffice', '--headless', '--nologo', '--norestore',
                        f'-env:UserInstallation={Path(profile).as_uri()}', '--convert-to',
                        'pdf:impress_pdf_Export', '--outdir', str(output), str(source)], check=True)
    pdf = output/source.with_suffix('.pdf').name
    assert pdf.is_file(), 'Slide PDF was not created'
    subprocess.run([sys.executable, str(root/'scripts/export_notes.py'),
                    '--input', str(source), '--output', str(output/'notes.pdf')], check=True)
    slide_source = json.loads((root/'output/qa/slide-manifest.json' if args.all else source.with_name('slides.json')).read_text(encoding='utf-8'))
    diagrams = sorted({slide['diagram'] for slide in slide_source['slides'] if 'diagram' in slide})
    diagram_output = output/'diagrams'
    diagram_output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='session7-diagrams-') as profile:
        for name in diagrams:
            subprocess.run(['libreoffice', '--headless', '--nologo', '--norestore',
                            f'-env:UserInstallation={Path(profile).as_uri()}', '--convert-to',
                            'pdf:draw_pdf_Export', '--outdir', str(diagram_output),
                            str(root/'assets/diagrams'/f'{name}.svg')], check=True)
            assert (diagram_output/f'{name}.pdf').is_file(), f'SVG {name} did not render'
    evidence = {
        'rendered_at_utc': datetime.now(timezone.utc).isoformat(),
        'input': str(source.relative_to(root)),
        'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'renderer': version, 'resolved_fonts': fonts,
        'slides_pdf': pdf.name, 'actual_notes_pdf': 'notes.pdf', 'svg_diagrams':diagrams,
        'powerpoint_desktop': 'not verified',
    }
    (output/'render-environment.json').write_text(json.dumps(evidence, indent=2)+'\n')


if __name__ == '__main__':
    main()
