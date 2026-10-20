"""Drawing kit for the v02 deck: inline SVG on canvas pixels, plus small HTML helpers.

Every slide is a 1920 x 1080 canvas. Diagrams are inline SVG with real text,
one <text> element per line so the browser check can measure each label.
Marker ids carry the slide number because all slides share one document.
"""

from html import escape

INK = "#14171C"
INK2 = "#3A4049"
MUTED = "#5E6570"
RULE = "#CFCBC2"
PAPER = "#F5F3EE"
PAPER2 = "#ECE9E1"
BLUE = "#2457A6"
BLUE_SOFT = "#E1E9F6"
AMBER = "#B45309"
AMBER_SOFT = "#FBECDB"
WHITE = "#FFFFFF"
NIGHT = "#11151B"
NIGHT2 = "#1B2129"
NIGHT_LINE = "#3B4552"
NIGHT_TEXT = "#ECEEF1"
NIGHT_MUTED = "#A2AAB5"
SKY = "#8DB4FF"
CHAPTER_SOFT = "#BFD3FF"
MONO = "SF Mono, Menlo, Consolas, monospace"

# Deck version being built. build_v02.py sets it before the slide functions run;
# slides that differ between versions read it. "v02" reproduces the v02 export.
VERSION = "v02"

MARKERS = {"ink": INK, "blue": BLUE, "amber": AMBER, "muted": MUTED, "white": WHITE, "sky": SKY}


def e(s):
    return escape(str(s), quote=False)


class Svg:
    """One inline SVG placed on the canvas at (x, y)."""

    def __init__(self, sid, x, y, w, h, label):
        self.sid, self.x, self.y, self.w, self.h, self.label = sid, x, y, w, h, label
        self.parts = []
        self.used = set()

    def add(self, s):
        self.parts.append(s)
        return self

    def rect(self, x, y, w, h, fill=WHITE, stroke=None, sw=2.5, dash=None, extra=""):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{st}{da}{extra}/>')

    def text(self, x, y, s, size=28, weight=400, fill=INK, anchor="start", mono=False, mid=True):
        fam = f' font-family="{MONO}"' if mono else ""
        db = ' dominant-baseline="central"' if mid else ""
        an = f' text-anchor="{anchor}"' if anchor != "start" else ""
        wt = f' font-weight="{weight}"' if weight != 400 else ""
        return self.add(f'<text x="{x}" y="{y}" font-size="{size}"{wt} fill="{fill}"{an}{fam}{db}>{e(s)}</text>')

    def lines(self, x, cy, lines, size=28, weight=400, fill=INK, anchor="start", lh=1.32, mono=False):
        """Lines centred as a block on cy."""
        step = size * lh
        top = cy - step * (len(lines) - 1) / 2
        for i, s in enumerate(lines):
            if isinstance(s, tuple):
                s, kw = s
                self.text(x, round(top + i * step, 1), s, **{"size": size, "weight": weight, "fill": fill,
                                                             "anchor": anchor, "mono": mono, **kw})
            else:
                self.text(x, round(top + i * step, 1), s, size=size, weight=weight, fill=fill,
                          anchor=anchor, mono=mono)
        return self

    def box(self, x, y, w, h, lines, size=30, weight=700, fill=WHITE, stroke=INK, sw=2.5, color=INK,
            dash=None, align="middle", pad=26, lh=1.32, mono=False):
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, dash=dash)
        if isinstance(lines, str):
            lines = [lines]
        tx = x + w / 2 if align == "middle" else x + pad
        self.lines(tx, y + h / 2, lines, size=size, weight=weight, fill=color, anchor=align, lh=lh, mono=mono)
        return self

    def arrow(self, pts, color="ink", sw=3, dash=None, head=True, tail=False):
        c = MARKERS[color]
        p = " ".join(f"{a},{b}" for a, b in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = ""
        if head:
            mk += f' marker-end="url(#{self.sid}-{color})"'
        if tail:
            mk += f' marker-start="url(#{self.sid}-{color}-s)"'
        self.used.add(color)
        return self.add(f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="{sw}"{da}{mk}/>')

    def line(self, x1, y1, x2, y2, color=RULE, sw=2, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{da}/>')

    def num(self, cx, cy, n, fill=INK, r=20, size=24):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')
        return self.text(cx, cy + 1, str(n), size=size, weight=800, fill=WHITE, anchor="middle")

    def check(self, x, y, ok=True, s=40):
        """ok=True: blue tick, ok=False: amber cross, ok=None: amber question mark (not yet checked)."""
        if ok is None:
            self.rect(x, y, s, s, fill=AMBER_SOFT, stroke=AMBER, sw=2)
            return self.text(x + s / 2, y + s / 2 + 1, "?", size=round(s * 0.62), weight=800, fill=AMBER, anchor="middle")
        if ok:
            self.rect(x, y, s, s, fill=BLUE_SOFT)
            self.add(f'<path d="M{x + s * .24} {y + s * .52} L{x + s * .43} {y + s * .71} L{x + s * .77} {y + s * .3}" '
                     f'fill="none" stroke="{BLUE}" stroke-width="{s / 9:.1f}"/>')
        else:
            self.rect(x, y, s, s, fill=AMBER_SOFT)
            self.add(f'<path d="M{x + s * .28} {y + s * .28} L{x + s * .72} {y + s * .72} M{x + s * .72} {y + s * .28} '
                     f'L{x + s * .28} {y + s * .72}" fill="none" stroke="{AMBER}" stroke-width="{s / 9:.1f}"/>')
        return self

    def render(self):
        defs = []
        for name in sorted(self.used):
            c = MARKERS[name]
            defs.append(f'<marker id="{self.sid}-{name}" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="14" '
                        f'markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0.5 L10,5 L0,9.5 z" '
                        f'fill="{c}"/></marker>')
            defs.append(f'<marker id="{self.sid}-{name}-s" viewBox="0 0 10 10" refX="0.5" refY="5" markerWidth="14" '
                        f'markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M10,0.5 L0,5 L10,9.5 z" '
                        f'fill="{c}"/></marker>')
        d = f"<defs>{''.join(defs)}</defs>" if defs else ""
        body = "\n    ".join(self.parts)
        return (f'<svg class="svg" style="left:{self.x}px;top:{self.y}px" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{e(self.label)}">{d}\n    {body}\n  </svg>')


def p(cls, html, tag="p", style=""):
    st = f' style="{style}"' if style else ""
    return f'<{tag} class="abs {cls}"{st}>{html}</{tag}>'


def kicker(cls, chapter, index):
    return p(f"kicker {cls}", f'<span class="dot"></span>{chapter}장<span class="gap"></span>용어 {index} / 25')


def case_head(n, name):
    return p("kicker case-head", f'<span class="tag-case">사례 {n} / 5</span>{e(name)}')


def scene(cls, quote, question, style=""):
    return (f'<div class="abs scene {cls}"{" style=" + chr(34) + style + chr(34) if style else ""}>'
            f'<p class="lab">장면</p><p class="say">{quote}</p><p class="ask">{question}</p></div>')


def diff(text, style=""):
    st = f' style="{style}"' if style else ""
    return (f'<div class="abs term-diff"{st}><span class="lab">헷갈리기 쉬운 점</span>'
            f'<span class="txt">{text}</span></div>')
