"""v11: slide 15 reframed as an emphasis shift, slide 16 kept in step. Everything else as in v10.

- Slide 15 (참고 A): no AS-IS/TO-BE labels and no migration arrow. Two stacked
  layers: execution habits (plan, implement, test, iterate), which Superpowers
  packages as well-made, maintained procedures and which models increasingly
  carry by default; above them a job-specific operating layer (success criteria
  and evidence, task-specific procedure selection, bounded delegation,
  returned-result verification), the emphasis this presenter takes from pstack.
  Both bundles overlap; this is an emphasis, not a ranking or a partition.
- Fact and interpretation stay apart in the notes and in
  docs/references/pstack-superpowers-comparison-v03.md: coding agents are
  trained on agentic coding with test loops, including by reinforcement
  learning (fact, historical Codex source); that value therefore shifts to
  tailored verification and delegation is this presenter's thesis.
- Slide 16 (참고 B): the two left labels lose AS-IS/TO-BE; the dashed
  Superpowers line and the OMH 같음/포함 rows stay.
"""

from kit import BLUE, BLUE_SOFT, INK, INK2, MUTED, PAPER2, WHITE, Svg, e, p

import copy_v07

SUPER_RELEASE = ("Superpowers RELEASE-NOTES (7.0.0까지의 변경 기록)",
                 "https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/RELEASE-NOTES.md")
BACKGROUND = [
    ("OpenAI, Introducing Codex (2025-05-16, 학습 방식에 관한 역사적 기록)", "https://openai.com/index/introducing-codex/"),
    ("OpenAI, Harness engineering", "https://openai.com/index/harness-engineering/"),
]


def _sources_html():
    pinned = "".join(f'<li><a href="{u}">{e(t)}</a><br><span class="src">{e(u)}</span></li>'
                     for t, u in copy_v07.SOURCES + [SUPER_RELEASE])
    bg = "".join(f'<li><a href="{u}">{e(t)}</a><br><span class="src">{e(u)}</span></li>' for t, u in BACKGROUND)
    return (f"<h3>출처 (고정된 커밋)</h3><ul>{pinned}</ul>"
            f"<h3>방향 해석의 배경 (2026-10-21 확인)</h3><ul>{bg}</ul>")


# ---------------------------------------------------------------- slide 15: 기본기 다음은, 검증과 위임


def ref_a():
    s = Svg("s15", 120, 330, 1680, 620, "두 층으로 본 강조점. 아래 층은 계획, 구현, 테스트, 반복 수정 같은 실행 기본기로, "
            "Superpowers가 잘 만든 기본 절차로 다듬어 왔고 모델에도 스며들고 있다. 위 층은 업무 운영 층으로, 성공 기준과 근거, "
            "작업별 절차 선택, 범위 정한 위임, 돌아온 결과 검증이며 pstack에서 참고할 강조점이다. 두 묶음은 계획, 위임, 검토, "
            "테스트를 함께 갖추며, 이 그림은 순위가 아니라 발표자의 강조점이다")
    sm = {"size": 24, "weight": 400, "fill": INK2}
    xs = [340, 680, 1020, 1360]
    # upper layer: the job-specific operating layer, drawn with more weight
    s.box(0, 0, 300, 200, [("다음 초점", {"size": 24, "weight": 800, "fill": WHITE}), "업무 운영 층",
                           ("pstack에서 참고", {"size": 24, "weight": 400, "fill": WHITE})],
          size=32, weight=800, fill=BLUE, stroke=BLUE, color=WHITE, lh=1.35)
    upper = [["성공 기준과 근거", ("완료 기준을 먼저 정함", sm)], ["작업별 절차 선택", ("일에 맞는 플레이북", sm)],
             ["범위 정한 위임", ("파일 범위와 완료 조건", sm)], ["돌아온 결과 검증", ("실제 동작과 근거 대조", sm)]]
    for k, (x, lines) in enumerate(zip(xs, upper)):
        s.box(x, 15, 300, 170, lines, size=28, weight=800, fill=BLUE_SOFT, stroke=BLUE, sw=3, lh=1.4)
        if k < 3:
            s.arrow([(x + 302, 100), (xs[k + 1] - 6, 100)], color="blue")
    # lower layer: execution habits, the foundation the upper layer stands on
    s.line(0, 222, 1680, 222, color=PAPER2, sw=2)
    s.box(0, 244, 300, 190, [("실행 기본기", {"size": 24, "weight": 800, "fill": MUTED}), "Superpowers",
                             ("잘 만든 기본 절차,", sm), ("계속 다듬어지는 습관", sm)],
          size=32, weight=800, fill=PAPER2, stroke=INK, lh=1.3)
    lower = [["계획", ("작은 단위로 나눔", sm)], ["구현", ("명세에 맞춰 작성", sm)],
             ["테스트", ("통과할 때까지 확인", sm)], ["반복 수정", ("검토 받고 고침", sm)]]
    for k, (x, lines) in enumerate(zip(xs, lower)):
        s.box(x, 264, 300, 150, lines, size=28, weight=800, fill=WHITE, stroke=INK, sw=2.5, lh=1.4)
        if k < 3:
            s.arrow([(x + 302, 339), (xs[k + 1] - 6, 339)])
    s.rect(0, 470, 1680, 130, fill=PAPER2)
    s.text(28, 512, "강조점", size=26, weight=800, fill=BLUE)
    s.text(160, 512, "기본기는 모델에, 업무 기준과 위임은 하네스에", size=30, weight=800)
    s.text(160, 558, "계획하고 시험하는 기본기는 모델에 스며들고, 두 묶음 모두 계획, 위임, 검토, 테스트를 갖춤", size=24,
           fill=INK2)
    body = "\n  ".join([
        copy_v07._head("참고 A", "Superpowers와 pstack"),
        p("qline case-q", "<b>질문</b>계획하고 테스트하는 습관이 기본이 되면, 하네스는 무엇을 더 챙겨야 할까?"),
        p("case-title", "기본기 다음은, 검증과 위임", "h2"),
        s.render(),
        p("foot", e(copy_v07.PROVENANCE), style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    notes = f"""<p><strong>이 화면의 위치:</strong> 본문(25개 용어와 다섯 사례)에 들지 않는 참고 화면입니다. 필요하면 오른쪽 위 '본문으로'를 눌러 {copy_v07.SKIP_TO}쪽으로 건너뜁니다.</p>
<p><strong>전달 의도:</strong> Superpowers는 잘 만든 절차 모음이고 지금도 꾸준히 다듬어지고 있습니다. 낡았거나 필요 없다는 이야기가 아닙니다. 다만 계획하고, 구현하고, 테스트하고, 고쳐 가는 실행 기본기는 점점 모델이 스스로 해내는 방향으로 가고 있습니다. 그래서 이 발표는 하네스의 다음 초점을 그 위의 층, 곧 이 일에 맞는 성공 기준과 근거, 작업에 맞는 절차 선택, 범위를 정한 위임, 돌아온 결과의 검증에 둡니다. pstack은 이 층을 앞에 두는 예로 참고합니다. 어느 쪽이 더 낫다는 점수나 제품 순위가 아닙니다.</p>
<p><strong>사실과 해석:</strong> 사실로 말할 수 있는 것은 이렇습니다. OpenAI는 2025년 5월 Codex를 소개하며, codex-1이 실제 코딩 작업에 대한 강화학습으로 훈련됐고 테스트를 반복 실행해 통과할 때까지 고치도록 학습됐다고 밝혔습니다(당시 기록이며, 제품의 다른 세부는 그 뒤 바뀌었을 수 있습니다). 같은 회사의 Harness engineering 글은 에이전트가 일하는 환경을 설계하고, 의도를 전하고, 되먹임 고리와 강제할 수 있는 검증을 갖추는 일을 다룹니다. Superpowers의 변경 기록(RELEASE-NOTES)은 절차와 검토 방식이 계속 고쳐지고 있음을 보여 줍니다. 그 위의 해석, 곧 '이런 습관이 기본이 될수록 하네스의 가치는 일에 맞춘 검증과 위임으로 옮겨 간다'는 것은 이 발표의 관점입니다. 모든 모델이 Superpowers 문서 자체를 학습했다거나, 모델이 늘 절차를 빠짐없이 따른다거나, 추가 지시가 더는 쓸모없다는 뜻이 아닙니다.</p>
<p><strong>아래 층, 실행 기본기:</strong> Superpowers에서는 brainstorming이 먼저 의도를 끌어내고 이해한 내용을 되짚습니다. 작은 변경은 대화로, 큰 작업은 설계 문서로 합의합니다. 이어서 작은 단위의 계획을 쓰고, 실행할 때는 작업마다 새 하위 에이전트가 테스트 먼저(RED, GREEN, REFACTOR) 구현하고 작업별 검토 한 번이 명세 충족과 코드 품질을 함께 봅니다. 마지막에 브랜치 전체를 검토하고 마무리 방식을 고릅니다. 하위 에이전트 대신 한 세션에서 실행하고 마지막에 한 번 검토하는 방식(executing-plans)도 있습니다. 위임과 검토도 이미 갖추고 있다는 뜻입니다.</p>
<p><strong>위 층, 업무 운영:</strong> pstack에서는 poteto-mode가 요청을 보고 작업에 맞는 플레이북(README 기준 23개)을 고릅니다. 기능 플레이북을 고르면 영향 범위를 파악하고 설계를 탐색한 뒤, 먼저 끝낼 단계, 독립 작업, 공유 상태, 가장 작은 안전한 분할을 점검하고, 파일 범위와 데이터 구조, 성공 기준을 정해 구현을 맡깁니다. 그다음 돌아온 결과를 실제 동작으로 검증합니다. 코드, 테스트, 실행 결과를 근거와 대조하는 것이며, 화면 캡처만 보는 것이 아닙니다. 플레이북마다 단계는 다르고, 한 기능처럼 코드가 엮인 일은 한 담당자에게 둡니다. pstack에도 계획과 테스트가 있습니다.</p>
<p><strong>아래 띠 읽는 법:</strong> '기본기는 모델에, 업무 기준과 위임은 하네스에'는 강조점입니다. 두 층을 딱 잘라 나누는 구조도가 아니며, 하네스가 기본기를 신경 쓰지 않아도 된다는 뜻도 아닙니다. 두 묶음은 계획, 위임, 검토, 테스트를 함께 갖추고, 겹치는 부분이 많습니다. 바꿔 쓴다고 정확도나 속도가 저절로 오른다고 말하지 않으며, 잰 수치도 없습니다.</p>
<p><strong>실행 환경:</strong> pstack은 Cursor 이름으로 쓰여 있고 Claude Code용 어댑터가 이름을 바꿔 대응하며, Cursor 전용 기능은 건너뜁니다. 호스트마다 똑같이 동작한다고 말하지 않습니다. Superpowers도 여러 코딩 에이전트에 설치 경로를 안내합니다.</p>
<p><strong>표기 주의:</strong> Superpowers README의 스킬 목록에는 '두 단계 검토'라는 표현이 남아 있지만, 같은 커밋의 subagent-driven-development 본문은 작업별 검토 한 번이 명세와 품질을 함께 본다고 설명합니다. 이 화면은 스킬 본문을 따랐습니다.</p>
{_sources_html()}"""
    return dict(kind="reference", reference="A", label="참고 A: 기본기 다음은, 검증과 위임",
                theme="t-paper", body=body, notes=notes, chapter=2, layout="reference")


# ---------------------------------------------------------------- slide 16: keep in step with 15

REF_B_EDITS = [
    ('>TO-BE pstack에서 가져올 것<', '>pstack에서 참고할 운영 방식<'),
    ('>AS-IS Superpowers (비교 참고)<', '>Superpowers에서 참고할 기본기<'),
]

REF_B_NOTES = [
    ("15쪽에서 Superpowers는 AS-IS, pstack은 TO-BE입니다. 이 화면에서도 pstack은 가져올 방향, Superpowers는 지금 방식의 비교 참고이며, OMH 구현의 근거로 제시하지 않습니다.",
     "15쪽처럼 Superpowers는 잘 만든 기본 절차로, pstack은 일에 맞춘 검증과 위임을 운영하는 방식으로 참고합니다. Superpowers는 비교 참고이며, OMH 구현의 근거로 제시하지 않습니다."),
]


def _ref_b(sl):
    body, notes = sl["body"], sl["notes"]
    for old, new in REF_B_EDITS:
        if body.count(old) != 1:
            raise SystemExit(f"v11 slide 16: expected one match for {old[:60]}")
        body = body.replace(old, new)
    for old, new in REF_B_NOTES:
        if notes.count(old) != 1:
            raise SystemExit(f"v11 slide 16 notes: expected one match for {old[:60]}")
        notes = notes.replace(old, new)
    # the pinned release notes join the source list, as on slide 15
    old_src = copy_v07._sources_html()
    if notes.count(old_src) != 1:
        raise SystemExit("v11 slide 16 notes: expected one source list")
    sl["body"], sl["notes"] = body, notes.replace(old_src, _sources_html())


def apply_refs(slides):
    out = []
    for sl in slides:
        if sl.get("reference") == "A":
            out.append(ref_a())
        else:
            if sl.get("reference") == "B":
                _ref_b(sl)
            out.append(sl)
    return out
