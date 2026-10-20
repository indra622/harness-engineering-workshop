"""Shared slide frame: meta row, title, question strip, key sentence, footnote.

The frame keeps the same positions on every slide so the deck reads as one
system. It returns the y coordinate where the diagram area starts.
"""

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches

from . import kit
from . import theme as T

C = T.COLORS
CONTENT_W = T.RIGHT - T.MARGIN


def background(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = kit.rgb(C["canvas"])


def build(page, spec):
    """spec keys: sid, section, time, title, title_break, question, lead_tag,
    lead, footnote."""
    background(page.slide)
    m = T.MARGIN

    # meta row: section marker on the left, source slide ID and time on the right
    kit.text(page, m, 0.42, 6.0, 0.32,
             [[(f"S{spec['sid']}", T.SIZE["meta"], True, C["primary"]),
               (f"   {spec['section']}", T.SIZE["meta"], False, C["muted"])]],
             hint="meta-left")
    kit.text(page, m + 6.0, 0.42, CONTENT_W - 6.0, 0.32,
             [[(f"원본 S{spec['sid']}   {spec['time']}", T.SIZE["meta"], False, C["muted"])]],
             align=PP_ALIGN.RIGHT, hint="meta-right")

    # title: one line unless it does not fit, then break where the spec says
    title = spec["title"]
    if kit.text_width_in(title, T.SIZE["title"], True) + 2 * kit.INSET <= CONTENT_W:
        lines = [title]
    else:
        brk = spec["title_break"]
        lines = [title[:brk].rstrip(), title[brk:].lstrip()]
    title_h = 0.66 * len(lines)
    kit.text(page, m, 0.78, CONTENT_W, title_h,
             [[(ln, T.SIZE["title"], True, C["ink"])] for ln in lines],
             anchor=MSO_ANCHOR.TOP, hint="title")
    y = 0.78 + title_h + 0.12

    # question strip: tag and question on a light band, primary accent bar at left
    q_h = 0.6
    kit.band(page, m, y, CONTENT_W, q_h,
             paragraphs=[[("질문   ", T.SIZE["label"], True, C["primary"]),
                          (spec["question"], T.SIZE["body"], False, C["ink"])]],
             hint="question")
    kit.band(page, m, y, 0.08, q_h, color="primary", hint="question-accent")
    y += q_h + 0.12

    # key sentence: one definition or the opening scene
    lead_h = 0.5
    kit.text(page, m, y, CONTENT_W, lead_h,
             [[(f"{spec['lead_tag']}   ", T.SIZE["label"], True, C["primary"]),
               (spec["lead"], T.SIZE["body"], True, C["ink"])]],
             hint="lead")
    y += lead_h + 0.2

    # footnote: caveat or source, one line at 16 pt
    kit.text(page, m, 6.68, CONTENT_W, 0.38,
             [[(spec["footnote"], T.SIZE["footnote"], False, C["muted"])]],
             hint="footnote")
    return y
