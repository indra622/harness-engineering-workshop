"""v22: a 26th term, LLM wiki, right after 메모리 (physical 29). Everything else as in v21.

LLM wiki is a normal term slide, not a reference: our way of keeping the
original, curating reusable notes with sources and links, and finding and
reading the relevant notes again in a later task. OKF is explained on the same
slide as the format for recording source and status. The example is a generic
AI교양 workflow, not private notes; the operating basis is described in the
notes ('클식이 지식 정리 운영 방식, 2026-10-22 확인') and OKF cites the pinned
official spec.

Because a term is added, later term ordinals move by one and read 'n / 26';
the cover, roadmap, chapter 3 route and Q&A index name the new term; pages
after 28 move by one and the pointers to them follow (slide 2 notes, Q&A
numbers, the AI교양 correction).
"""

import re

from kit import AMBER, BLUE, BLUE_SOFT, INK, INK2, MUTED, PAPER2, WHITE, Svg, p, scene

TERM = "LLM wiki"
ORIG = "llm-wiki"
OKF_SPEC = ("https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/"
            "ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md")
HEADLINE = "쌓아 둔 기록을, 다음 작업의 재료로"
DEFINITION = "LLM과 함께 지식을 정리하고 연결해, 필요할 때 다시 찾아 쓰는 방식"
STAGES = [
    ("원문 보존", "내가 쓴 AI교양 원고", "참고 자료는 따로 둠"),
    ("정리와 연결", "개념 노트와 출처", "관련 글, 인덱스"),
    ("관련 노트 찾고 읽기", "새 글 주제로 검색", "실제 내용을 읽음"),
    ("다음 글에 재사용", "이전 관점을 가져옴", "근거는 사람이 다시 확인"),
]
LINE_OKF = "LLM wiki는 정리하고 쓰는 방식, OKF(Open Knowledge Format)는 출처와 상태를 적는 형식"
LINE_READ = "저장만으로 기억되는 건 아님. 필요한 노트를 찾아 읽는 단계까지."


def term_svg():
    s = Svg("sllmwiki", 120, 440, 1680, 470,
            "AI교양 예시로 본 LLM wiki 네 단계. 원문 보존: 내가 쓴 원고와 참고 자료를 따로 둔다. 정리와 연결: 개념 노트에 출처와 "
            "관련 글, 인덱스를 단다. 여기까지는 파일로 남긴 위키다. 관련 노트 찾고 읽기: 새 글 주제로 검색해 실제 내용을 읽어 이번 "
            "작업의 컨텍스트로 가져온다. 다음 글에 재사용: 이전 관점을 가져오고 근거는 사람이 다시 확인한다. " + LINE_OKF + ". " + LINE_READ)
    sm = {"size": 24, "weight": 400, "fill": INK2}
    s.text(0, 14, HEADLINE, size=30, weight=800)
    w, gap = 390, 40
    for k, (title, a, b) in enumerate(STAGES):
        x = k * (w + gap)
        read = k == 2
        s.rect(x, 64, w, 170, fill=WHITE, stroke=BLUE if read else INK, sw=3.5 if read else 2.5,
               extra=f' data-stage="{k + 1}"')
        s.lines(x + w / 2, 149, [title, (a, sm), (b, sm)], size=28, weight=800, anchor="middle", lh=1.42)
        s.num(x, 64, k + 1, fill=BLUE if read else INK)
        if k < 3:
            s.arrow([(x + w + 2, 149), (x + w + gap - 6, 149)], color="blue" if k == 1 else "ink")
    # where each half lives: the stored wiki versus what this task actually reads
    s.rect(0, 258, 2 * w + gap, 56, fill=PAPER2, extra=' data-zone="stored"')
    s.text(24, 286, "파일로 남긴 위키 (예: Obsidian)", size=26, weight=800, fill=MUTED)
    s.rect(2 * (w + gap), 258, 2 * w + gap, 56, fill=BLUE_SOFT, extra=' data-zone="context"')
    s.text(2 * (w + gap) + 24, 286, "이번 작업의 컨텍스트로 읽어 옴", size=26, weight=800, fill=BLUE)
    s.text(0, 372, LINE_OKF, size=28, weight=800)
    s.text(0, 424, LINE_READ, size=26, weight=800, fill=AMBER)
    return s.render()


NOTES = f"""<p><strong>정의:</strong> LLM wiki는 LLM과 함께 지식을 정리하고 연결해, 필요할 때 다시 찾아 쓰는 방식입니다. 이 발표에서 우리가 일하는 방식을 부르는 이름이며, 정해진 제품이나 업계 표준을 뜻하지 않습니다.</p>
<p><strong>장면과 예시 (AI교양, 설명용):</strong> 새 세션에서 지난 글의 핵심을 다시 설명해야 하는 일이 있습니다. 대화 전문을 무조건 쌓아 두는 대신, 먼저 내가 쓴 원고와 참고 자료를 원문 그대로 따로 보존합니다. 다시 쓸 개념과 판단은 노트로 정리해 출처와 관련 글, 인덱스를 달아 둡니다. 다음 글을 쓸 때 에이전트가 새 주제로 관련 노트를 검색하고, 실제 내용을 읽어 이번 작업의 컨텍스트에 넣습니다. 그다음 이전 관점을 가져와 쓰되, 근거가 지금도 맞는지는 사람이 다시 확인합니다. 화면의 노트 이름과 내용은 만든 예시이며 실제 개인 노트가 아닙니다. Obsidian은 우리가 쓰는 파일 기반 도구의 예일 뿐 필요 조건이 아닙니다.</p>
<p><strong>헷갈리는 지점, 저장과 읽기:</strong> 폴더에 저장해 둔 위키와, 이번 작업에 실제로 들어간 컨텍스트는 다릅니다. 앞의 메모리처럼, 저장해 둔 노트도 찾아서 읽어야 이번 작업의 근거가 됩니다. 저장만으로 모델이 기억하게 되는 것은 아니고, 모델을 다시 학습시키는 것도 아닙니다.</p>
<p><strong>헷갈리는 지점, LLM wiki와 OKF:</strong> LLM wiki는 정리하고 찾아 쓰는 방식이고, OKF(Open Knowledge Format)는 그 노트에 출처와 상태를 적는 형식입니다. OKF v0.2 명세는 Markdown 본문과 YAML 머리말로 출처, 상태 같은 메타데이터와 링크를 적는 방법을 정합니다. 검색기나 실행 방식, 자동 기억 갱신은 정하지 않습니다. 형식 출처: <a href="{OKF_SPEC}">OKF v0.2 명세 (고정 커밋 ad30107)</a></p>
<p><strong>운영 근거:</strong> '클식이 지식 정리 운영 방식, 2026-10-22 확인'을 일반화한 설명입니다. 원문은 따로 보존하고, 다시 쓸 노트는 AI와 함께 검토하며 출처와 의미 있는 연결, 인덱스를 달아 정리하고, 노트는 버전을 남기고, 사실과 해석과 열린 질문을 나눠 적고, 작업할 때는 실제 파일을 찾아 읽어 컨텍스트로 씁니다. 모든 문서가 자동으로 노트가 되거나 모든 대화가 보관되는 것은 아닙니다. 원문과 경로는 공개하지 않습니다.</p>
<p><strong>말하지 않는 것:</strong> 검색 정확도나 업무 성능을 잰 결과, 빠짐없이 기억한다는 보장, 모두에게 필요하다는 주장은 하지 않습니다.</p>
<p><strong>확인 질문과 모범 답안:</strong> 폴더에 저장만 해 두면 새 세션에서도 자동으로 알고 있을까? 아닙니다. 필요한 노트를 찾아 읽어 이번 작업의 컨텍스트에 넣어야 근거로 쓸 수 있습니다.</p>"""


def term_slide():
    body = "\n  ".join([
        p("kicker tp-kicker", '<span class="dot"></span>3장<span class="gap"></span>용어 16 / 26'),
        p("tp-word", TERM, "h2"),
        p("tp-def", DEFINITION),
        scene("tp-scene", "지난 AI교양 글에서 정리한 개념을 새 글에도 쓰고 싶다.", "저장해 둔 노트, 새 세션이 저절로 떠올릴까?"),
        term_svg(),
    ])
    return dict(kind="term", term=TERM, term_index=16, chapter=3, label=f"용어 16 {TERM}", theme="t-paper",
                body=body, notes=NOTES, layout="sequence", orig=ORIG)


# ---------------------------------------------------------------- chapter 3 route with seven stations

ROUTE = [("프롬프트", "지시와 제약", "term"), ("컨텍스트", "이번 호출의 입력", "term"), ("토큰", "세는 단위", "term"),
         ("컨텍스트 창", "한 호출의 한계", "term"), ("메모리", "저장과 불러오기", "term"),
         ("LLM wiki", "정리해 다시 찾기", "term"), ("사례 AI교양", "작가의 확정", "case")]


def route_svg():
    s = Svg("s19", 0, 700, 1920, 300, "이번 장의 경로: " + ", ".join(r[0].replace("사례 ", "") for r in ROUTE))
    s.line(128, 150, 1792, 150, color="#FFFFFF", sw=3)
    s.parts[-1] = s.parts[-1].replace("/>", ' stroke-opacity="0.45"/>')
    x0, x1 = 230, 1690
    gap = (x1 - x0) / (len(ROUTE) - 1)
    for i, (name, sub, kind) in enumerate(ROUTE):
        x = round(x0 + i * gap)
        if kind == "term":
            s.add(f'<circle cx="{x}" cy="150" r="15" fill="#FFFFFF"/>')
        else:
            s.rect(x - 26, 124, 52, 52, fill="#FFFFFF")
        s.text(x, 96, name, size=36, weight=800, fill="#FFFFFF", anchor="middle")
        s.text(x, 212, sub, size=26, fill="#BFD3FF", anchor="middle")
    return s.render()


# ---------------------------------------------------------------- text edits on existing slides

EDITS = [  # (finder, field, old, new)
    (lambda s: s.get("orig") == 1, "body", "용어 25개와 사례 5개로", "용어 26개와 사례 5개로"),
    (lambda s: s.get("orig") == 1, "notes", "용어 25개를 하나씩", "용어 26개를 하나씩"),
    (lambda s: s.get("orig") == 2, "notes", "AI교양 사례(29번)", "AI교양 사례(30번)"),
    (lambda s: s.get("orig") == 2, "notes", "워크플로우(37번)", "워크플로우(38번)"),
    (lambda s: s.get("orig") == 3, "body", "프롬프트, 컨텍스트, 토큰, 컨텍스트 창, 메모리</p>",
     "프롬프트, 컨텍스트, 토큰, 컨텍스트 창, 메모리, LLM wiki</p>"),
    (lambda s: s.get("orig") == 19, "body", "지시와 입력, 처리 단위와 한계, 저장과 불러오기.",
     "지시와 입력, 처리 단위와 한계, 저장과 불러오기, 다시 찾아 쓰기."),
    (lambda s: s.get("orig") == 19, "notes", "순서: 프롬프트, 컨텍스트, 토큰, 컨텍스트 창, 메모리, 그리고 사례 AI교양.",
     "순서: 프롬프트, 컨텍스트, 토큰, 컨텍스트 창, 메모리, LLM wiki, 그리고 사례 AI교양."),
    (lambda s: s.get("reference") == "A", "notes", "본문(25개 용어와 다섯 사례)", "본문(26개 용어와 다섯 사례)"),
    (lambda s: s.get("reference") == "C", "notes", "본문(25개 용어와 다섯 사례)", "본문(26개 용어와 다섯 사례)"),
]

FIX_PAGES = [("v12부터 이 화면(v20부터 29쪽) 가운데 흐름은", "v12부터 이 화면(v22부터 30쪽) 가운데 흐름은")]
CORRECTIONS = {
    42: "v22부터 용어는 메모리 다음의 LLM wiki를 더해 26개다. 아래 발췌의 '용어 25개'는 이전 구성을 기준으로 한 표현이다.",
}


def fix_text(text):
    for old, new in FIX_PAGES:
        text = text.replace(old, new)
    return text


def _edit(slides, find, field, old, new):
    hit = [s for s in slides if find(s)]
    if len(hit) != 1 or hit[0][field].count(old) != 1:
        raise SystemExit(f"v22: text not found once: {old[:50]}")
    hit[0][field] = hit[0][field].replace(old, new)


def apply(slides):
    for find, field, old, new in EDITS:
        _edit(slides, find, field, old, new)
    ch = [s for s in slides if s.get("orig") == 19]
    body, n = re.subn(r'<svg class="svg".*?</svg>', lambda m: route_svg(), ch[0]["body"], count=1, flags=re.S)
    if n != 1:
        raise SystemExit("v22: chapter 3 route not found")
    ch[0]["body"] = body
    qa = [s for s in slides if s["kind"] == "qa"][0]
    body, k = re.subn(r"<b>(\d+)</b>",
                      lambda m: f"<b>{int(m.group(1)) + 1 if int(m.group(1)) > 28 else m.group(1)}</b>", qa["body"])
    if k != 30:
        raise SystemExit(f"v22: Q&A index expected 30 numbers, found {k}")
    anchor = "<li><b>28</b>메모리</li>"
    if body.count(anchor) != 1:
        raise SystemExit("v22: Q&A 메모리 entry not found")
    qa["body"] = body.replace(anchor, anchor + "<li><b>29</b>LLM wiki</li>")
    i = next(i for i, s in enumerate(slides) if s.get("term") == "메모리")
    slides = slides[:i + 1] + [term_slide()] + slides[i + 1:]
    # later terms move by one; every term now reads 'n / 26'
    for n, sl in enumerate((s for s in slides if s["kind"] == "term"), 1):
        old = f"용어 {sl['term_index']} / 25"
        if sl.get("orig") != ORIG:
            if sl["body"].count(old) != 1:
                raise SystemExit(f"v22: term kicker not found for {sl['term']}")
            sl["body"] = sl["body"].replace(old, f"용어 {n} / 26")
        sl["term_index"] = n
        sl["label"] = f"용어 {n} {sl['term']}"
    return slides
