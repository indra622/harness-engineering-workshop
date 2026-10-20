"""v07: two optional reference slides after the OMH case, everything else as in v06.

The 42 original slides keep their content, their v10 source ids and their
correction ids. Two reference slides (참고 A, 참고 B) are inserted after
original slide 14, so original 15 to 42 become physical 17 to 44. Only
physical page references move: the page numbers, the Q&A index on original
slide 42, and the "N번" pointers in the original slide 2 notes.

The reference slides compare two published skill collections as reference
data, not as workflows this deck runs or installs:
- cursor/plugins pstack 0.15.29, commit 111cf6a16b11cc822782c1585859af4a580a2490
- obra/superpowers 7.0.0, commit b739a8af570e10a95898f2bdf6cec97467fa6c12
They are an edited summary as of 2026-10-21, not an execution log, a benchmark
or a ranking. Full claim-level links are in
docs/references/pstack-superpowers-comparison-v01.md.
"""

import re

from kit import BLUE, BLUE_SOFT, INK, INK2, MUTED, PAPER2, WHITE, Svg, e, p

INSERT_AFTER = 14  # original slide number of the OMH case
SKIP_TO = INSERT_AFTER + 3  # physical number of the first main slide after the references

PSTACK = "https://github.com/cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490/pstack"
SUPER = "https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12"
SOURCES = [
    ("pstack README (cursor/plugins, 0.15.29)", f"{PSTACK}/README.md"),
    ("pstack plugin.json (버전)", f"{PSTACK}/plugin.json"),
    ("pstack 기능(feature) 플레이북", f"{PSTACK}/skills/poteto-mode/playbooks/feature.md"),
    ("pstack Claude Code 어댑터", f"{PSTACK}/docs/harness/claude-code.md"),
    ("Superpowers README (obra/superpowers, 7.0.0)", f"{SUPER}/README.md"),
    ("Superpowers plugin.json (버전)", f"{SUPER}/.claude-plugin/plugin.json"),
    ("Superpowers brainstorming", f"{SUPER}/skills/brainstorming/SKILL.md"),
    ("Superpowers subagent-driven-development", f"{SUPER}/skills/subagent-driven-development/SKILL.md"),
    ("Superpowers test-driven-development", f"{SUPER}/skills/test-driven-development/SKILL.md"),
]
PROVENANCE = ("출처: pstack 0.15.29 (cursor/plugins 111cf6a), Superpowers 7.0.0 (obra/superpowers b739a8a), "
              "2026-10-21 기준 편집 요약")


def physical(orig):
    """Physical slide number in v07 for an original (v06) slide number."""
    return orig if orig <= INSERT_AFTER else orig + 2


def _head(tag, name):
    return "\n  ".join([
        p("kicker case-head", f'<span class="tag-case">{tag}</span>{e(name)}'),
        f'<a class="abs ref-skip" href="#s{SKIP_TO}">본문으로, {SKIP_TO}쪽</a>',
    ])


def _sources_html():
    items = "".join(f'<li><a href="{u}">{e(t)}</a><br><span class="src">{e(u)}</span></li>' for t, u in SOURCES)
    return f"<h3>출처 (고정된 커밋)</h3><ul>{items}</ul>"


# ---------------------------------------------------------------- 참고 A


def ref_a():
    s = Svg("s15", 120, 340, 1680, 600, "같은 가상 개발 요청에 대한 pstack과 Superpowers의 대표 흐름 비교. "
            "pstack: 플레이북 고르기(이 예에서는 기능), 구조 파악과 설계, 범위를 정해 위임, 실제 동작으로 검증. "
            "Superpowers: 의도와 설계 합의, 작은 단위로 계획, 테스트 먼저 구현과 작업별 검토, 브랜치 전체 검토. "
            "둘 다 스킬 묶음이고 둘 다 맡기고 검토할 수 있으며, 차이는 강조점")
    sm = {"size": 24, "weight": 400, "fill": INK2}
    sm_w = {"size": 24, "weight": 400, "fill": WHITE}
    lanes = [
        (40, "pstack", [("작업별 플레이북", sm), ("위임, 실제 동작 검증", sm)], WHITE, INK, INK, [
            ["플레이북 고르기", ("이번엔 기능 플레이북", sm)],
            ["구조 파악, 설계", ("영향 범위, 데이터 구조", sm)],
            ["범위 정해 위임", ("성공 기준, 분할 점검", sm)],
            ["실제 동작으로 검증", ("결과와 근거 대조", sm)],
        ]),
        (230, "Superpowers", [("설계, 계획, 테스트,", sm_w), ("단계마다 검토", sm_w)], BLUE, BLUE, WHITE, [
            ["의도와 설계 합의", ("작업 크기에 맞게", sm)],
            ["작은 단위로 계획", ("파일, 확인 방법까지", sm)],
            ["테스트 먼저 구현", ("명세, 품질 함께 검토", sm)],
            ["브랜치 전체 검토", ("마무리 방식 선택", sm)],
        ]),
    ]
    xs = [340, 680, 1020, 1360]
    for k, x in enumerate(xs):
        s.text(x, 14, f"{k + 1}", size=26, weight=800, fill=MUTED)
    for y, name, sub, fill, stroke, color, steps in lanes:
        s.box(0, y, 300, 150, [name, *sub], size=32, weight=800, fill=fill, stroke=stroke, color=color, lh=1.3)
        s.arrow([(300, y + 75), (334, y + 75)], color="blue" if fill == BLUE else "ink")
        for k, (x, lines) in enumerate(zip(xs, steps)):
            s.box(x, y, 300, 150, lines, size=28, weight=800,
                  fill=BLUE_SOFT if fill == BLUE else WHITE, stroke=BLUE if fill == BLUE else INK, sw=2.5)
            if k < 3:
                s.arrow([(x + 302, y + 75), (xs[k + 1] - 6, y + 75)], color="blue" if fill == BLUE else "ink")
    s.rect(0, 420, 1680, 130, fill=PAPER2)
    s.text(28, 462, "공통점", size=26, weight=800, fill=BLUE)
    s.text(160, 462, "둘 다 다시 쓰는 스킬 묶음, 둘 다 하위 에이전트에 맡기고 검토할 수 있음", size=28, weight=800)
    s.text(160, 508, "이 그림은 먼저 챙기는 것의 차이. 할 수 있는 일의 유무나 성능 순위가 아님. 대표 흐름을 편집한 요약",
           size=24, fill=INK2)
    body = "\n  ".join([
        _head("참고 A", "pstack과 Superpowers"),
        p("qline case-q", "<b>질문</b>같은 기능 추가 요청(가상): CSV 내보내기. 두 스킬 묶음은 무엇을 먼저 챙길까?"),
        p("case-title", "같은 개발 요청, 서로 다른 작업 설계", "h2"),
        s.render(),
        p("foot", e(PROVENANCE), style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    notes = f"""<p><strong>이 화면의 위치:</strong> 본문(25개 용어와 다섯 사례)에 들지 않는 참고 화면입니다. 필요하면 오른쪽 위 '본문으로'를 눌러 {SKIP_TO}쪽으로 건너뜁니다.</p>
<p><strong>읽는 법:</strong> 같은 가상 요청(CSV 내보내기 기능 추가)을 두 스킬 묶음이 어떤 순서로 다루는지, 각자의 대표 흐름을 편집해 나란히 놓았습니다. 실제 실행 기록이 아니며, 속도나 품질을 잰 결과도 아닙니다.</p>
<p><strong>pstack 줄:</strong> poteto-mode가 요청을 보고 플레이북(README 기준 23개, 기능, 버그 수정, 조사 등)을 고릅니다. 2단계부터는 이 예처럼 기능 플레이북을 고른 경우이며, 플레이북마다 단계는 다릅니다. 기능 플레이북은 영향 범위를 파악하고 설계를 탐색한 뒤, 먼저 끝내야 할 단계, 서로 독립인 작업, 공유 상태, 가장 작은 안전한 분할을 점검하고, 파일 범위와 데이터 구조, 성공 기준을 정해 구현을 하위 에이전트에 맡깁니다. 그다음 실제 동작으로 검증합니다. 코드, 테스트, 실행 결과를 근거와 대조하는 것이며, 화면 캡처만 보는 것이 아닙니다. 순서 없이 자동으로 병렬 분산하는 흐름이 아니며, 한 기능처럼 코드가 엮인 일은 한 담당자에게 둡니다.</p>
<p><strong>Superpowers 줄:</strong> brainstorming이 먼저 의도를 끌어내고 이해한 내용을 되짚습니다. 작은 변경은 대화로, 큰 작업은 설계 문서로 합의합니다(작업 크기에 맞게). 이어서 작은 단위의 계획을 쓰고, 계획을 실행할 때는 작업마다 새 하위 에이전트가 테스트 먼저(RED, GREEN, REFACTOR) 구현하고 작업별 검토 한 번이 명세 충족과 코드 품질을 함께 봅니다. 마지막에 브랜치 전체를 검토하고 마무리 방식을 고릅니다. 하위 에이전트 대신 한 세션에서 계획을 그대로 실행하고 마지막에 한 번 검토하는 방식(executing-plans)도 있습니다.</p>
<p><strong>공통점과 차이:</strong> 둘 다 다시 쓰는 스킬 묶음이고, 둘 다 하위 에이전트에 맡기고 검토할 수 있습니다. pstack은 작업에 맞는 플레이북과 위임 범위, 실제 동작으로 하는 검증을 앞에 두고, Superpowers는 설계 합의, 계획, 테스트 먼저, 단계마다 검토를 앞에 둡니다. 한쪽은 빠르고 한쪽은 꼼꼼하다는 식의 구분이나, 병렬과 직렬의 이분법으로 말하지 않습니다. 에이전트 수도 고정돼 있지 않습니다.</p>
<p><strong>실행 환경:</strong> pstack은 Cursor 이름으로 쓰여 있고 Claude Code용 어댑터가 이름을 바꿔 대응하며, Cursor 전용 기능은 건너뜁니다. 그래서 호스트마다 똑같이 동작한다고 말하지 않습니다. Superpowers도 Claude Code만이 아니라 여러 코딩 에이전트에 설치 경로를 안내합니다.</p>
<p><strong>표기 주의:</strong> Superpowers README의 스킬 목록에는 '두 단계 검토'라는 표현이 남아 있지만, 같은 커밋의 subagent-driven-development 스킬 본문은 작업별 검토 한 번이 명세와 품질을 함께 본다고 설명합니다. 이 화면은 스킬 본문을 따랐습니다.</p>
{_sources_html()}"""
    return dict(kind="reference", reference="A", label="참고 A: 같은 개발 요청, 서로 다른 작업 설계",
                theme="t-paper", body=body, notes=notes, chapter=2, layout="reference")


# ---------------------------------------------------------------- 참고 B


def ref_b():
    s = Svg("s16", 120, 340, 1680, 600, "pstack과 Superpowers에서 눈여겨볼 작업 방식과 내 환경의 조건이 "
            "'내 환경에서 쓸 절차와 도구 선택'으로 모이고, OMH의 경우 설정된 모델과 OpenCode, OMO 역할을 그대로 두고 "
            "업무 도구와 omh-rigorous를 더한다. Superpowers는 비교용 참고이고, 오른쪽은 이런 선택을 OMH에 적용한 예")
    sm = {"size": 24, "weight": 400, "fill": INK2}
    s.box(0, 0, 520, 172, ["pstack에서 눈여겨볼 것", ("작업에 맞는 플레이북", sm), ("범위와 성공 기준을 정한 위임", sm),
                           ("실제 동작으로 검증", sm)], size=28, weight=800, lh=1.32)
    s.box(0, 196, 520, 172, ["Superpowers (비교 참고)", ("작업 크기에 맞춘 설계 합의", sm),
                             ("작은 단위 계획, 테스트 먼저", sm), ("단계마다 검토", sm)], size=28, weight=800, lh=1.32)
    s.box(0, 392, 520, 84, ["내 환경의 조건", ("호스트 도구, 설정된 모델, 오프라인", sm)], size=28, weight=800,
          stroke=MUTED, dash="9 7", lh=1.3)
    s.box(620, 130, 440, 200, ["내 환경에서 쓸", "절차와 도구 선택", ("그대로 옮기지 않고 골라서 맞춤", {"size": 24,
                                                                                     "weight": 400, "fill": WHITE})],
          size=32, weight=800, fill=BLUE, stroke=BLUE, color=WHITE, lh=1.4)
    s.arrow([(520, 86), (570, 86), (570, 180), (614, 180)])
    s.arrow([(520, 282), (570, 282), (570, 270), (614, 270)])
    s.arrow([(520, 434), (590, 434), (590, 310), (614, 310)], color="muted", dash="9 7")
    s.arrow([(1060, 230), (1154, 230)], color="blue")
    s.rect(1160, 0, 520, 470, fill=WHITE, stroke=INK, sw=2.5)
    s.text(1190, 40, "적용 예: OMH", size=30, weight=800)
    rows = [(110, "그대로", "설정된 모델 하나", False), (150, "", "OpenCode와 OMO 역할", False),
            (215, "더함", "data_inspect", True), (253, "", "data_compare", True),
            (318, "골라 씀", "omh-rigorous", True)]
    for y, lab, val, mono in rows:
        if lab:
            s.text(1190, y, lab, size=24, weight=800, fill=MUTED)
        s.text(1310, y, val, size=26, weight=700, fill=BLUE if mono else INK, mono=mono)
    s.line(1190, 362, 1650, 362, color=PAPER2, sw=2)
    s.text(1190, 396, "필요한 절차를 골라", size=24, fill=INK2)
    s.text(1190, 432, "업무 환경에 맞춤", size=24, fill=INK2)
    s.rect(0, 500, 1680, 60, fill=BLUE_SOFT)
    s.text(24, 530, "정리", size=26, weight=800, fill=BLUE)
    s.text(110, 530, "OMH는 모델을 유지하고, 절차와 확인 도구를 업무에 맞게", size=28, weight=800)
    body = "\n  ".join([
        _head("참고 B", "pstack과 Superpowers"),
        p("qline case-q", "<b>질문</b>다른 팀의 스킬 묶음에서 무엇을 가져와야 할까?"),
        p("case-title", "가져올 것은 기능 목록보다 작업 방식", "h2"),
        s.render(),
        p("foot", e(PROVENANCE), style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    notes = f"""<p><strong>이 화면의 위치:</strong> 참고 A에 이어지는 참고 화면입니다. 오른쪽 위 '본문으로'를 누르면 {SKIP_TO}쪽(플러그인)으로 갑니다.</p>
<p><strong>읽는 법:</strong> 왼쪽은 두 스킬 묶음에서 눈여겨볼 작업 방식, 아래는 내 환경의 조건입니다. 셋이 가운데 '내 환경에서 쓸 절차와 도구 선택'으로 모입니다. 스킬 묶음을 통째로 설치해 그대로 따르기보다, 작업 방식을 보고 내 도구와 모델, 제약에 맞게 골라 쓰자는 교육용 정리입니다.</p>
<p><strong>OMH와의 연결:</strong> 적용 예로 든 OMH는 설정된 모델 하나와 OpenCode, OMO의 기존 역할을 그대로 두고, 업무 도구(data_inspect, data_compare)와 필요할 때 골라 쓰는 절차(omh-rigorous)를 더했습니다(14쪽). v10 기획(S11)에는 omh-rigorous가 pstack에서 버그 수정, 기능 구현, 근거 기반 조사 절차를 골라 적응시킨 것이라고 적혀 있습니다. 이 화면의 pstack 연결은 그 기록에만 근거합니다. 어느 pstack 버전에서 가져왔는지는 이 저장소에 기록이 없어, 참고 A가 인용한 0.15.29와 같다고 말하지 않습니다.</p>
<p><strong>Superpowers의 자리:</strong> Superpowers는 여기서 비교용 참고이며, OMH 구현의 근거로 제시하지 않습니다. 가운데 상자에서 오른쪽으로 가는 선은 '이렇게 골라 적용한다'는 설계 선택의 예이지, OMH가 실제로 어디서 무엇을 가져왔는지를 보여 주는 계보가 아닙니다.</p>
<p><strong>화면에 쓰지 않은 단서:</strong> 이 화면은 교육용 정리입니다. 어느 쪽이 더 낫다는 점수, 벤치마크, 모든 환경에서 그대로 동작한다는 호환성 주장은 하지 않습니다. 설치 방법도 안내하지 않습니다. 두 묶음 모두 설치 경로가 호스트마다 다르고, pstack은 Cursor 전용 단계를 다른 호스트에서 건너뜁니다.</p>
{_sources_html()}"""
    return dict(kind="reference", reference="B", label="참고 B: 가져올 것은 기능 목록보다 작업 방식",
                theme="t-paper", body=body, notes=notes, chapter=2, layout="reference")


V07_CSS = """
/* v07: optional reference slides */
.ref-skip { right: 120px; top: 96px; font-size: 26px; font-weight: 700; color: var(--blue); text-decoration: none;
  border-bottom: 2px solid var(--blue); padding-bottom: 2px; }
.ref-skip:focus-visible { outline: 3px solid var(--blue); outline-offset: 4px; }
.notes-body .src { color: var(--muted); font-size: 13px; word-break: break-all; }
"""


# ---------------------------------------------------------------- physical references in the original slides


def apply(orig, sl):
    """Move physical page pointers in an original slide to their v07 numbers."""
    if orig == 2:
        for a, b in (("AI교양 사례(25번)", f"AI교양 사례({physical(25)}번)"), ("워크플로우(33번)", f"워크플로우({physical(33)}번)")):
            if a not in sl["notes"]:
                raise SystemExit(f"v07: slide 2 note pointer not found: {a}")
            sl["notes"] = sl["notes"].replace(a, b)
    if orig == 42:
        body, k = re.subn(r"<b>(\d+)</b>", lambda m: f"<b>{physical(int(m.group(1)))}</b>", sl["body"])
        if k != 30:
            raise SystemExit(f"v07: Q&A index expected 30 numbers, found {k}")
        sl["body"] = body


def insert(slides):
    """The two reference slides go right after the OMH case."""
    k = next(i for i, sl in enumerate(slides) if sl.get("orig") == INSERT_AFTER)
    return slides[:k + 1] + [ref_a(), ref_b()] + slides[k + 1:]
