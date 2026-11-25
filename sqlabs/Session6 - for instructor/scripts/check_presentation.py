#!/usr/bin/env python3
"""Check native PPTX/source consistency and create QA previews from rendered PDFs.

Optional dependencies: requirements-qa.txt. First render output/session6.pptx
to output/qa/session6.pdf with LibreOffice or PowerPoint. Export Notes separately
with export_notes.py when LibreOffice's python3-uno is available.
"""
from pathlib import Path
from collections import Counter
import json
import posixpath
import re
import zipfile

import fitz
from lxml import etree
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import yaml

from build_presentation import ROOT, sources, integrity, all_texts


def walk(shapes):
    for shape in shapes:
        yield shape
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from walk(shape.shapes)


def condensed(text):
    return re.sub(r"\s+", "", text)


def main():
    source = sources()
    path = ROOT / "output/session6.pptx"
    qa = ROOT / "output/qa"
    integrity(path, source)
    deck = Presentation(path)
    font_sizes, counts = set(), Counter()
    for number, slide in enumerate(deck.slides, 1):
        for sh in walk(slide.shapes):
            counts[str(sh.shape_type)] += 1
            assert sh.left >= 0 and sh.top >= 0, (number, sh.name)
            assert sh.left + sh.width <= deck.slide_width, (number, sh.name)
            assert sh.top + sh.height <= deck.slide_height, (number, sh.name)
            if sh.has_text_frame and sh.text.strip() and sh.name != "Slide number":
                for p in sh.text_frame.paragraphs:
                    for run in p.runs:
                        if run.text.strip():
                            font_sizes.add(run.font.size.pt)
                            assert run.font.size.pt >= 24
            assert sh.shape_type != MSO_SHAPE_TYPE.PICTURE
        for p in slide.notes_slide.notes_text_frame.paragraphs:
            assert p._p.get_or_add_pPr().get("rtl") == "1", number
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        for name in names:
            if not name.endswith(".rels"):
                continue
            base = posixpath.dirname(posixpath.dirname(name))
            for rel in etree.fromstring(z.read(name)):
                if rel.get("TargetMode") == "External":
                    continue
                target = rel.get("Target")
                target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(base, target))
                assert target in names, (name, target)
    pdf = fitz.open(qa / "session6.pdf")
    assert len(pdf) == len(source)
    previews = qa / "previews"
    previews.mkdir(exist_ok=True)
    fonts, bounds_errors = set(), []
    for number, (page, src) in enumerate(zip(pdf, source), 1):
        expected = src.title + src.text + str(number)
        assert condensed(page.get_text()) == condensed(expected), (number, "Rendered text differs or is missing")
        assert abs(page.rect.width / page.rect.height - 16/9) < .001
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    fonts.add(span["font"])
                    box = fitz.Rect(span["bbox"])
                    if not page.rect.contains(box):
                        bounds_errors.append({"slide": number, "text": span["text"], "bounds": list(box)})
        page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(previews / f"slide-{number:02d}.png")
    assert not bounds_errors, bounds_errors
    for first in range(0, len(pdf), 6):
        count = min(6, len(pdf) - first)
        rows = (count + 1) // 2
        sheet = Image.new("RGB", (1800, rows*540), "#e4e8e5")
        draw = ImageDraw.Draw(sheet)
        for k in range(count):
            number = first + k + 1
            preview = Image.open(previews / f"slide-{number:02d}.png")
            preview.thumbnail((864, 486))
            x, y = 18 + (k%2)*900, 35 + (k//2)*540
            sheet.paste(preview, (x, y))
            draw.text((x, y-22), f"Slide {number}", fill="black")
        sheet.save(qa / f"contact-{first//6+1}.png")
    notes = fitz.open(qa / "notes.pdf")
    assert len(notes) == 39
    assert notes[0].rect.height > notes[0].rect.width
    for number, page in enumerate(notes, 1):
        assert re.search(r"[\u0590-\u05ff]", page.get_text()), number
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    assert page.rect.contains(fitz.Rect(span["bbox"])), (number, span)
        if number in [1, 4, 16, 17, 32, 34, 37]:
            page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(qa / f"notes-{number:02d}.png")
    # BaseLoader avoids YAML 1.1 treating the workflow key `on` as a Boolean.
    wf = yaml.load((ROOT / "labs/lab1/workflows/ci-complete.yml").read_text(), Loader=yaml.BaseLoader)
    assert wf["on"] == ["push"]
    assert wf["permissions"] == {"contents": "read"}
    assert list(wf["jobs"]) == ["check-and-build"]
    job = wf["jobs"]["check-and-build"]
    assert job["runs-on"] == "ubuntu-latest"
    steps = job["steps"]
    assert len(steps) == 5
    assert steps[0]["uses"] == "actions/checkout@v7.0.1"
    assert steps[1]["uses"] == "actions/setup-python@v7.1.0"
    assert steps[1]["with"]["python-version"] == "3.10"
    assert steps[2]["run"] == "python -m pip install -r requirements-dev.txt"
    assert steps[3]["run"] == "python -m pytest -q"
    assert steps[4]["run"] == "docker build -f dockerfile -t sms-api:ci ."
    assert all("continue-on-error" not in step and "if" not in step for step in steps)
    challenge_wf = yaml.load((ROOT / "labs/final-lab/solutions/option_c_ci.yml").read_text(), Loader=yaml.BaseLoader)
    assert challenge_wf["on"] == ["push", "pull_request"]
    assert {k: v for k, v in challenge_wf.items() if k != "on"} == {k: v for k, v in wf.items() if k != "on"}
    svgs = sorted((ROOT / "assets/diagrams").glob("*.svg"))
    assert len(svgs) == 5
    for svg in svgs:
        tree = etree.fromstring(svg.read_bytes())
        assert not tree.xpath("//*[local-name()='image']")
        assert tree.xpath("//*[local-name()='text']")
    result = {
        "status": "PASS", "slides": 39, "embedded_hebrew_notes": 39,
        "minutes_per_part": [25,40,50,30,60], "total_minutes": 205,
        "hands_on_minutes": 107, "hands_on_percent": round(107/205*100,1),
        "editable_shape_types": dict(counts), "student_font_sizes_pt": sorted(font_sizes),
        "rendered_fonts": sorted(fonts), "rendered_slide_text_matches_source": True,
        "out_of_page_text_spans": bounds_errors, "rendered_notes_pages": 39,
        "svg_count": len(svgs), "workflow_validation": "Static inspection only",
        "hosted_github_run": "NOT VERIFIED", "microsoft_powerpoint_desktop": "NOT VERIFIED",
    }
    (qa / "presentation-checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
