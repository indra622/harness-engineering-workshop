"""v20: a case follow-up after the OMH case (physical 15). Everything else as in v19, with page pointers moved.

The new page tells the author's own migration in three stages: OMH v05, built
over several days on OpenCode + OMO; moving to OMP (Oh My Pi), whose base
already provides file editing, command execution and task subagents; OMH v06,
a thin own layer (omh-rigorous, the procedure this work needs) on that base.
The author's experience (stated 2026-10-21) is the source for v05, v06 and the
outcome; the OMP README is the source only for its general built-ins. It does
not claim that OMP has the OMH data tools, measured sizes or performance.

The page is kind 'case-detail' with original id 'omh-evolution': not a sixth
case, not a fourth reference. Pages after 14 move by one; the page pointers
that name them follow (slide 2 notes, reference skip links and notes, the Q&A
index and the AI교양 correction). Source ids and data values are left alone.
"""

import re

from kit import AMBER, BLUE, BLUE_SOFT, INK, INK2, MUTED, PAPER2, WHITE, Svg, e, p

ORIG = "omh-evolution"
OMP_README = "https://github.com/can1357/oh-my-pi/blob/57b56631ee009098a78d9badf91afc3a48eef32e/README.md"

STAGES = [
    ("v05", "OMH v05", "OpenCode + OMO 위에 며칠 동안 쌓음"),
    ("omp", "OMP(Oh My Pi)로 옮김", "실행, 도구, 하위 에이전트가 기본"),
    ("v06", "OMH v06", "기본 위에 얇은 절차 한 겹"),
]


def svg():
    s = Svg("s14b", 120, 340, 1680, 600,
            "작성자의 전환 경험 세 단계. OMH v05: OpenCode와 OMO 위에 역할 조율, 실행과 도구 연결, 업무 도구, omh-rigorous 절차를 며칠 동안 "
            "직접 덧붙였다. OMP로 옮기니 파일 편집, 명령 실행, 하위 에이전트 작업이 기본 기능이라 상당 부분은 직접 덧붙일 필요가 없어졌다. "
            "OMH v06은 OMP 기본 기능 위에 omh-rigorous, 내 업무에 필요한 절차만 얇게 둔다. 하네스가 사라진 것이 아니라 직접 덧붙인 부분이 줄었다")
    sm = {"size": 24, "weight": 400, "fill": INK2}
    w, xs = 480, [0, 600, 1200]
    for (key, name, sub), x in zip(STAGES, xs):
        s.text(x, 16, name, size=30, weight=800, fill=BLUE if key == "v06" else INK)
        s.text(x, 52, sub, size=24, fill=INK2)
    # 1 OMH v05: a tall own layer on OpenCode + OMO
    x = xs[0]
    s.rect(x, 84, w, 256, fill=BLUE_SOFT, stroke=BLUE, sw=3, extra=' data-stage="v05" data-layer="own"')
    s.lines(x + w / 2, 212, ["직접 덧붙인 부분", ("역할 조율", sm), ("실행과 도구 연결", sm), ("업무 도구", sm),
                             ("omh-rigorous 절차", sm)], size=28, weight=800, anchor="middle", lh=1.4)
    s.rect(x, 352, w, 88, fill=PAPER2, stroke=INK, sw=2.5, extra=' data-stage="v05" data-layer="base"')
    s.text(x + w / 2, 396, "OpenCode + OMO", size=28, weight=800, anchor="middle")
    # 2 OMP: what was added by hand is now in the base
    x = xs[1]
    s.rect(x, 84, w, 76, fill="none", stroke=MUTED, sw=2.5, dash="9 7", extra=' data-stage="omp" data-layer="own"')
    s.text(x + w / 2, 122, "직접 덧붙일 필요가 없어짐", size=26, weight=800, fill=MUTED, anchor="middle")
    s.arrow([(x + w / 2, 162), (x + w / 2, 196)], color="muted")
    s.rect(x, 200, w, 240, fill=WHITE, stroke=INK, sw=2.5, extra=' data-stage="omp" data-layer="base"')
    s.lines(x + w / 2, 320, ["OMP 기본 기능", ("파일 읽기, 쓰기, 편집", sm), ("명령 실행", sm), ("하위 에이전트 작업", sm)],
            size=28, weight=800, anchor="middle", lh=1.45)
    # 3 OMH v06: a thin own strip on a large base
    x = xs[2]
    s.rect(x, 84, w, 52, fill=BLUE, stroke=BLUE, sw=3, extra=' data-stage="v06" data-layer="own"')
    s.text(x + w / 2, 110, "omh-rigorous, 내 업무 절차", size=26, weight=800, fill=WHITE, anchor="middle")
    s.rect(x, 148, w, 292, fill=WHITE, stroke=INK, sw=2.5, extra=' data-stage="v06" data-layer="base"')
    s.text(x + w / 2, 294, "OMP 기본 기능", size=28, weight=800, anchor="middle")
    for k, label in enumerate(["옮겨 보니", "다시 정리"]):
        x1 = xs[k] + w + 4
        s.arrow([(x1, 270), (xs[k + 1] - 8, 270)], color="ink")
        s.text((x1 + xs[k + 1]) / 2, 240, label, size=24, weight=800, fill=INK2, anchor="middle")
    s.rect(0, 480, 1680, 110, fill=PAPER2)
    s.text(28, 516, "작성자 경험", size=26, weight=800, fill=AMBER)
    s.text(220, 516, "며칠 동안 v05까지 만들었는데, 상당 부분은 이미 기본 기능이었음", size=28, weight=800)
    s.text(220, 560, "v06에는 필요한 절차만 얇게. 하네스가 사라진 게 아니라 내가 덧붙일 부분이 줄어듦", size=24, fill=INK2)
    return s.render()


NOTES = f"""<p><strong>이 화면의 자리:</strong> 14쪽 OMH 사례에 이어지는 한 장입니다. 여섯 번째 사례나 참고 화면이 아니라, 같은 사례를 만든 작성자가 그 뒤에 겪은 일입니다.</p>
<p><strong>작성자의 전환 경험 (2026-10-21 작성자 진술):</strong> OpenCode와 OMO 위에 며칠 동안 하네스를 덧붙여 OMH v05까지 만들었습니다. 그 뒤 OMP(Oh My Pi)로 옮겨 보니, 직접 덧붙였던 것 중 상당 부분이 이미 기본으로 들어 있었고, 따로 남길 만한 것은 omh-rigorous 절차 정도였습니다. 며칠 들인 작업이 허무하게 느껴졌고, 그래서 v06은 v05보다 훨씬 얇게, 내 업무에 필요한 절차만 남기는 쪽으로 정리할 수 있었습니다. 이 단계와 결과는 작성자의 경험이며, v05와 v06 패키지를 따로 열어 코드나 테스트로 대조한 기록은 아닙니다.</p>
<p><strong>공식 문서로 확인한 일반 기능:</strong> OMP 공식 README(2026-10-21 확인, 커밋 57b5663 기준)는 파일을 읽고 쓰고 고치는 기본 도구, 명령 실행, 하위 에이전트에 작업을 맡기고 조율하는 기능을 설명합니다. 이 화면의 'OMP 기본 기능' 세 줄은 이 일반 기능만 가리키며, 작성자가 설치한 버전과 같다는 뜻은 아닙니다. OMH의 data_inspect, data_compare 같은 업무 도구가 OMP에 같은 방식으로 들어 있다거나 그대로 대체된다고 말하지 않습니다. 출처: <a href="{OMP_README}">{e(OMP_README)}</a></p>
<p><strong>읽는 법:</strong> 하네스가 필요 없어졌다는 이야기가 아닙니다. 바탕이 되는 도구가 많은 것을 기본으로 갖추면, 내가 직접 덧붙일 부분은 얇아질 수 있다는 이야기입니다. 크기 비교, 코드 줄 수, 성능 측정은 하지 않았습니다.</p>
<p><strong>맺음말과의 연결:</strong> 마지막 쪽의 '공부할수록, 오히려 확신이 줄었어요'는 이 경험에서 나온 말입니다. 어디까지 직접 구조를 더해야 하는지는 여기서도 답을 내리지 않습니다.</p>
<h3>출처</h3><ul><li><a href="{OMP_README}">oh-my-pi README (can1357/oh-my-pi, 57b5663)</a><br><span class="src">{e(OMP_README)}</span></li></ul>"""


def detail():
    body = "\n  ".join([
        p("kicker case-head", f'<span class="tag-case">사례 2 이어서</span>{e("OMH에서 OMP로")}'),
        p("qline case-q", "<b>질문</b>직접 덧붙인 하네스, 바탕이 바뀌면 얼마나 남을까?"),
        p("case-title", "며칠을 만들었는데, 옮겨 보니 이미 있었다", "h2"),
        svg(),
    ])
    return dict(kind="case-detail", label="사례 2 이어서: OMH에서 OMP로", theme="t-paper", body=body, notes=NOTES,
                chapter=2, layout="case", orig=ORIG)


# ---------------------------------------------------------------- page pointers that move by one

# (slide finder, field, old, new): each must match exactly once
POINTERS = [
    (lambda s: s.get("orig") == 2, "notes", "AI교양 사례(28번)", "AI교양 사례(29번)"),
    (lambda s: s.get("orig") == 2, "notes", "워크플로우(36번)", "워크플로우(37번)"),
    (lambda s: s.get("reference") == "A", "body", '<a class="abs ref-skip" href="#s17">본문으로, 17쪽</a>',
     '<a class="abs ref-skip" href="#s18">본문으로, 18쪽</a>'),
    (lambda s: s.get("reference") == "A", "notes", "'본문으로'를 눌러 17쪽으로", "'본문으로'를 눌러 18쪽으로"),
    (lambda s: s.get("reference") == "B", "body", '<a class="abs ref-skip" href="#s17">본문으로, 17쪽</a>',
     '<a class="abs ref-skip" href="#s18">본문으로, 18쪽</a>'),
    (lambda s: s.get("reference") == "B", "notes", "'본문으로'를 누르면 17쪽(플러그인)으로", "'본문으로'를 누르면 18쪽(플러그인)으로"),
    (lambda s: s.get("reference") == "B", "notes", "15쪽처럼 Superpowers는", "16쪽처럼 Superpowers는"),
    (lambda s: s.get("reference") == "C", "body", '<a class="abs ref-skip" href="#s22">본문으로, 22쪽</a>',
     '<a class="abs ref-skip" href="#s23">본문으로, 23쪽</a>'),
    (lambda s: s.get("reference") == "C", "notes", "'본문으로'를 눌러 22쪽으로", "'본문으로'를 눌러 23쪽으로"),
]

FIX_PAGES = [("v12부터 이 화면(v16부터 28쪽) 가운데 흐름은", "v12부터 이 화면(v20부터 29쪽) 가운데 흐름은")]


def fix_text(text):
    for old, new in FIX_PAGES:
        text = text.replace(old, new)
    return text


def apply(slides):
    """Insert the follow-up after the OMH case and move the page pointers."""
    for find, field, old, new in POINTERS:
        hit = [s for s in slides if find(s)]
        if len(hit) != 1 or hit[0][field].count(old) != 1:
            raise SystemExit(f"v20: pointer not found once: {old[:50]}")
        hit[0][field] = hit[0][field].replace(old, new)
    qa = [s for s in slides if s["kind"] == "qa"]
    body, k = re.subn(r"<b>(\d+)</b>",
                      lambda m: f"<b>{int(m.group(1)) + 1 if int(m.group(1)) > 14 else m.group(1)}</b>", qa[0]["body"])
    if len(qa) != 1 or k != 30:
        raise SystemExit(f"v20: Q&A index expected 30 numbers, found {k}")
    qa[0]["body"] = body
    i = next(i for i, s in enumerate(slides) if s.get("orig") == 14)
    return slides[:i + 1] + [detail()] + slides[i + 1:]
