#!/usr/bin/env python3
"""Build one authorized part from JSON, using native PowerPoint elements.

Run: python scripts/build_presentation.py --part 1
The JSON is the authoring source. CONTENT.md and diagram SVGs are generated.
"""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import re

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR, PP_PLACEHOLDER
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
GREEN, INK, MUTED = "196B24", "24292D", "596269"
PALE, NEUTRAL, LINE, WHITE = "F1F7F2", "F5F6F7", "D5DDD6", "FFFFFF"
LEFT, RIGHT = 0.72, 12.61
WIDTH, HEIGHT = 13.3333333333, 7.5


def load_part(part):
    manifest = json.loads((ROOT / "slides/manifest.json").read_text(encoding="utf-8"))
    entry = next(item for item in manifest["parts"] if item["part"] == part)
    if "source" not in entry:
        raise ValueError(f"Part {part} has no authorized source to build")
    source = json.loads((ROOT / entry["source"]).read_text(encoding="utf-8"))
    slides = source["slides"]
    assert len({slide["id"] for slide in slides}) == len(slides)
    assert sum(slide["minutes"] for slide in slides) == entry["minutes"]
    assert sum(slide["hands_on_minutes"] for slide in slides) == entry["hands_on_minutes"]
    if entry.get("objective_slide_id"):
        assert slides[0]["id"] == entry["objective_slide_id"]
        assert slides[0]["layout"] == "objectives"
        assert slides[0]["title"] == entry["title"]
        assert slides[0]["objective"] == entry["objective"]
        assert slides[0]["lines"] == entry["main_goals"]
    return manifest, entry, source


def rgb(value):
    return RGBColor.from_string(value)


def textbox(shapes, text, x, y, w, h, *, size=31, font="Aptos", color=INK,
            bold=False, align="left", vertical="top", space_after=0,
            name="Content::text"):
    shape = shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    shape.name = name
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.margin_left = frame.margin_right = Pt(0)
    frame.margin_top = frame.margin_bottom = Pt(0)
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE if vertical == "middle" else MSO_ANCHOR.TOP
    for index, line in enumerate(text.split("\n")):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.alignment = {"left": PP_ALIGN.LEFT, "right": PP_ALIGN.RIGHT,
                               "center": PP_ALIGN.CENTER}[align]
        paragraph.space_before = Pt(0)
        paragraph.space_after = Pt(space_after)
        paragraph.line_spacing = 1.1
        run = paragraph.add_run()
        run.text = line
        run.font.name, run.font.size = font, Pt(size)
        run.font.bold = bold
        run.font.color.rgb = rgb(color)
        run._r.get_or_add_rPr().set("lang", "en-US")
    return shape


def panel(shapes, x, y, w, h, fill=NEUTRAL, line=LINE, name="Panel"):
    shape = shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
                             Inches(x), Inches(y), Inches(w), Inches(h))
    shape.name = name
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    shape.line.color.rgb = rgb(line)
    shape.line.width = Pt(1)
    return shape


def arrow(shapes, x1, y1, x2, y2, color=GREEN):
    shape = shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                 Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    shape.name = "Diagram::editable arrow"
    shape.line.color.rgb = rgb(color)
    shape.line.width = Pt(1.8)
    end = OxmlElement("a:tailEnd")
    end.set("type", "triangle")
    shape.line._get_or_add_ln().append(end)
    return shape


def diagram_source(name):
    return json.loads((ROOT / "assets/diagrams" / f"{name}.json").read_text(encoding="utf-8"))


def add_diagram(slide, name, x, y):
    definition = diagram_source(name)
    group = slide.shapes.add_group_shape()
    group.name = f"Diagram::{name}"
    for index, item in enumerate(definition["elements"]):
        if item["type"] == "rect":
            panel(group.shapes, x + item["x"], y + item["y"], item["w"], item["h"],
                  item["fill"], item["line"], name=f"Panel::{name}-{index}")
        elif item["type"] == "arrow":
            arrow(group.shapes, x + item["x1"], y + item["y1"],
                  x + item["x2"], y + item["y2"], item["line"])
        elif item["type"] == "text":
            textbox(group.shapes, item["text"], x + item["x"], y + item["y"],
                    item["w"], item["h"], size=item["size"],
                    color=item.get("color", INK), bold=item.get("bold", False),
                    align=item.get("align", "left"), vertical=item.get("vertical", "top"),
                    name=f"Content::{name}-{index}")
        else:
            raise ValueError(item["type"])


def export_svg(name):
    definition = diagram_source(name)
    scale = 72
    width, height = definition["width"] * scale, definition["height"] * scale
    result = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width*4/3:g}" '
              f'height="{height*4/3:g}" viewBox="0 0 {width:g} {height:g}" role="img">',
              f'<title>{escape(definition["title"])}</title>',
              '<!-- Generated from the same JSON as the native PowerPoint diagram. -->']
    for item in definition["elements"]:
        if item["type"] == "rect":
            result.append(f'<rect x="{item["x"]*scale:g}" y="{item["y"]*scale:g}" '
                          f'width="{item["w"]*scale:g}" height="{item["h"]*scale:g}" '
                          f'fill="#{item["fill"]}" stroke="#{item["line"]}" stroke-width="1"/>')
        elif item["type"] == "arrow":
            assert item["y1"] == item["y2"]
            x1, x2, y = item["x1"]*scale, item["x2"]*scale, item["y1"]*scale
            result.extend([
                f'<line x1="{x1:g}" y1="{y:g}" x2="{x2-6:g}" y2="{y:g}" stroke="#{item["line"]}" stroke-width="1.8"/>',
                f'<polygon points="{x2:g},{y:g} {x2-7:g},{y-3.5:g} {x2-7:g},{y+3.5:g}" fill="#{item["line"]}"/>'])
        else:
            size = item["size"]
            lines = item["text"].split("\n")
            line_height = size * 1.1
            align = item.get("align", "left")
            x = (item["x"] + (item["w"] / 2 if align == "center" else 0)) * scale
            top = item["y"] * scale
            if item.get("vertical") == "middle":
                top += (item["h"] * scale - line_height * len(lines)) / 2
            baseline = top + size * 0.85
            anchor = "middle" if align == "center" else "start"
            result.append(f'<text x="{x:g}" y="{baseline:g}" font-family="Aptos,Arial,sans-serif" '
                          f'font-size="{size}" font-weight="{"bold" if item.get("bold") else "normal"}" '
                          f'fill="#{item.get("color", INK)}" text-anchor="{anchor}">')
            for index, line in enumerate(lines):
                result.append(f'<tspan x="{x:g}" dy="{0 if index == 0 else line_height:g}">{escape(line)}</tspan>')
            result.append('</text>')
    result.append('</svg>')
    (ROOT / "assets/diagrams" / f"{name}.svg").write_text("\n".join(result) + "\n", encoding="utf-8")


def note_text(block):
    # Keep technical identifiers intact at hyphens, and protect numeric ranges
    # from reversal inside a Hebrew paragraph. Format controls remain invisible.
    text = re.sub(r"`([^`]+)`", lambda match: "\u200e" +
                  match.group(1).replace('-', '\u2060-\u2060') + "\u200e", block["text"])
    text = re.sub(r'\d+–\d+', lambda match: '\u200e' + match.group(0) + '\u200e', text)
    return f'{block["heading"]}: {text}'


def add_notes(slide, blocks, slide_number=None):
    notes = slide.notes_slide
    for shape in list(notes.shapes):
        if shape.is_placeholder and shape.placeholder_format.type == PP_PLACEHOLDER.SLIDE_IMAGE:
            shape._element.getparent().remove(shape._element)
        elif (slide_number is not None and shape.is_placeholder and
              shape.placeholder_format.type == PP_PLACEHOLDER.SLIDE_NUMBER):
            # Materialize inherited geometry before converting the auto-number
            # placeholder into ordinary native text. Part decks then preserve
            # the course-wide number on Notes pages instead of restarting at 1.
            bounds = (shape.left, shape.top, shape.width, shape.height)
            shape.left, shape.top, shape.width, shape.height = bounds
            for placeholder in shape._element.xpath('./p:nvSpPr/p:nvPr/p:ph'):
                placeholder.getparent().remove(placeholder)
            shape.name = "Notes page number"
            shape.text_frame.text = str(slide_number)
            for paragraph in shape.text_frame.paragraphs:
                paragraph.alignment = PP_ALIGN.RIGHT
                paragraph.space_after = Pt(0)
                for run in paragraph.runs:
                    run.font.name, run.font.size = "Arial", Pt(12)
    body = notes.notes_placeholder
    assert body is not None
    body.left, body.top = Inches(0.55), Inches(0.4)
    body.width, body.height = Inches(6.4), Inches(9)
    frame = body.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.margin_left = frame.margin_right = Pt(0)
    frame.margin_top = frame.margin_bottom = Pt(0)
    for index, block in enumerate(blocks):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.alignment = PP_ALIGN.RIGHT
        paragraph.space_after = Pt(8)
        paragraph.line_spacing = 1.12
        paragraph._p.get_or_add_pPr().set("rtl", "1")
        heading, text = note_text(block).split(": ", 1)
        for text_value, bold in [(heading + ": ", True), (text, False)]:
            run = paragraph.add_run()
            run.text = text_value
            run.font.name, run.font.size = "Arial", Pt(12)
            run.font.bold = bold
            properties = run._r.get_or_add_rPr()
            properties.set("lang", "he-IL")
            for tag in ["a:cs", "a:ea"]:
                node = OxmlElement(tag)
                node.set("typeface", "Arial")
                properties.append(node)


def plain_lines(slide, lines, y=2.2, size=31, gap=0.96):
    for index, line in enumerate(lines):
        textbox(slide.shapes, line, LEFT, y + index*gap, RIGHT-LEFT, 0.8,
                size=size, name=f"Content::statement-{index+1}")


def diagram_questions(slide, source):
    add_diagram(slide, source["diagram"], LEFT, 2.2)
    plain_lines(slide, source["lines"], y=3.92, gap=0.9)


def sms_example(slide, source):
    textbox(slide.shapes, source["scenario_label"], LEFT, 2.12, 11.8, 0.5,
            size=24, color=GREEN, name="Content::synthetic-label")
    textbox(slide.shapes, source["message"], LEFT, 2.81, 11.8, 0.9,
            name="Content::SMS")
    textbox(slide.shapes, source["http"], LEFT, 3.95, 2.65, 0.7,
            size=32, name="Content::status")
    textbox(slide.shapes, source["response"], 3.6, 3.95, 8.9, 0.7,
            size=31, font="Aptos Mono", name="Content::response")
    textbox(slide.shapes, source["truth"], LEFT, 4.9, 11.8, 0.8,
            name="Content::known-label")
    textbox(slide.shapes, source["takeaway"], LEFT, 6.0, 11.8, 0.7,
            size=30, bold=True, name="Content::takeaway")


def diagram_takeaway(slide, source):
    add_diagram(slide, source["diagram"], LEFT, 2.2)
    textbox(slide.shapes, source["takeaway"], LEFT, 6.02, 11.8, 0.7,
            size=31, name="Content::takeaway")


def plain(slide, source):
    plain_lines(slide, source["lines"], y=2.2, gap=1.3)


def plain_takeaway(slide, source):
    plain_lines(slide, source["lines"], y=2.2, gap=1.2)
    textbox(slide.shapes, source["takeaway"], LEFT, 6.0, 11.8, 0.8,
            size=28, color=GREEN, name="Content::takeaway")


def lab(slide, source):
    plain_lines(slide, source["lines"], y=2.18, gap=1.0)
    textbox(slide.shapes, source["guide"], LEFT, 5.48, 11.8, 0.6,
            size=24, color=MUTED, name="Content::lab-guide")
    panel(slide.shapes, LEFT, 6.25, 2.3, 0.55, fill=PALE, line=GREEN, name="Lab time badge")
    textbox(slide.shapes, source["badge"], LEFT+0.12, 6.31, 2.05, 0.43,
            size=24, color=GREEN, name="Content::lab-time")


def report_overview(slide, source):
    for index, text in enumerate(source["lines"]):
        textbox(slide.shapes, text, LEFT, 2.05+index*.7, RIGHT-LEFT, .55,
                size=28, name=f"Content::statement-{index+1}")
    picture = slide.shapes.add_picture(str(ROOT/source["image"]), Inches(LEFT), Inches(3.45), height=Inches(2.55))
    picture.name = "Report screenshot::actual Evidently excerpt"
    textbox(slide.shapes, source["takeaway"], LEFT, 6.28, 11.8, .6,
            size=28, color=GREEN, name="Content::takeaway")


def report_chart(slide, source):
    picture = slide.shapes.add_picture(str(ROOT/source["image"]), Inches(LEFT), Inches(2.2), width=Inches(8.2))
    picture.name = "Report screenshot::actual Evidently chart"
    for index, text in enumerate(source["lines"]):
        textbox(slide.shapes, text, 9.25, 2.2+index*1.15, 3.36, 1.02,
                size=26, color=GREEN if index==0 else INK,
                bold=index==0, name=f"Content::chart-annotation-{index+1}")
    textbox(slide.shapes, source["takeaway"], LEFT, 6.02, 11.8, .7,
            size=28, name="Content::takeaway")


def objectives(slide, source):
    textbox(slide.shapes, source["objective_label"], LEFT, 2.05, 11.8, .45,
            size=24, color=GREEN, bold=True, name="Content::objective-label")
    textbox(slide.shapes, source["objective"], LEFT, 2.62, 11.8, .7,
            size=31, name="Content::objective")
    textbox(slide.shapes, source["goals_label"], LEFT, 3.65, 11.8, .45,
            size=24, color=GREEN, bold=True, name="Content::goals-label")
    for index, text in enumerate(source["lines"]):
        textbox(slide.shapes, text, LEFT, 4.22+index*.78, 11.8, .65,
                size=31, name=f"Content::goal-{index+1}")


LAYOUTS = {function.__name__: function for function in
           [diagram_questions, sms_example, diagram_takeaway, plain, plain_takeaway, lab,
            report_overview, report_chart, objectives]}


def walk(shapes):
    for shape in shapes:
        yield shape
        if shape.shape_type == 6:
            yield from walk(shape.shapes)


def source_texts(source):
    if source["layout"] == "objectives":
        return [source["objective_label"], source["objective"], source["goals_label"], *source["lines"]]
    if "diagram" in source:
        result = [item["text"] for item in diagram_source(source["diagram"])["elements"] if item["type"] == "text"]
    else:
        result = []
    if source["layout"] == "sms_example":
        return [source[key] for key in ["scenario_label", "message", "http", "response", "truth", "takeaway"]]
    result += source.get("lines", [])
    for key in ["takeaway", "guide", "badge"]:
        if key in source:
            result.append(source[key])
    return result


def markdown_source(entry, source):
    lines = [f'# Part {entry["part"]} — {entry["title"]}', '',
             '> Generated from slides.json. Edit the JSON and rebuild to preserve reproducibility.', '',
             f'**Timing:** {entry["minutes"]} minutes, including {entry["hands_on_minutes"]} hands-on.', '']
    for offset, slide in enumerate(source["slides"]):
        number = entry["first_slide"] + offset
        lines.extend([f'## Slide {number} — {slide["title"]}', '', f'**ID:** {slide["id"]}  ',
                      f'**Layout:** {slide["layout"]}  ',
                      f'**Minutes:** {slide["minutes"]}; **hands-on:** {slide["hands_on_minutes"]}', '',
                      '### Student-facing content', '', '```text',
                      '\n'.join(source_texts(slide)), '```', '', '### Embedded Hebrew notes', ''])
        lines += [f'**{block["heading"]}:** {block["text"]}\n' for block in slide["notes"]]
    return '\n'.join(lines) + '\n'


def new_deck(manifest, title):
    reference = Presentation(ROOT / manifest["reference"])
    deck = Presentation()
    deck.slide_width, deck.slide_height = reference.slide_width, reference.slide_height
    theme = next(relation.target_part.blob for relation in reference.slide_master.part.rels.values()
                 if relation.reltype.endswith('/theme'))
    for relation in deck.slide_master.part.rels.values():
        if relation.reltype.endswith('/theme'):
            relation.target_part._blob = theme
    deck.core_properties.title = title
    deck.core_properties.subject = manifest["course"]
    deck.core_properties.author = "MLOps Essentials"
    deck.core_properties.comments = "Native editable slides; embedded Hebrew notes; synthetic examples only."
    return deck


def append_part(deck, entry, source):
    part = entry["part"]
    for offset, item in enumerate(source["slides"]):
        number = entry["first_slide"] + offset
        slide = deck.slides.add_slide(deck.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = rgb(WHITE)
        textbox(slide.shapes, item["title"], LEFT, 0.58, RIGHT-LEFT, 1.1, size=40,
                font="Aptos Display", bold=True, name="Title")
        accent = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                    Inches(LEFT), Inches(1.68), Inches(LEFT+0.65), Inches(1.68))
        accent.name = "Title accent"
        accent.line.color.rgb, accent.line.width = rgb(GREEN), Pt(2.5)
        textbox(slide.shapes, f'Part {part}/5', 10.7, 0.17, 1.9, 0.26,
                size=13, color=MUTED, align="right", name="Part marker")
        LAYOUTS[item["layout"]](slide, item)
        textbox(slide.shapes, str(number), 12.05, 7.06, 0.55, 0.25,
                size=13, color=MUTED, align="right", name="Slide number")
        for shape in walk(slide.shapes):
            for effect in shape._element.xpath('./p:style/a:effectRef'):
                effect.set('idx', '0')
        add_notes(slide, item["notes"], number)


def build(part):
    manifest, entry, source = load_part(part)
    deck = new_deck(manifest, f'Monitoring & Maintenance — Part {part}: {entry["title"]}')
    append_part(deck, entry, source)
    output_dir = (ROOT / entry["source"]).parent
    output = output_dir / f'Session7_Part{part}.pptx'
    deck.save(output)
    for name in sorted({slide["diagram"] for slide in source["slides"] if "diagram" in slide}):
        export_svg(name)
    (output_dir / 'CONTENT.md').write_text(markdown_source(entry, source), encoding='utf-8')
    print(f'Built {output}: {len(source["slides"])} native slides with embedded Hebrew notes.')
    return output


def build_final():
    manifest, _, _ = load_part(1)
    deck = new_deck(manifest, 'Session 7 — Monitoring & Maintenance')
    combined = {"title":manifest["session"], "slides":[]}
    next_number = 1
    for part in range(1,6):
        _, entry, source = load_part(part)
        assert entry["first_slide"] == next_number
        append_part(deck, entry, source)
        (ROOT/entry["source"]).with_name('CONTENT.md').write_text(markdown_source(entry, source), encoding='utf-8')
        for name in sorted({s['diagram'] for s in source['slides'] if 'diagram' in s}):
            export_svg(name)
        combined["slides"] += [{**item,"part":part,"number":entry["first_slide"]+offset}
                               for offset,item in enumerate(source["slides"])]
        next_number += len(source["slides"])
    combined["minutes"] = sum(s["minutes"] for s in combined["slides"])
    combined["hands_on_minutes"] = sum(s["hands_on_minutes"] for s in combined["slides"])
    assert combined["minutes"] == 180 and combined["hands_on_minutes"] == 95
    output = ROOT/'output/Session7_Monitoring_Maintenance.pptx'
    output.parent.mkdir(parents=True, exist_ok=True)
    deck.save(output)
    qa = output.parent/'qa'
    qa.mkdir(exist_ok=True)
    (qa/'slide-manifest.json').write_text(json.dumps(combined,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Built {output}: {len(deck.slides)} editable slides, 180 minutes, 95 hands-on.')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--part', type=int, choices=range(1, 6))
    mode.add_argument('--all', action='store_true', help='Build the final deck without rewriting standalone parts')
    args = parser.parse_args()
    build_final() if args.all else build(args.part)
