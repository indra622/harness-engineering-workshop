"""Build the HTML presentation (canonical output).

Usage (from the project root):
    python3 slides/src/build_html.py

Writes slides/index-v01.html (35 slides, inline SVG diagrams, presenter notes)
and slides/speaker-notes.md. Before writing, every slide is checked for
shapes outside the 0.4 in safe area, text that does not fit its box (real
Nanum Gothic metrics), unintended overlaps between boxes and labels, and
connectors that pass through boxes. Any failure stops the build.
"""

import re
import sys
from html import escape
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from deck import notes  # noqa: E402
from deck import theme as T  # noqa: E402
from web import kit  # noqa: E402
from web.slides import SCREEN_TITLES, SLIDES  # noqa: E402

OUT = ROOT / "slides" / "index-v01.html"  # slides/index.html is now the v02 entry
NOTES_MD = ROOT / "slides" / "speaker-notes.md"
STANDALONE = ROOT / "slides" / "harness-engineering-workshop-v01.html"
EPS = 0.02


# ------------------------------------------------------------------ checks

def _seg_hits_rect(p, q, r, pad=0.03):
    """Liang-Barsky: does segment p-q cross the rectangle r shrunk by pad?"""
    x0, y0, x1, y1 = r.x + pad, r.y + pad, r.x + r.w - pad, r.y + r.h - pad
    if x1 <= x0 or y1 <= y0:
        return False
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pp) < 1e-12:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def check_page(page):
    problems = []
    for b in page.boxes:
        if (b.x < T.SAFE - 1e-3 or b.y < T.SAFE - 1e-3 or b.x + b.w > T.SLIDE_W - T.SAFE + 1e-3
                or b.y + b.h > T.SLIDE_H - T.SAFE + 1e-3):
            problems.append(f"outside safe area: {b.name}")
    for t in page.texts:
        total = 0.0
        last = 0.0
        for runs in t["paragraphs"]:
            if not runs:
                continue
            width = sum(kit.width_in(txt, size, bold) for txt, size, bold, _ in runs)
            avail = t["w"] - t["inset_l"] - t["inset_r"]
            if width > avail + 0.01:
                problems.append(f"text too wide: {t['name']} '{''.join(r[0] for r in runs)[:24]}' "
                                f"{width:.2f} > {avail:.2f}")
            for _, size, _, _ in runs:
                floor = T.SIZE["label"] if t["role"] == "label" else T.SIZE["footnote"]
                if size < floor:
                    problems.append(f"font below {floor}pt: {t['name']}")
            last = max(r[1] for r in runs) / 72
            total += last * kit.LINE_HEIGHT
        # glyph extent: full line pitch for all but the last line, one em for the last
        total -= last * (kit.LINE_HEIGHT - 1.0)
        if total > t["h"] - 2 * kit.INSET_V + 0.01:
            problems.append(f"text too tall: {t['name']} {total:.2f} > {t['h']:.2f}")
    solid = [b for b in page.boxes if b.role in ("N", "T")]
    for a, b in combinations(solid, 2):
        ox = min(a.x + a.w, b.x + b.w) - max(a.x, b.x)
        oy = min(a.y + a.h, b.y + b.h) - max(a.y, b.y)
        if ox > EPS and oy > EPS:
            problems.append(f"overlap: {a.name} x {b.name}")
    for pts, src, dst in page.arrows:
        for p, q in zip(pts, pts[1:]):
            for b in solid:
                if b.name in (src, dst):
                    continue
                if _seg_hits_rect(p, q, b):
                    problems.append(f"connector crosses {b.name}")
    return problems


# ------------------------------------------------------------------ notes

def notes_html(text):
    out, in_list = [], False
    for line in text.splitlines():
        s = line.strip()
        if not s:
            if in_list:
                out.append("</ul>")
                in_list = False
            continue
        if s.startswith("[") and s.endswith("]"):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h3>{escape(s[1:-1])}</h3>")
        elif s.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{escape(s[2:])}</li>")
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            m = re.match(r"^([^:]{2,40}):\s(.*)$", s)
            if m and not s.startswith("http"):
                out.append(f"<p><strong>{escape(m.group(1))}:</strong> {escape(m.group(2))}</p>")
            else:
                out.append(f"<p>{escape(s)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


# ------------------------------------------------------------------ page

def render_slide(sid):
    h = notes.heading(ROOT, sid)
    page = kit.Page(sid)
    SLIDES[sid](page, h)
    screen = SCREEN_TITLES.get(sid, h["title"])
    svg = (f'<svg class="slide-svg" viewBox="0 0 {T.SLIDE_W} {T.SLIDE_H}" role="img" '
           f'aria-labelledby="t-s{sid}" preserveAspectRatio="xMidYMid meet">'
           f'<title id="t-s{sid}">S{sid}. {escape(screen)}</title>'
           f'<rect width="{T.SLIDE_W}" height="{T.SLIDE_H}" fill="#{T.COLORS["canvas"]}"/>'
           f'{kit.markers(page)}{"".join(page.parts)}</svg>')
    text = notes.notes_for(ROOT, sid)
    section = (f'<section class="slide" id="s{sid}" data-sid="{sid}" '
               f'data-title="{escape(screen)}" data-canonical-title="{escape(h["title"])}" '
               f'data-minutes="{h["minutes"]}" aria-label="S{sid}. {escape(screen)}">\n'
               f'<div class="stage">{svg}</div>\n'
               f'<aside class="notes" aria-label="S{sid} 발표자 노트">\n{notes_html(text)}\n</aside>\n'
               f'</section>')
    return section, check_page(page), text, h


TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>하네스 엔지니어링 워크샵</title>
<meta name="description" content="120분 워크샵 발표 자료. 용어 25개와 사례 다섯 개.">
<link rel="stylesheet" href="assets/deck.css">
<script src="assets/deck.js" defer></script>
</head>
<body>
<div class="deck" id="deck">
<main class="viewport" id="viewport" aria-live="polite">
{slides}
</main>
<aside class="notes-panel" id="notes-panel" aria-label="발표자 노트" hidden>
<div class="notes-head"><span>발표자 노트</span><button type="button" class="ctl" id="notes-close" aria-label="노트 닫기">닫기</button></div>
<div class="notes-body" id="notes-body"></div>
</aside>
<nav class="controls" aria-label="슬라이드 이동">
<button type="button" class="ctl" id="prev" aria-label="이전 슬라이드">이전</button>
<div class="progress" aria-hidden="true"><span id="progress-bar"></span></div>
<span class="counter" id="counter" aria-live="polite">1 / {count}</span>
<span class="now" id="now-title"></span>
<button type="button" class="ctl" id="notes-toggle" aria-pressed="false" aria-controls="notes-panel">노트 (N)</button>
<button type="button" class="ctl" id="next" aria-label="다음 슬라이드">다음</button>
</nav>
</div>
<noscript><p class="noscript">자바스크립트 없이도 모든 슬라이드가 아래로 이어져 보입니다.</p></noscript>
</body>
</html>
"""


def main():
    ids = sorted(SLIDES)
    sections, problems, md = [], [], ["# 하네스 엔지니어링 워크샵 발표자 노트", "",
                                      "slides/index.html의 발표자 노트와 같은 내용이다. 원천은 "
                                      f"{notes.PLAN}와 {notes.BRIEF}다.", ""]
    for sid in ids:
        sec, probs, text, h = render_slide(sid)
        sections.append(sec)
        problems += [f"S{sid}: {p}" for p in probs]
        md += [f"## S{sid}. {h['title']}", "", text.strip(), ""]
    if problems:
        for p in problems:
            print("FAIL", p)
        print(f"{len(problems)} problem(s); nothing written")
        sys.exit(1)
    html = TEMPLATE.replace("{slides}", "\n".join(sections)).replace("{count}", str(len(ids)))
    OUT.write_text(html, encoding="utf-8")
    NOTES_MD.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")
    STANDALONE.write_text(standalone(html), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(ids)} slides), {STANDALONE.relative_to(ROOT)} "
          f"and {NOTES_MD.relative_to(ROOT)}")


def standalone(html):
    """Single-file export: the same page with deck.css and deck.js inlined.
    SVG diagrams are already inline, so the file needs nothing next to it."""
    css = (ROOT / "slides" / "assets" / "deck.css").read_text(encoding="utf-8")
    js = (ROOT / "slides" / "assets" / "deck.js").read_text(encoding="utf-8")
    if "</script" in js or "</style" in css:
        raise SystemExit("asset contains a closing tag; cannot inline safely")
    link = '<link rel="stylesheet" href="assets/deck.css">'
    script = '<script src="assets/deck.js" defer></script>'
    assert html.count(link) == 1 and html.count(script) == 1
    html = html.replace(link, f"<style>\n{css}</style>")
    # inline scripts cannot be deferred, so the inlined script goes at the end of body
    html = html.replace(script, "")
    return html.replace("</body>", f"<script>\n{js}</script>\n</body>")


if __name__ == "__main__":
    main()
