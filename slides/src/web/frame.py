"""Shared slide frame for the HTML deck: meta row, title, question strip,
key sentence and footnote. Positions match the PPTX proofs so the design
reads the same, in inches on a 13.333 x 7.5 viewBox."""

from deck import theme as T

from . import kit

C = T.COLORS
M = T.MARGIN
CONTENT_W = T.RIGHT - T.MARGIN
TITLE_LINE = 0.66


def build(page, spec):
    """spec keys: sid, section, time, title (on-screen), question, lead_tag, lead,
    footnote. Optional: kind='break' or 'plain' for the minimal frames."""
    kit.text(page, M, 0.42, 7.2, 0.32,
             [[(f"S{spec['sid']}", T.SIZE["meta"], True, C["primary"]),
               (f"   {spec['section']}", T.SIZE["meta"], False, C["muted"])]],
             role="meta", hint="meta-left")
    kit.text(page, M + 7.2, 0.42, CONTENT_W - 7.2, 0.32,
             [[(spec["time"], T.SIZE["meta"], False, C["muted"])]],
             align="right", role="meta", hint="meta-right")

    kit.text(page, M, 0.78, CONTENT_W, TITLE_LINE,
             [[(spec["title"], T.SIZE["title"], True, C["ink"])]],
             anchor="top", role="title", hint="title")
    y = 0.78 + TITLE_LINE + 0.12
    if spec.get("kind") == "break":
        return y

    q_h = 0.6
    kit.band(page, M, y, CONTENT_W, q_h, style="lane",
             paragraphs=[[("질문   ", T.SIZE["label"], True, C["primary"]),
                          (spec["question"], T.SIZE["body"], False, C["ink"])]],
             hint="question")
    kit.band(page, M, y, 0.08, q_h, style="solid", hint="question-accent")
    y += q_h + 0.12

    lead_h = 0.5
    kit.text(page, M, y, CONTENT_W, lead_h,
             [[(f"{spec['lead_tag']}   ", T.SIZE["label"], True, C["primary"]),
               (spec["lead"], T.SIZE["body"], True, C["ink"])]],
             role="lead", hint="lead")
    y += lead_h + 0.2

    kit.text(page, M, 6.68, CONTENT_W, 0.38,
             [[(spec["footnote"], T.SIZE["footnote"], False, C["muted"])]],
             role="footnote", hint="footnote")
    return y
