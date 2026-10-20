"""SVG drawing kit for the HTML deck.

Each slide is one inline SVG with viewBox 0 0 13.333 7.5, so every coordinate
is in inches and every size in points converts with pt / 72. Text is native
SVG text (selectable, searchable, scales without blur). Labels use explicit
line breaks; real font metrics decide layout, and the browser check measures
the rendered text again.

Every element is recorded on the Page so the build can check bounds, overlap
and connectors that pass through boxes before anything is written.
"""

from html import escape

from deck import theme as T
from deck.metrics import text_width_in  # Nanum Gothic metrics via Pillow

C = T.COLORS
L = T.SIZE["label"]
LINE_HEIGHT = 1.2
INSET = 0.07
INSET_V = 0.04


def pt(size):
    return size / 72


class Box:
    __slots__ = ("x", "y", "w", "h", "role", "name", "parent", "shape")

    def __init__(self, x, y, w, h, role, name, parent=None, shape="rect"):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.role, self.name, self.parent, self.shape = role, name, parent, shape

    def side(self, s):
        return {"right": (self.x + self.w, self.y + self.h / 2),
                "left": (self.x, self.y + self.h / 2),
                "top": (self.x + self.w / 2, self.y),
                "bottom": (self.x + self.w / 2, self.y + self.h)}[s]


class Page:
    def __init__(self, sid):
        self.sid = sid
        self.parts = []      # svg fragments in paint order
        self.boxes = []      # Box records for checks
        self.arrows = []     # (points, src, dst) for crossing checks
        self.texts = []      # text records (paragraphs, box, align) for fit checks
        self.colors_used = set()
        self._n = 0

    def name(self, hint):
        self._n += 1
        return f"s{self.sid}-{self._n:02d}-{hint}"

    def add(self, frag):
        self.parts.append(frag)


# ------------------------------------------------------------------ text

def _line_height(runs):
    return max(r[1] for r in runs) * LINE_HEIGHT / 72


def runs_of(text, size, bold=False, color=None):
    color = color or C["ink"]
    return [[(line, size, bold, color)] for line in text.split("\n")]


def _text_svg(page, x, y, w, h, paragraphs, align="center", anchor="middle",
              margin_left=INSET, role="label", box_name=""):
    heights = [_line_height(p) for p in paragraphs if p]
    total = sum(heights)
    if anchor == "middle":
        cy = y + (h - total) / 2
    else:
        cy = y + INSET_V
    if align == "left":
        tx, ta = x + margin_left, "start"
    elif align == "right":
        tx, ta = x + w - INSET, "end"
    else:
        tx, ta = x + w / 2, "middle"
    lines = []
    for runs, lh in zip([p for p in paragraphs if p], heights):
        mid = cy + lh / 2
        spans = []
        for text, size, bold, color in runs:
            weight = ' font-weight="700"' if bold else ""
            spans.append(f'<tspan font-size="{pt(size):.4f}"{weight} fill="#{color}">'
                         f'{escape(text)}</tspan>')
        lines.append(f'<text x="{tx:.4f}" y="{mid:.4f}" text-anchor="{ta}" '
                     f'dominant-baseline="central" xml:space="preserve">{"".join(spans)}</text>')
        cy += lh
    ml = margin_left if align == "left" else INSET
    page.texts.append({"name": box_name, "x": x, "y": y, "w": w, "h": h,
                       "paragraphs": paragraphs, "inset_l": ml, "inset_r": INSET,
                       "role": role})
    return (f'<g class="tx" data-name="{box_name}" data-role="{role}" '
            f'data-box="{x:.4f} {y:.4f} {w:.4f} {h:.4f}" '
            f'data-inset="{ml:.4f} {INSET:.4f} {INSET_V:.4f}">{"".join(lines)}</g>')


def text(page, x, y, w, h, paragraphs, align="left", anchor="middle", role="text",
         parent=None, hint="text", margin_left=INSET):
    nm = page.name(hint)
    page.add(_text_svg(page, x, y, w, h, paragraphs, align, anchor, margin_left, role, nm))
    b = Box(x, y, w, h, "T", nm, parent)
    page.boxes.append(b)
    return b


# ------------------------------------------------------------------ shapes

STYLES = {
    # fill, stroke, stroke width (pt), dashed, text color, bold
    "base":     ("surface", "ink", 1.25, False, "ink", False),
    "focus":    ("focus_fill", "primary", 2.25, False, "ink", False),
    "gate":     ("surface", "warning", 3.0, False, "ink", True),
    "retained": ("canvas", "muted", 2.0, True, "ink", False),
    "out":      (None, "muted", 1.25, True, "muted", False),
    "chip":     ("band", None, 0, False, "ink", False),
    "plain":    ("surface", None, 0, False, "ink", False),
    "note":     (None, "muted", 1.0, True, "muted", False),
    "caution":  ("surface", "warning", 2.0, True, "warning", True),
    "tile":     ("surface", "hairline", 1.0, False, "ink", False),
    "scope":    (None, "primary", 2.0, False, "ink", False),
    "solid":    ("primary", None, 0, False, "surface", True),
    "lane":     ("band", None, 0, False, "ink", False),
    "lane_focus": ("focus_fill", "primary", 2.0, False, "ink", False),
}


def _shape_svg(x, y, w, h, style, radius=0.09, shape="rect"):
    fill, stroke, sw, dash, _, _ = STYLES[style]
    f = f'#{C[fill]}' if fill else "none"
    s = f'#{C[stroke]}' if stroke else "none"
    d = f' stroke-dasharray="{pt(sw) * 3.2:.4f} {pt(sw) * 2.4:.4f}"' if dash else ""
    if shape == "diamond":
        pts = f"{x + w / 2:.4f},{y:.4f} {x + w:.4f},{y + h / 2:.4f} {x + w / 2:.4f},{y + h:.4f} {x:.4f},{y + h / 2:.4f}"
        return (f'<polygon points="{pts}" fill="{f}" stroke="{s}" '
                f'stroke-width="{pt(sw):.4f}"{d} stroke-linejoin="round"/>')
    r = min(radius, w / 2, h / 2)
    return (f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" rx="{r:.4f}" '
            f'fill="{f}" stroke="{s}" stroke-width="{pt(sw):.4f}"{d}/>')


def node(page, x, y, w, h, label, style="base", size=L, parent=None, hint=None,
         align="center", paragraphs=None, shape="rect", radius=0.09):
    _, _, _, _, tcolor, bold = STYLES[style]
    nm = page.name(hint or label.split("\n")[0][:12])
    paras = paragraphs or runs_of(label, size, bold, C[tcolor])
    svg = _shape_svg(x, y, w, h, style, radius, shape)
    if shape == "diamond":   # text sits in the inner rectangle of the diamond
        tsvg = _text_svg(page, x + w * 0.2, y + h * 0.22, w * 0.6, h * 0.56, paras, align,
                         "middle", INSET, "label", nm)
    else:
        tsvg = _text_svg(page, x, y, w, h, paras, align, "middle", INSET, "label", nm)
    page.add(f'<g class="node node-{style}">{svg}{tsvg}</g>')
    b = Box(x, y, w, h, "N", nm, parent, shape)
    page.boxes.append(b)
    return b


def container(page, x, y, w, h, style="scope", hint="container", radius=0.12):
    nm = page.name(hint)
    page.add(f'<g class="container">{_shape_svg(x, y, w, h, style, radius)}</g>')
    b = Box(x, y, w, h, "C", nm)
    page.boxes.append(b)
    return b


def band(page, x, y, w, h, style="lane", paragraphs=None, hint="band", margin_left=0.3):
    nm = page.name(hint)
    parts = [_shape_svg(x, y, w, h, style, radius=0.0)]
    if paragraphs:
        parts.append(_text_svg(page, x, y, w, h, paragraphs, "left", "middle", margin_left,
                               "band", nm))
    page.add(f'<g class="band">{"".join(parts)}</g>')
    b = Box(x, y, w, h, "B", nm)
    page.boxes.append(b)
    return b


# ------------------------------------------------------------------ connectors

def _poly_svg(page, pts, color, width, dash):
    page.colors_used.add(color)
    d = " ".join(f"{px:.4f},{py:.4f}" for px, py in pts)
    da = ' stroke-dasharray="0.06 0.045"' if dash else ""
    return (f'<polyline class="arrow" points="{d}" fill="none" stroke="#{C[color]}" '
            f'stroke-width="{pt(width):.4f}"{da} stroke-linejoin="round" '
            f'marker-end="url(#ah-{page.sid}-{color})"/>')


def arrow(page, a, b, sa="right", sb="left", color="ink", width=1.5, dash=False,
          elbow=False):
    """Arrow from box a (side sa) to box b (side sb). Elbow routes orthogonally:
    horizontal sides go H-V-H, vertical sides go V-H-V."""
    p1, p2 = a.side(sa), b.side(sb)
    if a.shape == "diamond" or b.shape == "diamond":
        pass
    if not elbow or (abs(p1[0] - p2[0]) < 1e-3 or abs(p1[1] - p2[1]) < 1e-3):
        pts = [p1, p2]
    elif sa in ("left", "right"):
        mx = (p1[0] + p2[0]) / 2
        pts = [p1, (mx, p1[1]), (mx, p2[1]), p2]
    else:
        my = (p1[1] + p2[1]) / 2
        pts = [p1, (p1[0], my), (p2[0], my), p2]
    page.add(_poly_svg(page, pts, color, width, dash))
    page.arrows.append((pts, a.name, b.name))


def path_arrow(page, pts, color="ink", width=1.5, dash=False, src=None, dst=None):
    page.add(_poly_svg(page, pts, color, width, dash))
    page.arrows.append((pts, src.name if src else None, dst.name if dst else None))


def line(page, pts, color="muted", width=1.25, dash=True):
    d = " ".join(f"{px:.4f},{py:.4f}" for px, py in pts)
    da = ' stroke-dasharray="0.06 0.045"' if dash else ""
    page.add(f'<polyline points="{d}" fill="none" stroke="#{C[color]}" '
             f'stroke-width="{pt(width):.4f}"{da}/>')
    page.arrows.append((pts, None, None))


def markers(page):
    out = []
    for color in sorted(page.colors_used):
        out.append(f'<marker id="ah-{page.sid}-{color}" viewBox="0 0 10 10" refX="9.6" refY="5" '
                   f'markerUnits="userSpaceOnUse" markerWidth="0.13" markerHeight="0.13" '
                   f'orient="auto"><path d="M0,0.6 L10,5 L0,9.4 z" fill="#{C[color]}"/></marker>')
    return f'<defs>{"".join(out)}</defs>'


def width_in(s, size=L, bold=False):
    return text_width_in(s, size, bold)
