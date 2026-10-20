"""Build the v02 redesign proof as one self-contained HTML file.

Usage (from the project root):
    python3 slides/src/v02/build_proof.py

Reads slides/src/v02/proof.src.html, inlines v02.css and v02.js, fills the
presenter notes of the content slides with the full v10 source block, and
writes slides/previews/redesign-v02.html. Needs only the Python standard
library (notes extraction comes from slides/src/deck/notes.py).
"""

import re
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent
ROOT = SRC.parent.parent
sys.path.insert(0, str(SRC))

from deck import notes  # noqa: E402

OUT = ROOT / "slides" / "previews" / "redesign-v02.html"


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
            out.append(f"<p><strong>{escape(m.group(1))}:</strong> {escape(m.group(2))}</p>" if m
                       else f"<p>{escape(s)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def main():
    html = (HERE / "proof.src.html").read_text(encoding="utf-8")
    css = (HERE / "v02.css").read_text(encoding="utf-8")
    js = (HERE / "v02.js").read_text(encoding="utf-8")
    if "</style" in css or "</script" in js:
        raise SystemExit("asset contains a closing tag; cannot inline safely")
    html = html.replace("{{CSS}}", css).replace("{{JS}}", js)
    for sid in sorted({int(n) for n in re.findall(r"\{\{V10:(\d+)\}\}", html)}):
        html = html.replace(f"{{{{V10:{sid}}}}}", notes_html(notes.notes_for(ROOT, sid)))
    if "{{" in html:
        raise SystemExit("unfilled placeholder left in the page")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(html.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
