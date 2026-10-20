"""Speaker notes from the source documents.

Notes carry the full v10 block for the slide (scene, question, definition,
details, scene application, backup example, distinction, check and answer,
time) plus the production brief entry. Markdown emphasis is removed so the
notes read as plain text in PowerPoint and LibreOffice.
"""

import re
from pathlib import Path

PLAN = "docs/plans/slide-content-plan-v10.md"
BRIEF = "docs/production/slide-production-brief-v01.md"


def _block(text, sid):
    m = re.search(r"(?ms)^### S%d\. .*?(?=^### S\d+\. |^## )" % sid, text)
    if not m:
        raise KeyError(f"S{sid} not found")
    return m.group(0)


def _plain(md):
    out = []
    for line in md.strip().splitlines():
        line = line.replace("**", "")
        line = re.sub(r"^### ", "", line)
        out.append(line.rstrip())
    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text)


def heading(root, sid):
    plan = (Path(root) / PLAN).read_text(encoding="utf-8")
    first = _block(plan, sid).splitlines()[0]
    m = re.match(r"### S\d+\. (.+) \((\d+)분부터 (\d+)분까지, (\d+)분\)$", first)
    return {"title": m.group(1), "start": int(m.group(2)), "end": int(m.group(3)),
            "minutes": int(m.group(4))}


def notes_for(root, sid):
    plan = (Path(root) / PLAN).read_text(encoding="utf-8")
    brief = (Path(root) / BRIEF).read_text(encoding="utf-8")
    h = heading(root, sid)
    head = (f"원본 v10 S{sid}. {h['title']}\n"
            f"시간: {h['start']}분부터 {h['end']}분까지, {h['minutes']}분\n"
            f"출처: {PLAN} S{sid}, {BRIEF} S{sid}")
    body = _plain(_block(plan, sid))
    prod = _plain(_block(brief, sid))
    return (f"{head}\n\n[v10 원문]\n{body}\n\n[제작 브리프]\n{prod}\n")
