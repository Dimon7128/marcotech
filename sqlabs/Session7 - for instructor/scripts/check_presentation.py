#!/usr/bin/env python3
"""Validate a built part, lab records and real PDF exports; create review images.

Run after rendering: python scripts/check_presentation.py --part 1
"""

import argparse
from collections import Counter
import csv
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import posixpath
import re
import sys
import unicodedata
from zipfile import ZipFile

import fitz
from lxml import etree
from PIL import Image, ImageDraw
from pptx import Presentation

from build_presentation import ROOT, load_part, note_text, source_texts, walk, diagram_source


def compact(text):
    text = unicodedata.normalize('NFKC', text)
    return ''.join(char for char in text if not char.isspace() and unicodedata.category(char) != 'Cf')


def note_tokens(text):
    # PDF extraction can join adjacent Hebrew/Latin runs without spaces.
    # Compare each script and numbers separately, allowing the notes-page number.
    text = ''.join(char for char in unicodedata.normalize('NFKC', text)
                   if unicodedata.category(char) != 'Cf')
    return Counter(re.findall(r'[\u0590-\u05ff]+|[A-Za-z_]+|\d+', text))


def check_archive(path, expected_notes, allow_report_images=False):
    with ZipFile(path) as archive:
        assert archive.testzip() is None
        names = set(archive.namelist())
        for name in names:
            if name.endswith('.xml') or name.endswith('.rels'):
                document = etree.fromstring(archive.read(name))
                if name.endswith('.rels'):
                    base = posixpath.dirname(posixpath.dirname(name))
                    for relationship in document:
                        if relationship.get('TargetMode') == 'External':
                            continue
                        target = relationship.get('Target')
                        resolved = (target.lstrip('/') if target.startswith('/') else
                                    posixpath.normpath(posixpath.join(base, target)))
                        assert resolved in names, (name, target)
        note_parts = [name for name in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', name)]
        assert len(note_parts) == expected_notes
        media = [name for name in names if name.startswith('ppt/media/')]
        assert allow_report_images or not media
        if allow_report_images:
            assert len(media) == 2 and all(name.endswith('.png') for name in media)


def check_lab():
    lab = ROOT/'labs/lab1'
    with (lab/'records.csv').open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == ['record_id', 'http_status', 'synthetic_sms', 'predicted_label', 'true_label']
        rows = list(reader)
    assert len(rows) == 6
    assert len({row['record_id'] for row in rows}) == len(rows)
    assert all(row['http_status'] == '200' for row in rows)
    assert all(row['predicted_label'] in {'ham','spam'} and row['true_label'] in {'ham','spam'} for row in rows)
    wrong = [row for row in rows if row['predicted_label'] != row['true_label']]
    assert [row['record_id'] for row in wrong] == ['sms-01', 'sms-04']
    assert {(row['predicted_label'],row['true_label']) for row in wrong} == {('ham','spam'),('spam','ham')}
    worksheet = (lab/'WORKSHEET.md').read_text(encoding='utf-8')
    expected_table = ['| ' + ' | '.join(row[key] for key in reader.fieldnames) + ' |' for row in rows]
    assert all(line in worksheet for line in expected_table), 'CSV and fallback table differ'
    assert Counter(row['predicted_label'] for row in rows) == {'ham':3, 'spam':3}
    assert 'simulated' in (lab/'README.md').read_text().lower()
    return {'records':len(rows),'http_successes':len(rows),'correct_predictions':len(rows)-len(wrong),
            'incorrect_ids':[row['record_id'] for row in wrong],
            'csv_matches_fallback':True,'student_code':'none; document-based exercise',
            'predictions':'synthetic and instructor-selected; model not executed'}


def check_svgs(source):
    checked = []
    namespace = {'s':'http://www.w3.org/2000/svg'}
    for name in sorted({slide['diagram'] for slide in source['slides'] if 'diagram' in slide}):
        path = ROOT/'assets/diagrams'/f'{name}.svg'
        document = etree.fromstring(path.read_bytes())
        assert not document.findall('.//s:image', namespace)
        assert not document.findall('.//s:foreignObject', namespace)
        assert all(not key.endswith('href') for node in document.iter() for key in node.attrib)
        actual = [compact(''.join(node.itertext())) for node in document.findall('s:text',namespace)]
        expected = [compact(item['text']) for item in diagram_source(name)['elements'] if item['type']=='text']
        assert actual == expected, name
        checked.append(name)
    return checked


def check_pdf(path, expected_count):
    document = fitz.open(path)
    assert len(document) == expected_count, (path.name,len(document))
    for page_number, page in enumerate(document,1):
        assert page.get_text().strip(), (path.name,page_number,'blank page')
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    if not span['text'].strip():
                        continue
                    box = fitz.Rect(span['bbox'])
                    assert box.x0 >= -1 and box.y0 >= -1, (path.name,page_number,span)
                    assert box.x1 <= page.rect.width+1 and box.y1 <= page.rect.height+1, (path.name,page_number,span)
    return document


def previews(slides_pdf, notes_pdf, qa, first_slide=1):
    directory = qa/'previews'
    directory.mkdir(exist_ok=True)
    images = []
    for index, page in enumerate(slides_pdf,first_slide):
        path = directory/f'slide-{index:02d}.png'
        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(path)
        with Image.open(path) as image:
            images.append(image.copy().resize((720,405),Image.LANCZOS))
    for index,page in enumerate(notes_pdf,first_slide):
        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(directory/f'notes-{index:02d}.png')
    margin, label, gap = 18, 25, 18
    rows = (len(images)+1)//2
    contact = Image.new('RGB',(2*720+3*margin,rows*(405+label+gap)+margin),'#E5E9E6')
    draw = ImageDraw.Draw(contact)
    for index,image in enumerate(images):
        x = margin+(index%2)*(720+margin)
        y = margin+(index//2)*(405+label+gap)
        draw.text((x,y),f'Slide {first_slide+index}',fill='#24292D')
        contact.paste(image,(x,y+label))
    contact.save(qa/'contact-sheet.png')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--part',type=int)
    mode.add_argument('--all',action='store_true')
    args = parser.parse_args()
    if args.all:
        manifest,_,_ = load_part(1)
        source = json.loads((ROOT/'output/qa/slide-manifest.json').read_text())
        expected = []
        for part in range(1,6):
            _,part_entry,part_source=load_part(part)
            expected += [{**item,'part':part,'number':part_entry['first_slide']+offset}
                         for offset,item in enumerate(part_source['slides'])]
        assert source['slides'] == expected, 'Final source differs from part sources'
        entry = {'first_slide':1,'minutes':180,'hands_on_minutes':95}
        assert sum(s['minutes'] for s in expected)==180
        assert sum(s['hands_on_minutes'] for s in expected)==95
        assert [s['number'] for s in expected]==list(range(1,len(expected)+1))
        path = ROOT/'output/Session7_Monitoring_Maintenance.pptx'
    else:
        manifest,entry,source = load_part(args.part)
        path = (ROOT/entry['source']).parent/f'Session7_Part{args.part}.pptx'
    deck = Presentation(path)
    assert len(deck.slides) == len(source['slides'])
    reference = Presentation(ROOT/manifest['reference'])
    assert (deck.slide_width,deck.slide_height)==(reference.slide_width,reference.slide_height)
    report = {'part':'all' if args.all else args.part,'slides':[],'object_types':Counter(), 'checks':{}}
    for offset,(slide,item) in enumerate(zip(deck.slides,source['slides'])):
        number = entry['first_slide']+offset
        shapes = list(walk(slide.shapes))
        content = [shape for shape in shapes if shape.name.startswith('Content::')]
        assert [compact(shape.text) for shape in content] == [compact(text) for text in source_texts(item)]
        assert next(shape.text for shape in shapes if shape.name=='Title') == item['title']
        assert next(shape.text for shape in shapes if shape.name=='Slide number') == str(number)
        assert next(shape.text for shape in shapes if shape.name=='Part marker') == f'Part {item["part"] if args.all else args.part}/5'
        words = len(' '.join(shape.text for shape in content).split())
        assert 10 <= words <= 30, (number,words)
        assert not re.search(r'[\u0590-\u05ff]',' '.join(shape.text for shape in content))
        for shape in shapes:
            report['object_types'][str(shape.shape_type)] += 1
            if shape.shape_type == 13:
                assert 'image' in item and shape.name.startswith('Report screenshot::')
                assert shape.image.blob == (ROOT/item['image']).read_bytes(), 'Report screenshot differs from source'
                assert shape.width < deck.slide_width*.9 and shape.height < deck.slide_height*.6
            assert shape.left >= 0 and shape.top >= 0, (number,shape.name)
            assert shape.left+shape.width <= deck.slide_width+2, (number,shape.name)
            assert shape.top+shape.height <= deck.slide_height+2, (number,shape.name)
            if shape in content:
                assert all(run.font.size.pt >= 24 for paragraph in shape.text_frame.paragraphs for run in paragraph.runs)
        for index,first in enumerate(content):
            for second in content[index+1:]:
                overlap_x = min(first.left+first.width,second.left+second.width)-max(first.left,second.left)
                overlap_y = min(first.top+first.height,second.top+second.height)-max(first.top,second.top)
                assert overlap_x <= 2 or overlap_y <= 2, (number,'overlapping text boxes',first.name,second.name)
        assert slide.has_notes_slide
        notes = slide.notes_slide.notes_text_frame
        assert notes.text == '\n'.join(note_text(block) for block in item['notes'])
        assert all(paragraph._p.get_or_add_pPr().get('rtl')=='1' for paragraph in notes.paragraphs)
        assert re.search(r'[\u0590-\u05ff]',notes.text)
        report['slides'].append({'number':number,'id':item['id'],'title':item['title'],'body_words':words,
                                 'minutes':item['minutes'],'hands_on_minutes':item['hands_on_minutes'],
                                 'notes_words':len(notes.text.split())})
    check_archive(path,len(source['slides']),any('image' in s for s in source['slides']))
    report['diagram_exports'] = check_svgs(source)
    if args.part==1:
        report['lab'] = check_lab()
    elif args.part==2:
        lab_evidence = json.loads((ROOT/'output/qa/labs/lab2-checks.json').read_text())
        assert lab_evidence['status']=='PASS'
        for filename,expected in lab_evidence['source_sha256'].items():
            assert hashlib.sha256((ROOT/'labs/lab2'/filename).read_bytes()).hexdigest()==expected, ('stale lab evidence',filename)
        report['lab'] = lab_evidence
    if args.all or args.part in (3,5):
        evidence = json.loads((ROOT/'output/qa/labs/checks.json').read_text())
        assert evidence['status']=='PASS'
        report['monitoring_labs'] = evidence
    qa = ROOT/('output/qa/final' if args.all else f'output/qa/part{args.part}')
    rendering = json.loads((qa/'render-environment.json').read_text())
    assert rendering['input_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest(), 'PDF exports are stale'
    slides_pdf = check_pdf(qa/path.with_suffix('.pdf').name,len(deck.slides))
    notes_pdf = check_pdf(qa/'notes.pdf',len(deck.slides))
    for page,slide,item in zip(slides_pdf,deck.slides,source['slides']):
        actual_text = compact(page.get_text())
        for text in [item['title'],*source_texts(item)]:
            assert compact(text) in actual_text, (item['id'],'missing or clipped rendered text',text)
    for offset, (page,item) in enumerate(zip(notes_pdf,source['slides'])):
        expected = note_tokens('\n'.join(note_text(block) for block in item['notes']))
        expected[str(entry['first_slide']+offset)] += 1
        assert note_tokens(page.get_text()) == expected, (item['id'],'notes text missing from actual rendered page')
    for name in report['diagram_exports']:
        diagram_pdf = check_pdf(qa/'diagrams'/f'{name}.pdf',1)
        page_text = compact(diagram_pdf[0].get_text())
        for item in diagram_source(name)['elements']:
            if item['type']=='text':
                assert compact(item['text']) in page_text, (name,item['text'])
        image = diagram_pdf[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
        image.save(qa/'diagrams'/f'{name}.png')
    previews(slides_pdf,notes_pdf,qa,entry['first_slide'])
    report['rendering'] = rendering
    report['build_environment'] = {'python':sys.version.split()[0],**{package:version(package) for package in
                                   ['python-pptx','lxml','XlsxWriter','Pillow','PyMuPDF']}}
    report['checks'] = dict.fromkeys(['native_source_text','editable_shapes','slide_bounds','text_box_overlap',
        'word_budgets','embedded_hebrew_notes','rtl_paragraphs','package_xml_relationships','diagram_source_export_match',
        'current_slide_and_actual_notes_pdfs','rendered_text_presence','rendered_notes_content_complete',
        'rendered_svg_text','rendered_text_page_bounds'], 'PASS')
    report['manual_visual_review'] = 'pending; inspect the generated images'
    review_path = qa/'visual-review.json'
    if review_path.exists():
        review = json.loads(review_path.read_text())
        if review.get('input_sha256') == rendering['input_sha256']:
            report['manual_visual_review'] = review
    (qa/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS: {len(deck.slides)} editable slides, embedded Hebrew notes, source and rendered text, package relationships and bounds.')
    print(f'PASS: {sum(s["minutes"] for s in source["slides"])} minutes, {sum(s["hands_on_minutes"] for s in source["slides"])} hands-on; diagram exports and lab records checked.')
    print(f'Created slide and actual-notes previews, contact sheet and {qa/"checks.json"}.')


if __name__ == '__main__':
    main()
