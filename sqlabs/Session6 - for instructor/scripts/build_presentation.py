#!/usr/bin/env python3
"""Build the editable Session 6 deck from its five Markdown sources.

Run from any directory: python scripts/build_presentation.py
Only python-pptx is required. No raster slide assets are used.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import json
import re
import zipfile

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR, PP_PLACEHOLDER
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
ASSETS = ROOT / "assets/diagrams"
GREEN = "196B24"
INK = "24292D"
MUTED = "596269"
PALE = "F1F7F2"
NEUTRAL = "F5F6F7"
LINE = "D5DDD6"
WHITE = "FFFFFF"
TITLE_FONT = "Aptos Display"
BODY_FONT = "Aptos"
CODE_FONT = "Aptos Mono"
NOTES_FONT = "Arial"
WIDTH, HEIGHT = 13.333333, 7.5
LEFT, RIGHT = 0.72, 12.61


@dataclass
class SlideSource:
    number: int
    part: int
    title: str
    text: str
    notes: str
    minutes: float


def sources() -> list[SlideSource]:
    result = []
    for part in range(1, 6):
        source = (ROOT / f"content/part{part}.md").read_text(encoding="utf-8")
        pattern = r"(?ms)^## Slide (\d+) — ([^\n]+)\n(.*?)(?=^## |\Z)"
        for match in re.finditer(pattern, source):
            number, title, section = match.groups()
            body = re.search(r"```text\n(.*?)\n```", section, re.S)
            duration = re.search(r"\*\*Estimated duration:\*\* ([\d.]+)", section)
            assert body and duration and "### Hebrew instructor notes" in section
            notes = section.split("### Hebrew instructor notes", 1)[1]
            notes = notes.split("\n---", 1)[0].strip()
            notes = "\n".join(
                line for line in notes.splitlines() if "not slide text:" not in line
            ).strip()
            result.append(SlideSource(int(number), part, title, body.group(1), notes,
                                      float(duration.group(1))))
    assert [s.number for s in result] == list(range(1, 40))
    assert [sum(s.minutes for s in result if s.part == p) for p in range(1, 6)] == [25, 40, 50, 30, 60]
    return result


def color(value: str) -> RGBColor:
    return RGBColor.from_string(value)


def textbox(shapes, text, x, y, w, h, size=31, font=BODY_FONT, bold=False,
            fill=INK, align=PP_ALIGN.LEFT, vertical=MSO_ANCHOR.TOP,
            margin=0, space_after=12, line_spacing=1.12, name=None):
    shape = shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        shape.name = name
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = vertical
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(0)
        p.space_after = Pt(space_after)
        p.line_spacing = line_spacing
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color(fill)
        run._r.get_or_add_rPr().set("lang", "en-US")
    return shape


def panel(shapes, x, y, w, h, fill=NEUTRAL, border=LINE, name="Editable panel"):
    sh = shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.name = name
    sh.fill.solid()
    sh.fill.fore_color.rgb = color(fill)
    sh.line.color.rgb = color(border)
    sh.line.width = Pt(1)
    return sh


def arrow(shapes, x1, y, x2):
    sh = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y), Inches(x2), Inches(y))
    sh.name = "Editable sequence arrow"
    sh.line.color.rgb = color(GREEN)
    sh.line.width = Pt(1.8)
    tail = OxmlElement("a:tailEnd")
    tail.set("type", "triangle")
    tail.set("w", "sm")
    tail.set("len", "sm")
    sh.line._get_or_add_ln().append(tail)
    return sh


def pipeline(slide, labels, widths=None, y=2.65, h=1.55):
    """One native PowerPoint group, made only of rectangles, text and lines."""
    group = slide.shapes.add_group_shape()
    group.name = "Workflow — editable shapes, labels and arrows"
    gap = 0.23
    if widths is None:
        widths = [(RIGHT - LEFT - gap * (len(labels) - 1)) / len(labels)] * len(labels)
    total = sum(widths) + gap * (len(labels) - 1)
    x = (WIDTH - total) / 2
    for index, (label, w) in enumerate(zip(labels, widths)):
        panel(group.shapes, x, y, w, h, fill=PALE, border=GREEN, name=f"Stage {index + 1}")
        textbox(group.shapes, label, x + 0.05, y + 0.08, w - 0.1, h - 0.16,
                size=24, bold=False, fill=INK, align=PP_ALIGN.CENTER,
                vertical=MSO_ANCHOR.MIDDLE, space_after=0, line_spacing=1.04,
                name=f"Stage {index + 1} label — editable")
        if index < len(labels) - 1:
            arrow(group.shapes, x + w + 0.025, y + h / 2, x + w + gap - 0.025)
        x += w + gap


def code_panel(slide, code, y=3.9, h=1.25, size=27, x=LEFT, w=None):
    w = RIGHT - x if w is None else w
    panel(slide.shapes, x, y, w, h, fill=NEUTRAL, border=LINE, name="Editable code panel")
    return textbox(slide.shapes, code, x + 0.25, y + 0.15, w - 0.5, h - 0.3,
                   size=size, font=CODE_FONT, space_after=0, line_spacing=1.1,
                   name="Code — native editable text")


def plain(slide, text, y=2.2, size=31, h=4.55, w=None):
    return textbox(slide.shapes, text, LEFT, y, w or RIGHT - LEFT, h,
                   size=size, space_after=23, line_spacing=1.14, name="Student text — editable")


def note_lines(markdown):
    """Convert the instructor Markdown to ordered native Notes paragraphs."""
    lines = []
    for line in markdown.splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", line)
        # LRM protects technical expressions within a right-to-left paragraph.
        line = re.sub(r"`([^`]+)`", lambda m: "\u200e" + m.group(1) + "\u200e", line)
        line = line.replace("**", "")
        line = re.sub(r"^#{1,6}\s*", "", line)
        if line.startswith("- "):
            line = "• " + line[2:]
        # Keep the time heading short. The remaining allocation is a separate
        # paragraph, so a long bold RTL heading cannot run beyond the page.
        if not lines and (" — " in line or "; " in line):
            heading = re.split(r" — |; ", line, maxsplit=1)
            lines.extend(heading)
        else:
            lines.append(line)
    return lines


def add_notes(slide, markdown):
    ns = slide.notes_slide
    # Full-page notes leave room for Hebrew teaching prompts. The Notes section
    # remains native and also prints legibly; no slide screenshot is needed.
    for sh in list(ns.shapes):
        if sh.is_placeholder and sh.placeholder_format.type == PP_PLACEHOLDER.SLIDE_IMAGE:
            sh._element.getparent().remove(sh._element)
    body = next(sh for sh in ns.shapes if sh.is_placeholder and
                sh.placeholder_format.type == PP_PLACEHOLDER.BODY)
    body.left, body.top = Inches(0.55), Inches(0.4)
    body.width, body.height = Inches(6.4), Inches(9.0)
    tf = body.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_top = tf.margin_bottom = Pt(0)
    tf.margin_left = tf.margin_right = Pt(0)
    lines = note_lines(markdown)
    long_notes = sum(map(len, lines)) > 2000
    for index, line in enumerate(lines):
        p = tf.paragraphs[0] if index == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = PP_ALIGN.RIGHT
        p.space_before = Pt(0)
        p.space_after = Pt(4 if long_notes else 7)
        p.line_spacing = 1.06 if long_notes else 1.12
        pPr = p._p.get_or_add_pPr()
        pPr.set("rtl", "1")
        for run in p.runs:
            run.font.name = NOTES_FONT
            run.font.size = Pt(11 if long_notes else 12)
            run.font.bold = index == 0
            rPr = run._r.get_or_add_rPr()
            rPr.set("lang", "he-IL")
            for tag in ("a:cs", "a:ea"):
                child = OxmlElement(tag)
                child.set("typeface", NOTES_FONT)
                rPr.append(child)
    assert re.search(r"[\u0590-\u05FF]", tf.text)


def lay_out(slide, source):
    n, text = source.number, source.text
    lines = text.splitlines()
    if n == 4:
        groups = text.split("\n\n")
        for i, group_text in enumerate(groups):
            x, w = LEFT + i * 4.04, 3.81
            group = slide.shapes.add_group_shape()
            group.name = ["CI concept", "CD concept", "CT concept"][i]
            panel(group.shapes, x, 2.08, w, 3.82, fill=PALE, border=LINE)
            parts = group_text.splitlines()
            textbox(group.shapes, parts[0], x + .22, 2.32, w - .44, .7,
                    size=40, bold=True, fill=GREEN, space_after=0)
            textbox(group.shapes, parts[1], x + .22, 3.14, w - .44, .76,
                    size=24, bold=True, space_after=0)
            textbox(group.shapes, "\n".join(parts[2:]), x + .22, 4.18, w - .44, 1.5,
                    size=26, space_after=13)
    elif n == 6:
        pipeline(slide, ["Code\nPush", "Install\nDependencies", "Run\nTests",
                         "Build Docker\nImage", "CI Result\nPass / Fail"], y=2.3)
        plain(slide, "\n".join(lines[7:]), y=4.55, size=28, h=1.9)
    elif n in (14, 15):
        plain(slide, "\n".join(lines[:-1]), y=2.15, h=2.1)
        code_panel(slide, lines[-1], y=4.62, h=1.0, size=27)
    elif n in (17, 26, 37):
        plain(slide, "\n".join(lines[:3]), y=2.16, h=3.4, size=31)
        panel(slide.shapes, LEFT, 6.0, 2.3, .61, fill=PALE, border=GREEN,
              name="Editable time allocation")
        textbox(slide.shapes, lines[-1], LEFT + .12, 6.08, 2.06, .46,
                size=25, fill=GREEN, space_after=0)
    elif n == 20:
        for i, line in enumerate(lines):
            key, explanation = line.split(": ", 1)
            y = 2.05 + i * 1.0
            textbox(slide.shapes, key + ":", LEFT, y, 2.2, .58,
                    size=31, bold=True, fill=GREEN, space_after=0)
            textbox(slide.shapes, explanation, 3.18, y, 8.9, .64,
                    size=31, space_after=0)
    elif n == 21:
        group = slide.shapes.add_group_shape()
        group.name = "Repository files — editable text"
        panel(group.shapes, LEFT, 2.05, RIGHT - LEFT, 2.72, fill=NEUTRAL)
        textbox(group.shapes, lines[0], LEFT + .25, 2.23, 10.9, .5,
                size=26, bold=True, space_after=0)
        textbox(group.shapes, lines[1], LEFT + .25, 3.0, 10.9, .58,
                size=29, font=CODE_FONT, fill=GREEN, space_after=0)
        textbox(group.shapes, lines[2], LEFT + .25, 3.93, 10.9, .55,
                size=26, font=CODE_FONT, space_after=0)
        plain(slide, lines[3], y=5.28, size=30, h=1.0)
    elif n == 22:
        pipeline(slide, ["Push", "Checkout", "Set up\nPython", "Install\nDependencies",
                         "pytest", "Docker\nBuild"],
                 widths=[1.2, 1.7, 1.75, 2.47, 1.25, 1.95], y=2.4, h=1.6)
        plain(slide, "\n".join(lines[7:]), y=4.78, size=29, h=1.8)
    elif n == 23:
        code_panel(slide, "\n".join(lines[:5]), y=1.95, h=3.05, size=27)
        plain(slide, "\n".join(lines[6:]), y=5.38, size=28, h=1.2)
    elif n == 24:
        textbox(slide.shapes, lines[0], LEFT, 1.98, 11.8, .5,
                size=25, fill=MUTED, space_after=0)
        code_panel(slide, "\n".join(lines[1:4]), y=2.68, h=2.18, size=28)
        plain(slide, lines[4], y=5.42, size=30, h=1.05)
    elif n == 25:
        textbox(slide.shapes, lines[0], LEFT, 2.1, 11.8, .62,
                size=31, bold=True, fill=GREEN, space_after=0)
        plain(slide, "\n".join(lines[1:]), y=3.17, size=31, h=3.1)
    elif n == 27:
        parts = text.split("\n\n")
        for i, block in enumerate(parts[:2]):
            x, w = LEFT + i * 6.11, 5.78
            group = slide.shapes.add_group_shape()
            group.name = "Current CI" if i == 0 else "Future release"
            panel(group.shapes, x, 2.24, w, 2.45, fill=PALE if i == 0 else NEUTRAL)
            a, b = block.split("\n", 1)
            textbox(group.shapes, a, x + .25, 2.48, w - .5, .62,
                    size=31, bold=True, fill=GREEN, space_after=0)
            textbox(group.shapes, b, x + .25, 3.38, w - .5, 1.0,
                    size=28, space_after=0)
        plain(slide, parts[2], y=5.46, size=30, h=1)
    elif n == 28:
        plain(slide, lines[0], y=2.05, size=31, h=.9)
        for i, tag in enumerate(lines[1:3]):
            x, w = LEFT + i * 6.11, 5.78
            group = slide.shapes.add_group_shape()
            group.name = "Application version card — editable"
            panel(group.shapes, x, 3.2, w, 1.45, fill=PALE, border=GREEN)
            textbox(group.shapes, tag, x + .15, 3.48, w - .3, .85,
                    size=32, font=CODE_FONT, align=PP_ALIGN.CENTER,
                    vertical=MSO_ANCHOR.MIDDLE, space_after=0)
        plain(slide, lines[3], y=5.32, size=30, h=1.15)
    elif n == 32:
        textbox(slide.shapes, lines[0], LEFT, 1.9, 11.8, .45,
                size=25, fill=GREEN, bold=True, space_after=0)
        pipeline(slide, ["CI\nPasses", "Identify\nVersion", "Approval", "Release",
                         "Smoke\nTest", "Keep or\nRoll Back"],
                 widths=[1.5, 1.9, 1.75, 1.55, 1.7, 2.18], y=2.61, h=1.6)
        plain(slide, "\n".join(lines[8:]), y=4.91, size=28, h=1.65)
    elif n == 34:
        for i, line in enumerate(lines):
            group = slide.shapes.add_group_shape()
            group.name = f"Challenge choice {i + 1}"
            y = 2.04 + i * 1.27
            panel(group.shapes, LEFT, y, RIGHT - LEFT, .95, fill=PALE)
            textbox(group.shapes, line, LEFT + .24, y + .2, RIGHT - LEFT - .48, .6,
                    size=30, space_after=0)
    elif n == 39:
        plain(slide, "\n".join(lines[:3]), y=1.97, size=31, h=2.75)
        plain(slide, lines[3], y=4.85, size=28, h=1.05)
        textbox(slide.shapes, lines[4], LEFT, 6.38, 11.8, .5,
                size=26, fill=GREEN, space_after=0)
    else:
        plain(slide, text)


def svg_header(w=1200, h=260):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">\n'
            '<!-- Native vector text and shapes; no external styles or images. -->\n')


def svg_text(label, x, y, line_height=30, css="", anchor="middle", size=24, ink=INK, bold=False):
    lines = label.split("\n")
    if css == "small":
        size, ink = 22, MUTED
    result = (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
              f'font-family="Aptos,Arial,sans-serif" font-size="{size}" '
              f'font-weight="{"bold" if bold else "normal"}" fill="#{ink}">')
    for i, line in enumerate(lines):
        result += f'<tspan x="{x}" dy="{0 if i == 0 else line_height}">{escape(line)}</tspan>'
    return result + "</text>\n"


def svg_pipeline(name, labels, caption, widths=None):
    gap, x, y, h = 24, 12, 30, 120
    widths = widths or [(1176 - gap * (len(labels) - 1)) / len(labels)] * len(labels)
    svg = svg_header() + f'<title>{escape(caption)}</title>\n'
    for i, (label, w) in enumerate(zip(labels, widths)):
        svg += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#{PALE}" stroke="#{GREEN}" stroke-width="1.5"/>\n'
        nlines = len(label.splitlines())
        svg += svg_text(label, x + w/2, y + h/2 + 9 - (nlines-1)*15)
        if i < len(labels) - 1:
            end = x+w+gap-4
            svg += f'<line x1="{x+w+3}" y1="90" x2="{end-5}" y2="90" stroke="#{GREEN}" stroke-width="1.8"/>\n'
            svg += f'<polygon points="{end},90 {end-6},86 {end-6},94" fill="#{GREEN}"/>\n'
        x += w + gap
    svg += svg_text(caption, 600, 213, css="small") + "</svg>\n"
    (ASSETS / name).write_text(svg, encoding="utf-8")


def make_svgs():
    ASSETS.mkdir(parents=True, exist_ok=True)
    svg_pipeline("part1-ci-pipeline.svg",
                 ["Code\nPush", "Install\nDependencies", "Run\nTests", "Build Docker\nImage", "CI Result\nPass / Fail"],
                 "Build after tests pass. No deployment or retraining.")
    svg_pipeline("part3-ci-workflow.svg",
                 ["Push", "Checkout", "Set up\nPython", "Install\nDependencies", "pytest", "Docker\nBuild"],
                 "Tests must pass before Docker builds.",
                 [125, 168, 180, 215, 137, 231])
    svg_pipeline("part4-release-workflow.svg",
                 ["CI\nPasses", "Identify\nVersion", "Approval", "Release", "Smoke\nTest", "Keep or\nRoll Back"],
                 "Future workflow", [150, 190, 175, 155, 170, 216])
    svg = svg_header(h=320) + '<title>Application image versions</title>\n'
    svg += svg_text("A tag names an application image.", 600, 40)
    for x, label in [(25, "sms-api:v1.0"), (625, "sms-api:v1.1")]:
        svg += f'<rect x="{x}" y="85" width="550" height="120" fill="#{PALE}" stroke="#{GREEN}"/>\n'
        svg += svg_text(label, x+275, 157)
    svg += svg_text("New API code can use the same saved model.", 600, 275, css="small") + "</svg>\n"
    (ASSETS / "part4-application-versions.svg").write_text(svg, encoding="utf-8")
    svg = svg_header(h=380) + '<title>CI, CD and CT in the SMS project</title>\n'
    for x, lines in [(15, ["CI", "Continuous Integration", "Check changes.", "SMS API tests."]),
                     (415, ["CD", "Continuous Delivery", "Prepare releases.", "SMS service ready for approval."]),
                     (815, ["CT", "Continuous Training", "Retrain models automatically.", "Updated SMS model."])]:
        svg += f'<rect x="{x}" y="20" width="370" height="325" fill="#{PALE}" stroke="#{LINE}"/>\n'
        for j, label in enumerate(lines):
            # The long CD example wraps while remaining SVG text.
            if label == "SMS service ready for approval.":
                label = "SMS service ready\nfor approval."
            svg += svg_text(label, x+185, [75, 130, 205, 267][j],
                            size=40 if j == 0 else (24 if j == 1 else 26),
                            ink=GREEN if j == 0 else INK, bold=j < 2)
    svg += "</svg>\n"
    (ASSETS / "ci-cd-ct.svg").write_text(svg, encoding="utf-8")


def all_texts(shapes):
    for shape in shapes:
        if shape.shape_type == 6:  # GROUP
            yield from all_texts(shape.shapes)
        elif shape.has_text_frame and shape.text.strip():
            yield shape.text


def normalize(text):
    return " ".join(text.split())


def remove_effects(shapes):
    for shape in shapes:
        # python-pptx's default auto-shape style inherits a theme shadow.
        # Keep every panel and connector flat, following the course brief.
        for effect in shape._element.xpath("./p:style/a:effectRef"):
            effect.set("idx", "0")
        if shape.shape_type == 6:
            remove_effects(shape.shapes)


def integrity(path, source_slides):
    deck = Presentation(path)
    assert len(deck.slides) == 39
    manifest = []
    for slide, source in zip(deck.slides, source_slides):
        texts = list(all_texts(slide.shapes))
        assert texts[-1] == str(source.number)
        visible = "\n".join(texts[:-1])
        assert normalize(visible) == normalize(source.title + "\n" + source.text), (source.number, texts)
        assert not re.search(r"[\u0590-\u05ff]", visible), source.number
        assert slide.has_notes_slide and re.search(r"[\u0590-\u05ff]", slide.notes_slide.notes_text_frame.text)
        assert slide.notes_slide.notes_text_frame.text == "\n".join(note_lines(source.notes)), (source.number, "Notes differ from source")
        manifest.append({"slide": source.number, "part": source.part, "title": source.title,
                         "minutes": source.minutes,
                         "body_words": len(source.text.split()),
                         "notes_characters": len(slide.notes_slide.notes_text_frame.text)})
    with zipfile.ZipFile(path) as archive:
        # Ensure every XML part is well formed; the deck uses no raster media.
        for name in archive.namelist():
            if name.endswith(".xml"):
                etree.fromstring(archive.read(name))
        assert len([n for n in archive.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+.xml", n)]) == 39
        assert not [n for n in archive.namelist() if n.startswith("ppt/media/")]
    (OUT / "qa").mkdir(parents=True, exist_ok=True)
    (OUT / "qa/slide-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    source_slides = sources()
    reference = Presentation(ROOT / "reference/reference.pptx")
    deck = Presentation()
    deck.slide_width, deck.slide_height = reference.slide_width, reference.slide_height
    reference_theme = next(r.target_part.blob for r in reference.slide_master.part.rels.values()
                           if r.reltype.endswith("/theme"))
    for relation in deck.slide_master.part.rels.values():
        if relation.reltype.endswith("/theme"):
            relation.target_part._blob = reference_theme
    deck.core_properties.title = "CI/CD for Machine Learning"
    deck.core_properties.subject = "MLOps Essentials: AI Lifecycle Management — Session 6"
    deck.core_properties.author = "MLOps Essentials"
    deck.core_properties.keywords = "SMS, CI, CD, CT, pytest, GitHub Actions, Docker"
    deck.core_properties.comments = "Editable native PowerPoint slides; English slides and Hebrew instructor notes."
    for source in source_slides:
        slide = deck.slides.add_slide(deck.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = color(WHITE)
        textbox(slide.shapes, source.title, LEFT, .58, RIGHT - LEFT, 1.1,
                size=40, font=TITLE_FONT, bold=True, space_after=0, line_spacing=1.02,
                name=f"Slide {source.number} title — editable")
        # A small accent follows the restrained green reference identity.
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                Inches(LEFT), Inches(1.68), Inches(LEFT+.65), Inches(1.68))
        line.name = "Title accent"
        line.line.color.rgb = color(GREEN)
        line.line.width = Pt(2.5)
        lay_out(slide, source)
        textbox(slide.shapes, str(source.number), 12.05, 7.06, .55, .25,
                size=13, fill=MUTED, align=PP_ALIGN.RIGHT, space_after=0,
                name="Slide number")
        remove_effects(slide.shapes)
        add_notes(slide, source.notes)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "session6.pptx"
    deck.save(path)
    make_svgs()
    integrity(path, source_slides)
    print(f"Built {path}: 39 slides, 39 embedded Hebrew notes, five SVGs; source text verified.")


if __name__ == "__main__":
    main()
