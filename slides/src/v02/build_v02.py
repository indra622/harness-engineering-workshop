"""Build the full v02 deck: 42 slides, 120 minutes, one self-contained HTML file.

Usage (from the project root):
    python3 slides/src/v02/build_v02.py

Writes:
    slides/harness-engineering-workshop-v02.html   canonical single-file export
    slides/index.html                              current entry (same file)
    slides/harness-engineering-workshop-v02.manifest.json
    slides/speaker-notes-v02.md

Slide content lives in deck_a.py and deck_b.py. Term and case notes carry the
full v10 block for that slide. The build stops before writing if the deck no
longer adds up: 42 slides, 120 minutes, 25 distinct terms in v10 order, five
cases, one three-minute CEO Agent slide and a ten-minute break.
Needs only the Python standard library.
"""

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

from deck import notes as v10notes  # noqa: E402
from deck_a import SLIDES_A  # noqa: E402
from deck_b import SLIDES_B  # noqa: E402

SLIDES_DIR = ROOT / "slides"
EXPORT = SLIDES_DIR / "harness-engineering-workshop-v02.html"
INDEX = SLIDES_DIR / "index.html"
MANIFEST = SLIDES_DIR / "harness-engineering-workshop-v02.manifest.json"
NOTES_MD = SLIDES_DIR / "speaker-notes-v02.md"
PLAN = ROOT / v10notes.PLAN

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
    head = f"v02 {n}번. {sl['label']}. {mins}분, {start}분부터 {start + mins}분까지."
    html, md = [f"<h3>{escape(head)}</h3>"], [head, ""]
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
            cut = "v10은 3분 기준이다. v02에서는 2분이므로 강사용 보충 예시는 생략하고 확인 질문은 짧게 묻는다."
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


def slide_html(n, sl, notes):
    attrs = {"id": f"s{n}", "data-physical": n, "data-kind": sl["kind"], "data-label": f"{n}. {sl['label']}",
             "data-minutes": sl["minutes"], "data-start": sl["start"], "data-layout": sl.get("layout", sl["kind"])}
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
            f'<section class="slide" {a}>\n<div class="stage"><div class="canvas {sl["theme"]}">\n  {sl["body"]}\n'
            f'</div></div>\n<aside class="notes">\n{notes}\n</aside>\n</section>')


def validate(slides):
    problems = []
    if len(slides) != 42:
        problems.append(f"{len(slides)} slides, expected 42")
    if sum(s["minutes"] for s in slides) != 120:
        problems.append(f"minutes sum to {sum(s['minutes'] for s in slides)}, expected 120")
    terms = [s for s in slides if s["kind"] == "term"]
    if [s["term"] for s in terms] != V10_TERMS:
        problems.append("terms are not the 25 v10 terms in order")
    if [s["term_index"] for s in terms] != list(range(1, 26)):
        problems.append("term indexes are not 1 to 25")
    cases = [s for s in slides if s["kind"] == "case"]
    if [s["case"] for s in cases] != ["OpenClaw", "OMH", "Grokbot", "AI교양", "CEO Agent"]:
        problems.append("cases are not the five cases in order")
    ceo = [s for s in slides if s.get("case") == "CEO Agent"]
    if len(ceo) != 1 or ceo[0]["minutes"] != 3:
        problems.append("CEO Agent must be exactly one three-minute slide")
    brk = [s for s in slides if s["kind"] == "break"]
    if len(brk) != 1 or brk[0]["minutes"] != 10:
        problems.append("break must be one ten-minute slide")
    if len([s for s in slides if s["kind"] == "chapter"]) != 5:
        problems.append("expected five chapter screens")
    v10_terms = [s["v10"][0] for s in terms]
    for sid, s in zip(v10_terms, terms):
        title = v10notes.heading(ROOT, sid)["title"]
        if title != s["term"]:
            problems.append(f"S{sid} title {title} does not match term {s['term']}")
    return problems


def main():
    raw = [f() for f in SLIDES_A + SLIDES_B]
    start = 0
    for i, sl in enumerate(raw):
        sl["minutes"] = MINUTES[i]
        sl["start"] = start
        start += MINUTES[i]
    problems = validate(raw)
    if problems:
        raise SystemExit("deck does not add up:\n  " + "\n  ".join(problems))

    sections, md, manifest = [], [], []
    md.append("# 하네스 엔지니어링 v02 발표자 노트\n\n"
              "slides/harness-engineering-workshop-v02.html의 발표자 노트와 같은 내용이다. 용어와 사례 슬라이드에는 "
              "docs/plans/slide-content-plan-v10.md의 해당 블록 전체가 들어 있다. 42장, 120분.\n")
    for n, sl in enumerate(raw, 1):
        nh, nm = build_notes(n, sl)
        sections.append(slide_html(n, sl, nh))
        md.append(f"## {n}. {sl['label']}\n\n{nm}")
        manifest.append({k: v for k, v in {
            "physical": n, "id": f"s{n}", "kind": sl["kind"], "label": sl["label"], "layout": sl.get("layout", sl["kind"]),
            "chapter": sl.get("chapter"), "minutes": sl["minutes"], "start": sl["start"], "end": sl["start"] + sl["minutes"],
            "term": sl.get("term"), "term_index": sl.get("term_index"), "case": sl.get("case"),
            "case_index": sl.get("case_index"), "v10": [f"S{s}" for s in sl.get("v10", [])]}.items()
            if v not in (None, [])})

    css = (HERE / "v02.css").read_text(encoding="utf-8")
    js = (HERE / "v02.js").read_text(encoding="utf-8")
    man = json.dumps({"deck": "harness-engineering-workshop", "version": "v02", "slides": len(raw),
                      "minutes": sum(s["minutes"] for s in raw), "items": manifest}, ensure_ascii=False, indent=1)
    for blob in (css, js, man):
        if "</style" in blob or "</script" in blob:
            raise SystemExit("asset contains a closing tag; cannot inline safely")
    html = (HERE / "deck.src.html").read_text(encoding="utf-8")
    html = (html.replace("{{CSS}}", css).replace("{{JS}}", js).replace("{{MANIFEST}}", man)
            .replace("{{COUNT}}", str(len(raw))).replace("{{SLIDES}}", "\n\n".join(sections)))
    if "{{" in html:
        raise SystemExit("unfilled placeholder left in the page")
    # patterns are assembled so this file does not itself match a plain-text sweep
    for bad, why in ((chr(0xB7), "middle dot"), ("/" + "Users/", "host path"), ("/" + "Volumes/", "host path"),
                     ("claude.ai" + "/code/session", "session link")):
        if bad in html:
            raise SystemExit(f"output contains a {why}")
    EXPORT.write_text(html, encoding="utf-8")
    INDEX.write_text(html, encoding="utf-8")
    MANIFEST.write_text(man + "\n", encoding="utf-8")
    NOTES_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {EXPORT.relative_to(ROOT)} ({len(html.encode('utf-8'))} bytes, {len(raw)} slides, "
          f"{sum(s['minutes'] for s in raw)} min), {INDEX.relative_to(ROOT)}, {MANIFEST.relative_to(ROOT)}, "
          f"{NOTES_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
