"""Build the 42-slide deck as one self-contained HTML file.

Usage (from the project root):
    python3 slides/src/v02/build_v02.py                 # current version, v17
    python3 slides/src/v02/build_v02.py --version v03   # reproduces the v03 export
    python3 slides/src/v02/build_v02.py --version v02 --out-dir /tmp/x

Writes, for version VER, into slides/ (or --out-dir):
    harness-engineering-workshop-VER.html   canonical single-file export
    harness-engineering-workshop-VER.manifest.json
    speaker-notes-VER.md
    index.html                              only for the current version in slides/

v03 adds a physical page number inside every canvas and redraws slide 2 so the
author finds the topic and writes v01 before any AI review. v04 removes all
lecture timing (screen, notes, manifest, data attributes) and applies the
edited presentation copy from copy_v04.py; v05 drops the roadmap break marker
(copy_v05.py); v06 clarifies roles and wording (copy_v06.py); v07 inserts two
reference slides after the OMH case for 44 pages (copy_v07.py); v08 to v11 revise single slides
(copy_v08.py ... copy_v15.py, v11 reframes slide 15, v12 rewrites 14, 15 and 27, v13 retells 14 by role,
v14 shows the bare OpenCode process on 14, v15 changes its summary); v16 redraws the Grokbot case and adds
참고 C after it for 45 pages (copy_v16.py). Everything else is shared, so v02
and v03 still build byte-for-byte as exported.

Slide content lives in deck_a.py and deck_b.py. Term and case notes carry the
v10 block for that slide (in full for v02 and v03, as a labelled excerpt
without lecture timing for v04). The build stops before writing if the deck no
longer adds up: 42 slides, 25 distinct terms in v10 order, five cases, one
CEO Agent slide and one break, plus 120 minutes for the timed versions.
Needs only the Python standard library.
"""

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent
ROOT = SRC.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SRC))

import copy_v04  # noqa: E402
import copy_v05  # noqa: E402
import copy_v06  # noqa: E402
import copy_v07  # noqa: E402
import copy_v08  # noqa: E402
import copy_v09  # noqa: E402
import copy_v10  # noqa: E402
import copy_v11  # noqa: E402
import copy_v12  # noqa: E402
import copy_v13  # noqa: E402
import copy_v14  # noqa: E402
import copy_v15  # noqa: E402
import copy_v16  # noqa: E402
import copy_v17  # noqa: E402
import kit  # noqa: E402
from deck import notes as v10notes  # noqa: E402
from deck_a import SLIDES_A  # noqa: E402
from deck_b import SLIDES_B  # noqa: E402

SLIDES_DIR = ROOT / "slides"
# versions compare as strings; two digits after "v" keep that ordering correct up to v99
CURRENT = "v17"
VERSIONS = ("v02", "v03", "v04", "v05", "v06", "v07", "v08", "v09", "v10", "v11", "v12", "v13", "v14", "v15", "v16", "v17")
PLAN = ROOT / v10notes.PLAN

# Page number: inside the canvas, so it prints; bottom right, clear of the footers.
PAGENO_CSS = """
/* v03: physical page number, inside the canvas so print and PDF carry it */
.pageno { position: absolute; right: 64px; top: 1000px; margin: 0; font-size: 24px; font-weight: 700;
  letter-spacing: 0.04em; font-variant-numeric: tabular-nums; color: var(--muted); }
.t-night .pageno { color: var(--night-muted); }
.t-chapter .pageno { color: var(--chapter-soft); }
"""

# v04: the break slide loses its duration line, so its title moves down to keep the balance.
V04_CSS = """
/* v04: no lecture timing; break title recentred, edited-excerpt label in notes */
.brk-word { top: 330px; }
.notes-body .src { color: var(--muted); font-size: 14px; }
"""

# Minutes per physical slide, from docs/production/slide-production-brief-v02.md.
MINUTES = [1, 2, 1,
           1, 3, 3, 3, 3, 5,
           1, 3, 3, 3, 5, 2, 2, 3, 3,
           1, 3, 3, 2, 3, 3, 5,
           10,
           1, 3, 3, 3, 3,
           1, 3, 3, 3, 3, 2, 2, 3, 4,
           1, 5]

V10_TERMS = ["모델", "에이전트", "런타임", "하네스", "오케스트레이션", "도구", "스킬", "플러그인", "커넥터", "MCP",
             "프롬프트", "컨텍스트", "토큰", "컨텍스트 창", "메모리", "세션", "워커", "서브에이전트", "워크플로우",
             "자동화", "완료 보고", "검증", "로컬 실행", "클라우드 실행", "리모트 컨트롤"]


# v02 clarifications that override ambiguous wording or diagram prescriptions in the v10 block.
# The v10 block itself stays in the notes unchanged, under a source heading.
CORRECTIONS = {
    9: ("v10은 OpenClaw를 '로컬 구조'라고 부른다. v02 화면은 '작업 구조'라고 쓴다. 게이트웨이, 코디네이터, 워커가 "
        "어디서 도는지와 모델 추론이 어디서 일어나는지는 따로 확인하고 따로 말한다."),
    23: ("v10의 '압축은 현재 창을 줄이는 일'은 이전 표현이다. 압축은 창에 넣는 내용, 즉 입력의 분량을 줄이는 일이며 "
         "모델의 컨텍스트 창 크기는 그대로다. 화면의 현재 표현을 따른다."),
    29: ("그림의 경계는 작업 지시상 범위이지 권한 샌드박스가 아니다. 실제로 강제되는 권한은 도구와 런타임 설정이 정한다. "
         "v10의 '권한 경계', '쓰기 금지' 표현을 기술적으로 막힌 환경을 시연한 것으로 읽지 않는다."),
    30: ("v10 화면 구성의 '쓰기 권한 없음'은 v02에서 '읽기 전용 작업 지시 (이번 예시)'로 바뀌었다. 지시만으로 실제 "
         "쓰기 권한이 사라지지는 않는다. 권한은 설정에 따라 다르다."),
}

# v03 corrections, shown only in v03 notes.
CORRECTIONS_V03 = {
    2: ("v10 S1과 2.3은 '사용자가 원문을 보냈고, 받은 본문을 v01로 보존한다'고만 적어, v01이 누가 쓴 원고인지 드러내지 "
        "않는다. 실제 순서는 작가가 주제를 찾고 고른다, 작가가 초고 v01을 직접 쓴다, AI와 함께 검토하고 수정한다, 작가가 "
        "최종 확정한다, 삽화를 만들어 보관한다, 네이버 비공개 초안을 만든다, 다시 열어 확인한다이다. v01은 작가의 "
        "원고이며 AI가 생성한 초안이 아니다. v02 화면의 '원문을 받아 v01로 보존' 표현도 이 순서로 대체한다."),
}


def v10_html(text):
    """The v10 block as notes HTML. Code blocks stay verbatim; bracketed lines stay text."""
    out, in_list, in_code, code = [], False, False, []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            if in_code:
                out.append("<pre>" + escape("\n".join(code)) + "</pre>")
                code, in_code = [], False
            else:
                if in_list:
                    out.append("</ul>")
                    in_list = False
                in_code = True
            continue
        if in_code:
            code.append(line.rstrip())
            continue
        if s.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{escape(s[2:])}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if not s:
            continue
        m = re.match(r"^([^:]{2,40}):\s(.*)$", s)
        out.append(f"<p><strong>{escape(m.group(1))}:</strong> {escape(m.group(2))}</p>" if m else f"<p>{escape(s)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def v10_scene(sid):
    block = v10notes._block(PLAN.read_text(encoding="utf-8"), sid)
    m = re.search(r"\*\*장면과 질문 \(예시 초안\):\*\*\s*(.+)", block)
    return m.group(1).strip() if m else None


def v10_body(sid):
    return v10notes._plain(v10notes._block(PLAN.read_text(encoding="utf-8"), sid))


def build_notes(n, sl):
    """Notes HTML and Markdown for one slide."""
    mins, start = sl["minutes"], sl["start"]
    ver = kit.VERSION
    head = f"{ver} {n}번. {sl['label']}. {mins}분, {start}분부터 {start + mins}분까지."
    html, md = [f"<h3>{escape(head)}</h3>"], [head, ""]
    if ver >= "v03" and n in CORRECTIONS_V03:
        html.append(f'<p class="fix"><strong>v03 정정 (아래 v10 원문보다 우선):</strong> {escape(CORRECTIONS_V03[n])}</p>')
        md += [f"v03 정정 (아래 v10 원문보다 우선): {CORRECTIONS_V03[n]}", ""]
    if n in CORRECTIONS:
        html.append(f'<p class="fix"><strong>v02 정정 (아래 v10 원문보다 우선):</strong> {escape(CORRECTIONS[n])}</p>')
        md += [f"v02 정정 (아래 v10 원문보다 우선): {CORRECTIONS[n]}", ""]
    if sl["kind"] in ("term", "case", "synthesis"):
        sid = sl["v10"][0]
        sc = v10_scene(sid)
        if sc:
            html.append(f"<p><strong>장면 먼저:</strong> {escape(sc)}</p>")
            md += [f"장면 먼저: {sc}", ""]
    if sl["kind"] == "term":
        flow = ("장면을 20초에서 30초 말하고 예측 질문을 던진다. 답을 들은 뒤 화면의 정의를 읽고, 그림으로 장면에 다시 "
                "적용하고, 헷갈리기 쉬운 점과 확인 질문으로 닫는다.")
        html.append(f"<p><strong>진행:</strong> {escape(flow)}</p>")
        md += [f"진행: {flow}", ""]
        if mins == 2:
            cut = f"v10은 3분 기준이다. {ver}에서는 2분이므로 강사용 보충 예시는 생략하고 확인 질문은 짧게 묻는다."
            html.append(f"<p><strong>시간 조정:</strong> {escape(cut)}</p>")
            md += [f"시간 조정: {cut}", ""]
    if sl.get("notes"):
        html.append(sl["notes"])
        md += [re.sub(r"<[^>]+>", "", re.sub(r"</(p|li|h3)>", "\n", sl["notes"])).strip(), ""]
    for sid in sl.get("v10", []):
        body = v10_body(sid)
        html.append(f"<h3>v10 원문 S{sid} (출처 원본, 수정하지 않음)</h3>")
        html.append(v10_html(body))
        md += [f"[v10 원문 S{sid} (출처 원본, 수정하지 않음)]", body, ""]
    return "\n".join(html), "\n".join(md).rstrip() + "\n"


def build_notes_v04(n, sl):
    """v04 notes: no lecture timing anywhere; v10 blocks as labelled edited excerpts."""
    head = f"{kit.VERSION} {n}번. {sl['label']}"
    html, md = [f"<h3>{escape(head)}</h3>"], [head, ""]
    v06 = kit.VERSION >= "v06"
    o = sl.get("orig")  # original slide number; reference slides added in v07 have none
    fixes = [CORRECTIONS_V03.get(o), CORRECTIONS.get(o), copy_v06.CORRECTIONS.get(o) if v06 else None,
             copy_v10.CORRECTIONS.get(o) if kit.VERSION >= "v10" else None,
             copy_v12.CORRECTIONS.get(o) if kit.VERSION >= "v12" else None,
             copy_v16.CORRECTIONS.get(o) if kit.VERSION >= "v16" else None]
    if kit.VERSION >= "v16":  # corrections that name a physical page follow the v16 numbering
        fixes = [copy_v16.fix_text(f) if f else f for f in fixes]
    for fix in filter(None, fixes):
        html.append(f'<p class="fix"><strong>정정 (아래 v10 발췌보다 우선):</strong> {escape(fix)}</p>')
        md += [f"정정 (아래 v10 발췌보다 우선): {fix}", ""]
    if sl["kind"] in ("term", "case", "synthesis"):
        sc = v10_scene(sl["v10"][0])
        if sc:
            html.append(f"<p><strong>장면 먼저:</strong> {escape(sc)}</p>")
            md += [f"장면 먼저: {sc}", ""]
    if sl["kind"] == "term":
        html.append(f"<p><strong>진행:</strong> {escape(copy_v04.FLOW)}</p>")
        md += [f"진행: {copy_v04.FLOW}", ""]
    if sl.get("notes"):
        html.append(sl["notes"])
        md += [re.sub(r"<[^>]+>", "", re.sub(r"</(p|li|h3)>", "\n", sl["notes"])).strip(), ""]
    for sid in sl.get("v10", []):
        body = copy_v04.excerpt(sid, v10_body(sid))
        label, note = "v04 편집", copy_v04.EXCERPT_NOTE
        if v06:  # v06 also swaps outdated expressions for the current wording
            body, label, note = copy_v06.excerpt_edit(body), "v06 편집", copy_v06.EXCERPT_NOTE
        if kit.VERSION >= "v16":  # drops stale lines about the Grokbot attachment; a correction above says so
            body = copy_v16.excerpt(sid, body)
        html.append(f"<h3>v10 발췌 S{sid} ({label})</h3>")
        html.append(f'<p class="src">{escape(note)}</p>')
        html.append(v10_html(body))
        md += [f"[v10 발췌 S{sid} ({label})]", note, "", body, ""]
    return "\n".join(html), "\n".join(md).rstrip() + "\n"


def slide_html(n, sl, notes, total=42):
    body = sl["body"]
    if kit.VERSION >= "v03":
        body += f'\n  <p class="pageno" aria-label="{n}쪽, 전체 {total}쪽">{n} / {total}</p>'
    attrs = {"id": f"s{n}", "data-physical": n, "data-kind": sl["kind"], "data-label": f"{n}. {sl['label']}"}
    if "minutes" in sl:  # v02 and v03 carry the lecture schedule; v04 has none
        attrs.update({"data-minutes": sl["minutes"], "data-start": sl["start"]})
    attrs["data-layout"] = sl.get("layout", sl["kind"])
    if kit.VERSION >= "v07":  # original (v06) numbering kept for audits; reference slides have a letter instead
        attrs.update({"data-reference": sl["reference"]} if sl.get("reference") else {"data-original": sl["orig"]})
    if sl.get("chapter"):
        attrs["data-chapter"] = sl["chapter"]
    if sl.get("term"):
        attrs["data-term"] = sl["term"]
        attrs["data-term-index"] = sl["term_index"]
    if sl.get("case"):
        attrs["data-case"] = sl["case"]
        attrs["data-case-index"] = sl["case_index"]
    if sl.get("v10"):
        attrs["data-v10"] = " ".join(f"S{s}" for s in sl["v10"])
    a = " ".join(f'{k}="{escape(str(v))}"' for k, v in attrs.items())
    return (f'<!-- ===================================================== {n} {escape(sl["label"])} -->\n'
            f'<section class="slide" {a}>\n<div class="stage"><div class="canvas {sl["theme"]}">\n  {body}\n'
            f'</div></div>\n<aside class="notes">\n{notes}\n</aside>\n</section>')


def validate(slides):
    problems = []
    refs = [s for s in slides if s["kind"] == "reference"]
    want = 45 if kit.VERSION >= "v16" else 44 if kit.VERSION >= "v07" else 42
    if len(slides) != want or len(refs) != want - 42:
        problems.append(f"{len(slides)} slides with {len(refs)} reference slides, expected {want}")
    if all("minutes" in s for s in slides) and sum(s["minutes"] for s in slides) != 120:
        problems.append(f"minutes sum to {sum(s['minutes'] for s in slides)}, expected 120")
    terms = [s for s in slides if s["kind"] == "term"]
    if [s["term"] for s in terms] != V10_TERMS:
        problems.append("terms are not the 25 v10 terms in order")
    if [s["term_index"] for s in terms] != list(range(1, 26)):
        problems.append("term indexes are not 1 to 25")
    cases = [s for s in slides if s["kind"] == "case"]
    if [s["case"] for s in cases] != ["클식이" if kit.VERSION >= "v08" else "OpenClaw", "OMH", "Grokbot", "AI교양", "CEO Agent"]:
        problems.append("cases are not the five cases in order")
    ceo = [s for s in slides if s.get("case") == "CEO Agent"]
    if len(ceo) != 1 or ceo[0].get("minutes", 3) != 3:
        problems.append("CEO Agent must be exactly one slide (three minutes where timed)")
    brk = [s for s in slides if s["kind"] == "break"]
    if len(brk) != 1 or brk[0].get("minutes", 10) != 10:
        problems.append("break must be one slide (ten minutes where timed)")
    if len([s for s in slides if s["kind"] == "chapter"]) != 5:
        problems.append("expected five chapter screens")
    v10_terms = [s["v10"][0] for s in terms]
    for sid, s in zip(v10_terms, terms):
        title = v10notes.heading(ROOT, sid)["title"]
        if title != s["term"]:
            problems.append(f"S{sid} title {title} does not match term {s['term']}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--version", choices=VERSIONS, default=CURRENT)
    ap.add_argument("--out-dir", type=Path, default=SLIDES_DIR)
    args = ap.parse_args()
    ver = kit.VERSION = args.version
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    export = out / f"harness-engineering-workshop-{ver}.html"
    manifest_path = out / f"harness-engineering-workshop-{ver}.manifest.json"
    notes_md = out / f"speaker-notes-{ver}.md"
    index = SLIDES_DIR / "index.html" if (ver == CURRENT and out == SLIDES_DIR.resolve()) else None

    raw = [f() for f in SLIDES_A + SLIDES_B]
    timed = ver < "v04"  # v04 drops the lecture schedule entirely
    start = 0
    for i, sl in enumerate(raw):
        if timed:
            sl["minutes"] = MINUTES[i]
            sl["start"] = start
            start += MINUTES[i]
        else:
            copy_v04.apply(i + 1, sl)
            if ver >= "v05":
                copy_v05.apply(i + 1, sl)
            if ver >= "v06":
                copy_v06.apply(i + 1, sl)
            if ver >= "v07":
                copy_v07.apply(i + 1, sl)
            if ver >= "v08":
                copy_v08.apply(i + 1, sl)
            if ver >= "v09":
                copy_v09.apply(i + 1, sl)
            if ver >= "v10":
                copy_v10.apply(i + 1, sl)
            if ver >= "v12":
                copy_v12.apply(i + 1, sl)
            if ver >= "v13":
                copy_v13.apply(i + 1, sl)
            if ver >= "v14":
                copy_v14.apply(i + 1, sl)
            if ver >= "v15":
                copy_v15.apply(i + 1, sl)
            if ver >= "v16":
                copy_v16.apply(i + 1, sl)
        sl["orig"] = i + 1
    if ver >= "v07":
        raw = copy_v07.insert(raw)
    if ver >= "v10":
        raw = copy_v10.apply_refs(raw)
    if ver >= "v11":
        raw = copy_v11.apply_refs(raw)
    if ver >= "v12":
        raw = copy_v12.apply_refs(raw)
    if ver >= "v16":
        raw = copy_v16.insert(raw)
    if ver >= "v17":
        raw = copy_v17.apply_refs(raw)
    problems = validate(raw)
    if problems:
        raise SystemExit("deck does not add up:\n  " + "\n  ".join(problems))

    sections, md, manifest = [], [], []
    md.append(f"# 하네스 엔지니어링 {ver} 발표자 노트\n\n"
              f"slides/harness-engineering-workshop-{ver}.html의 발표자 노트와 같은 내용이다. 용어와 사례 슬라이드에는 "
              "docs/plans/slide-content-plan-v10.md의 해당 블록 전체가 들어 있다. 42장, 120분.\n" if timed else
              f"# 하네스 엔지니어링 {ver} 발표자 노트\n\n"
              f"slides/harness-engineering-workshop-{ver}.html의 발표자 노트와 같은 내용입니다. {len(raw)}장. 용어와 사례 슬라이드에는 "
              "docs/plans/slide-content-plan-v10.md의 해당 블록을 강의 시간 표기만 뺀 편집 발췌로 넣었습니다.\n")
    for n, sl in enumerate(raw, 1):
        nh, nm = build_notes(n, sl) if timed else build_notes_v04(n, sl)
        sections.append(slide_html(n, sl, nh, len(raw)))
        md.append(f"## {n}. {sl['label']}\n\n{nm}")
        manifest.append({k: v for k, v in {
            "physical": n, "id": f"s{n}", "kind": sl["kind"], "label": sl["label"], "layout": sl.get("layout", sl["kind"]),
            "chapter": sl.get("chapter"), "minutes": sl.get("minutes"), "start": sl.get("start"),
            "end": sl["start"] + sl["minutes"] if timed else None,
            "term": sl.get("term"), "term_index": sl.get("term_index"), "case": sl.get("case"),
            "case_index": sl.get("case_index"), "v10": [f"S{s}" for s in sl.get("v10", [])],
            "original": sl.get("orig") if ver >= "v07" else None,
            "reference": sl.get("reference") if ver >= "v07" else None}.items()
            if v not in (None, [])})

    css = (HERE / "v02.css").read_text(encoding="utf-8")
    if ver >= "v03":
        css += PAGENO_CSS
    if ver >= "v04":
        css += V04_CSS
    if ver >= "v07":
        css += copy_v07.V07_CSS
    js = (HERE / "v02.js").read_text(encoding="utf-8")
    head = {"deck": "harness-engineering-workshop", "version": ver, "slides": len(raw)}
    if timed:
        head["minutes"] = sum(s["minutes"] for s in raw)
    if ver >= "v06":  # published so a reader or the check can follow the excerpt wording
        head["excerpt_edits"] = [list(p) for p in copy_v06.EXCERPT_EDITS]
    man = json.dumps({**head, "items": manifest}, ensure_ascii=False, indent=1)
    for blob in (css, js, man):
        if "</style" in blob or "</script" in blob:
            raise SystemExit("asset contains a closing tag; cannot inline safely")
    html = (HERE / "deck.src.html").read_text(encoding="utf-8")
    if not timed:
        for old, new in copy_v04.SHELL:
            if old not in html:
                raise SystemExit(f"v04 shell text not found: {old[:50]}")
            html = html.replace(old, new)
        html = html.replace("발표 자료 v04.", f"발표 자료 {ver}.")
        if ver >= "v07":
            html = html.replace("42장, 용어 25개와 사례 5개.", f"{len(raw)}장(참고 {len(raw) - 42}장 포함), 용어 25개와 사례 5개.")
    html = (html.replace("{{CSS}}", css).replace("{{JS}}", js).replace("{{MANIFEST}}", man)
            .replace("{{COUNT}}", str(len(raw))).replace("{{SLIDES}}", "\n\n".join(sections)))
    if "{{" in html:
        raise SystemExit("unfilled placeholder left in the page")
    # patterns are assembled so this file does not itself match a plain-text sweep
    for bad, why in ((chr(0xB7), "middle dot"), ("/" + "Users/", "host path"), ("/" + "Volumes/", "host path"),
                     ("claude.ai" + "/code/session", "session link")):
        if bad in html:
            raise SystemExit(f"output contains a {why}")
    if not timed:
        html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    export.write_text(html, encoding="utf-8")
    manifest_path.write_text(man + "\n", encoding="utf-8")
    notes_md.write_text("\n".join(md), encoding="utf-8")
    written = [export, manifest_path, notes_md]
    if index:
        index.write_text(html, encoding="utf-8")
        written.append(index)
    show = lambda q: q.relative_to(ROOT) if q.is_relative_to(ROOT) else q.name  # noqa: E731
    print(f"{ver}: {len(html.encode('utf-8'))} bytes, {len(raw)} slides; wrote "
          + ", ".join(str(show(q)) for q in written))


if __name__ == "__main__":
    main()
