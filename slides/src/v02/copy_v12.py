"""v12: slides 14, 15 and 27 rewritten for impact and reading order. Everything else as in v11.

- Slide 14 (OMH): leads with a concrete catch instead of a component list. Task:
  fill blank `amount` values with 0 and add or delete no rows. The first result
  keeps three rows and clears the blank, so a row count and a blank count both
  look fine, but one original ID is gone and one new ID appears. The prepared
  keyed data_compare reports left_only 1 and right_only 1, the review criterion
  (추가, 삭제 0건) sends it back before completion, and the fixed result compares
  with left_only 0 and right_only 0. The counts are real tool output on the
  synthetic fixture in examples/omh-v12/ (run_example.py); the role and review
  flow around them is illustrative. Bare OpenCode can do the same with its own
  scripts; the difference shown is what must be written and wired each time.
- Slide 15 (참고 A): the thesis becomes the title, and the diagram reads top to
  bottom: Superpowers execution habits first, then the pstack focus in blue.
  v11 claim boundaries and sources stay.
- Slide 27 (사례 4 AI교양): the compressed four-step flow is replaced by the same
  seven steps, colours and role labels as slide 2, inside the five harness parts.
"""

import re

from kit import (AMBER, AMBER_SOFT, BLUE, BLUE_SOFT, INK, INK2, MUTED, PAPER2, WHITE, Svg, case_head, e, p)

import copy_v07
import copy_v11

# ---------------------------------------------------------------- slide 14: the catch before completion

# real data_compare / data_inspect facts on examples/omh-v12/data (see evidence/summary.json)
FIRST = {"rows": (3, 3), "blanks": (1, 0), "left_only": 1, "right_only": 1, "value_changed": 1}
FIXED = {"rows": (3, 3), "blanks": (1, 0), "left_only": 0, "right_only": 0, "value_changed": 1}


def omh_svg():
    s = Svg("s14", 120, 340, 1680, 600,
            "같은 요청, CSV 빈 amount만 0으로 바꾸고 행 추가와 삭제는 0건. 왼쪽 OpenCode 순정은 전용 도구가 없으면 빈 값 점검 스크립트, "
            "id 비교 코드, 검토 기준 연결을 직접 준비한다. 오른쪽 OMH 통합 구성은 OMO 역할 분담과 검토, data_inspect와 data_compare, "
            "omh-rigorous 절차를 미리 묶어 다시 쓴다. 첫 결과는 행 3개, 빈 값 0개로 겉보기엔 통과지만, id 기준 data_compare가 "
            "left_only 1, right_only 1을 찾고, 검토 기준에 걸려 완료 전에 되돌린다. 수정 결과는 left_only 0, right_only 0")
    sm = {"size": 24, "weight": 400, "fill": INK2}
    mono = {"size": 24, "weight": 700, "fill": BLUE, "mono": True}
    s.rect(0, 0, 1680, 54, fill=PAPER2)
    s.text(24, 27, "요청", size=26, weight=800, fill=MUTED)
    s.text(110, 27, "CSV 빈 amount만 0으로, 행 추가와 삭제는 0건", size=28, weight=800)
    s.text(1656, 27, "같은 모델, 추가 학습 없음", size=26, fill=INK2, anchor="end")

    # left: bare OpenCode, everything prepared for this one task
    s.rect(0, 80, 540, 410, fill=WHITE, stroke=INK, sw=2.5, extra=' data-box="opencode"')
    s.text(28, 118, "OpenCode 순정", size=30, weight=800)
    s.text(28, 154, "전용 도구가 없으면 직접 준비할 것", size=24, weight=800, fill=AMBER)
    prep = [("빈 값 점검 스크립트", "열과 빈 값 수 세기"), ("id 비교 코드", "빠진 ID, 새 ID 찾기"),
            ("검토 기준 연결", "'추가, 삭제 0'을 프롬프트로")]
    for k, (t, d) in enumerate(prep):
        y = 204 + k * 80
        s.text(28, y, str(k + 1), size=26, weight=800, fill=MUTED)
        s.text(64, y, t, size=28, weight=800)
        s.text(64, y + 34, d, size=24, fill=INK2)
    s.text(28, 432, "할 수는 있음, 다만 직접 짜서 검토에 연결", size=24, weight=800, fill=INK2)
    s.text(28, 466, "행 수, 빈 값만 세면 첫 결과도 통과로 보임", size=24, fill=AMBER)

    # right: the OMH package, OMO inside, with the scene it makes routine
    s.rect(580, 80, 1100, 410, fill="none", stroke=BLUE, sw=4, extra=' data-box="omh"')
    s.text(608, 118, "OMH 통합 구성", size=30, weight=800, fill=BLUE)
    s.text(1652, 118, "미리 묶어 다시 쓰는 것", size=24, weight=800, fill=BLUE, anchor="end")
    s.rect(608, 140, 300, 52, fill=BLUE_SOFT, stroke=BLUE, sw=2.5, extra=' data-box="omo"')
    s.text(758, 166, "OMO: 역할 분담, 검토", size=24, weight=800, anchor="middle")
    s.rect(924, 140, 420, 52, fill=WHITE, stroke=BLUE, sw=2.5, extra=' data-box="tools"')
    s.text(1134, 166, "data_inspect, data_compare", size=24, weight=700, fill=BLUE, anchor="middle", mono=True)
    s.rect(1360, 140, 292, 52, fill=WHITE, stroke=BLUE, sw=2.5, extra=' data-box="procedure"')
    s.text(1506, 166, "절차: omh-rigorous", size=24, weight=800, anchor="middle")
    xs = [608, 874, 1140, 1406]
    steps = [
        (["첫 결과", ("행 3 → 3", sm), ("빈 값 1 → 0", sm), ("겉보기엔 통과", sm)], WHITE, INK, 2.5, "first"),
        (["id 기준 비교", ("전체 범위", sm), (f"left_only {FIRST['left_only']}", mono),
          (f"right_only {FIRST['right_only']}", mono)], BLUE_SOFT, BLUE, 3, "compare"),
        (["검토 기준", ("추가, 삭제 0건", sm), ("ID 1건 빠지고", sm), ("새 ID 1건 생김", sm)], AMBER_SOFT, AMBER, 3.5, "review"),
        (["수정 결과", (f"left_only {FIXED['left_only']}", mono), (f"right_only {FIXED['right_only']}", mono),
          ("amount 1행만 변경", sm)], BLUE_SOFT, BLUE, 3, "fixed"),
    ]
    for k, (x, (lines, fill, stroke, sw, key)) in enumerate(zip(xs, steps)):
        s.rect(x, 216, 246, 180, fill=fill, stroke=stroke, sw=sw, extra=f' data-step="{key}"')
        s.lines(x + 123, 306, lines, size=26, weight=800, anchor="middle", lh=1.36)
        s.num(x, 216, k + 1, fill=AMBER if key == "review" else INK if key == "first" else BLUE)
        if k < 3:
            s.arrow([(x + 248, 306), (xs[k + 1] - 6, 306)], color="amber" if k == 1 else "blue")
    s.text(1140 + 123, 422, "완료 보고 전에 되돌림", size=24, weight=800, fill=AMBER, anchor="middle")
    s.text(608, 462, "data_compare: 행 값 없이 개수와 위치만, 자동 병합 없음", size=24, fill=INK2)

    s.rect(0, 510, 1680, 90, fill=WHITE, stroke=BLUE, sw=3)
    s.text(28, 538, "쓰는 이유", size=26, weight=800, fill=BLUE)
    s.text(190, 538, "미리 만든 점검, 비교 도구와 검토 흐름을 그대로 다시 씀", size=28, weight=800)
    s.text(190, 576, "같은 형식의 전체 범위 결과가 검토로 넘어가, 의도치 않은 ID 변경을 완료 전에 잡음", size=24, fill=INK2)
    return s.render()


def omh_body():
    return "\n  ".join([
        case_head(2, "OMH"),
        p("qline case-q", "<b>질문</b>OpenCode만으로도 할 수 있는 일, 왜 OMH 묶음으로 할까?"),
        p("case-title", "행 수는 그대로, 빠진 ID까지 찾아내기", "h2"),
        omh_svg(),
        p("foot", "합성 예시 CSV로 data_inspect, data_compare를 실제 실행한 개수. 역할과 검토 흐름은 설명용",
          style="left:120px;top:968px;width:1680px;margin:0;color:#B45309;font-weight:700"),
    ])


OMH_NOTES = """<p><strong>장면:</strong> 요청은 'CSV의 빈 amount만 0으로 바꾸고, 행은 더하지도 지우지도 말 것'입니다. 첫 결과를 보면 행은 3개 그대로이고 빈 값은 1개에서 0개가 됐습니다. 행 수와 빈 값만 세면 통과로 보입니다. 그런데 id 기준으로 맞춰 보면 원래 있던 ID 하나가 사라지고, 없던 ID 하나가 생겼습니다. 이 화면이 보여 주려는 것은 이런 의도치 않은 변경을 완료 보고 전에 잡는 장면입니다.</p>
<p><strong>OMH를 쓰는 이유:</strong> OpenCode 순정에서는 이 일을 위해 열과 빈 값을 세는 점검 스크립트, id 기준으로 빠진 행과 새 행을 찾는 비교 코드, '추가, 삭제 0건'이라는 검토 기준을, 전용 도구를 따로 만들어 두지 않았다면 직접 준비하고 프롬프트로 이어 붙여야 합니다. 이미 만들어 둔 스크립트가 있다면 그것을 다시 쓸 수도 있습니다. OMH 통합 구성에는 그 점검(data_inspect)과 비교(data_compare)가 시험을 거쳐 같은 형식의 결과를 내는 도구로 준비돼 있고, OMO의 역할 분담과 검토 흐름, 필요할 때 쓰는 절차(omh-rigorous)가 함께 묶여 있습니다. 순정에는 기본으로 없는 업무 전용 도구와 검토 흐름을 묶음으로 제공해, 같은 종류의 일에 다시 쓸 수 있다는 점이 핵심입니다.</p>
<p><strong>실제로 실행한 것:</strong> examples/omh-v12/의 합성 CSV 세 개(원본, 첫 결과, 수정 결과, 각 3행)에 OMH 통합 v04 묶음의 엔진으로 data_inspect와 data_compare를 실제로 실행했습니다. 첫 결과는 id 기준 전체 범위 비교에서 left_only 1(원본에만 있는 ID), right_only 1(결과에만 있는 ID), value_changed 1(amount)이 나왔고, 수정 결과는 left_only 0, right_only 0, value_changed 1(amount만)이었습니다. 빈 amount는 원본 1개, 두 결과 모두 0개였습니다. 값은 반환하지 않게 해서(include_values false) 화면에는 ID 값이 아니라 개수만 적었습니다. 도구 결과의 ok는 호출이 성공했다는 뜻일 뿐 업무 기준 통과가 아니며, 기준 판단(추가, 삭제 0건)은 검토 단계가 따로 합니다. 다시 돌리는 방법과 결과 파일은 examples/omh-v12/에 있습니다.</p>
<p><strong>설명용인 부분:</strong> 첫 결과 파일은 이 장면을 위해 손으로 만든 합성 데이터이며, 에이전트가 실제로 낸 실수를 기록한 것이 아닙니다. 검토 역할이 기준에 걸어 되돌리고 다시 비교하는 흐름도 설명용입니다. 모델이 늘 이렇게 판단한다거나, 자동으로 막는 관문이 있다는 뜻이 아닙니다.</p>
<p><strong>순정도 할 수 있는 일:</strong> OpenCode 순정의 에이전트도 스크립트를 짜서 같은 비교를 하고, 기준을 프롬프트로 주면 같은 문제를 잡을 수 있습니다. 순정이 못 한다거나 늘 실패한다는 이야기가 아닙니다. 차이는 그 점검 코드와 검토 연결을 직접 준비하고 이어 붙이느냐, 시험을 거쳐 미리 묶어 둔 도구와 검토 절차를 다시 쓰느냐입니다.</p>
<p><strong>묶음 구성과 전제:</strong> OMH 통합 구성은 OMO의 역할 협업과 작업 흐름, OMO의 원래 플러그인과 실행기, 의존성까지 한 패키지에 담고, 그 위에 업무 도구와 절차를 더한 것입니다. 그래서 그림에서 OMO는 OMH 경계 안에 있습니다. OpenCode와 Python은 미리 설치해야 하는 전제이고 패키지에 들어 있지 않습니다. 두 쪽은 같은 설정 모델을 쓰고, 추가 학습은 없습니다.</p>
<p><strong>말하지 않는 것:</strong> 속도나 정확도 수치, 오류가 없다는 보장, 질문 횟수가 늘 준다는 주장은 하지 않습니다. 비교 결과를 받아들일지는 여전히 사람이 결정합니다. 근거는 OMH 통합 v04 참고 문서(구성과 조건, 역할, 도구)이며 로컬 보관 자료로 이 저장소에 들어 있지 않습니다.</p>"""

# ---------------------------------------------------------------- slide 15: thesis first, Superpowers then pstack

TITLE_15 = "기본기는 모델에, 업무 기준과 위임은 하네스에"


def ref_a():
    s = Svg("s15", 120, 330, 1680, 620, "위에서 아래로 읽는 그림. 먼저 Superpowers의 실행 기본기: 계획, 구현, 테스트, 반복 수정. "
            "잘 만든 기본 절차이고 계속 다듬어지며 모델에도 스며들고 있다. 그 위에서 이 일에 맞게, pstack에서 참고할 다음 초점: "
            "성공 기준과 근거, 작업별 절차 선택, 범위 정한 위임, 돌아온 결과 검증. 두 묶음 모두 계획, 위임, 검토, 테스트를 갖춘다")
    sm = {"size": 24, "weight": 400, "fill": INK2}
    xs = [340, 680, 1020, 1360]
    # first: Superpowers, execution habits
    s.box(0, 0, 300, 176, [("먼저, 실행 기본기", {"size": 24, "weight": 800, "fill": MUTED}), "Superpowers",
                           ("잘 만든 기본 절차,", sm), ("계속 다듬어지는 습관", sm)],
          size=32, weight=800, fill=PAPER2, stroke=INK, lh=1.3)
    habits = [["계획", ("작은 단위로 나눔", sm)], ["구현", ("명세에 맞춰 작성", sm)],
              ["테스트", ("통과할 때까지 확인", sm)], ["반복 수정", ("검토 받고 고침", sm)]]
    for k, (x, lines) in enumerate(zip(xs, habits)):
        s.box(x, 13, 300, 150, lines, size=28, weight=800, fill=WHITE, stroke=INK, sw=2.5, lh=1.4)
        if k < 3:
            s.arrow([(x + 302, 88), (xs[k + 1] - 6, 88)])
    # a modest reading connector, not a migration arrow
    s.arrow([(150, 180), (150, 232)], color="blue")
    s.text(184, 206, "그 위에서, 이 일에 맞게", size=26, weight=800, fill=BLUE)
    # then: pstack, the next focus, in strong blue
    s.box(0, 238, 300, 200, [("다음 초점", {"size": 24, "weight": 800, "fill": WHITE}), "pstack",
                             ("일에 맞춘 검증과 위임", {"size": 24, "weight": 400, "fill": WHITE})],
          size=32, weight=800, fill=BLUE, stroke=BLUE, color=WHITE, lh=1.35)
    focus = [["성공 기준과 근거", ("완료 기준을 먼저 정함", sm)], ["작업별 절차 선택", ("일에 맞는 플레이북", sm)],
             ["범위 정한 위임", ("파일 범위와 완료 조건", sm)], ["돌아온 결과 검증", ("실제 동작과 근거 대조", sm)]]
    for k, (x, lines) in enumerate(zip(xs, focus)):
        s.box(x, 253, 300, 170, lines, size=28, weight=800, fill=BLUE_SOFT, stroke=BLUE, sw=3, lh=1.4)
        if k < 3:
            s.arrow([(x + 302, 338), (xs[k + 1] - 6, 338)], color="blue")
    s.rect(0, 470, 1680, 130, fill=PAPER2)
    s.text(28, 512, "겹치는 부분", size=26, weight=800, fill=BLUE)
    s.text(220, 512, "두 묶음 모두 계획, 위임, 검토, 테스트를 갖춤", size=28, weight=800)
    s.text(220, 558, "계획하고 시험하는 기본기는 모델에 스며들고, 하네스는 이 일의 기준과 근거, 위임을 챙김",
           size=24, fill=INK2)
    body = "\n  ".join([
        copy_v07._head("참고 A", "Superpowers와 pstack"),
        p("qline case-q", "<b>질문</b>계획하고 테스트하는 습관이 기본이 되면, 하네스는 무엇을 더 챙겨야 할까?"),
        p("case-title", TITLE_15, "h2"),
        s.render(),
        p("foot", e(copy_v07.PROVENANCE), style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    return dict(kind="reference", reference="A", label=f"참고 A: {TITLE_15}",
                theme="t-paper", body=body, notes=_ref_a_notes(), chapter=2, layout="reference")


REF_A_NOTES = [
    ("이 발표는 하네스의 다음 초점을 그 위의 층, 곧", "이 발표는 하네스의 다음 초점을 그다음 단계, 곧"),
    ("<p><strong>아래 층, 실행 기본기:</strong>", "<p><strong>먼저 읽는 위 줄, 실행 기본기:</strong>"),
    ("<p><strong>위 층, 업무 운영:</strong>", "<p><strong>이어서 읽는 아래 줄, 다음 초점:</strong>"),
    ("<p><strong>아래 띠 읽는 법:</strong> '기본기는 모델에, 업무 기준과 위임은 하네스에'는 강조점입니다. 두 층을",
     "<p><strong>제목과 읽는 순서:</strong> 제목 '기본기는 모델에, 업무 기준과 위임은 하네스에'가 이 화면의 요지이며, 발표자의 강조점입니다. "
     "그림은 위에서 아래로 읽습니다. 먼저 Superpowers가 잘 다듬어 온 실행 기본기를 보고, 이어서 pstack에서 참고할 다음 초점, "
     "곧 이 일에 맞춘 기준과 근거, 절차 선택, 위임, 검증을 파란색으로 봅니다. 위아래는 설명 순서이지 순위나 전환 단계가 아닙니다. 두 줄을"),
]


def _ref_a_notes():
    notes = copy_v11.ref_a()["notes"]
    for old, new in REF_A_NOTES:
        if notes.count(old) != 1:
            raise SystemExit(f"v12 slide 15 notes: expected one match for {old[:60]}")
        notes = notes.replace(old, new)
    return notes


# ---------------------------------------------------------------- slide 27: the opening seven steps inside the harness


def ai_svg():
    s = Svg("s25", 120, 360, 1680, 580, "AI교양 일곱 단계: 작가가 주제를 찾고 고르고, 초고 v01을 직접 쓰고, AI와 함께 검토하고 수정한 뒤, "
            "작가가 최종본을 확정하고, 그다음 삽화 생성과 보관, 네이버 비공개 초안, 다시 열어 확인. 둘레에 규칙, 컨텍스트, 도구, "
            "상태, 검증. 공개 발행은 이 흐름 밖")
    top = [("규칙", "초고 v01 보존과 버전, 확정 문장 불변"), ("컨텍스트", "해당 글, 수정 이력, 관련 근거"),
           ("도구", "파일 저장, 이미지 생성, 초안 작성")]
    for i, (t, d) in enumerate(top):
        x = i * 570
        s.rect(x, 0, 540, 100, fill=PAPER2)
        s.text(x + 28, 32, t, size=28, weight=800, fill=BLUE)
        s.text(x + 28, 72, d, size=26, fill=INK2)
    # the same seven steps, colours and role labels as slide 2
    steps = [(["주제를", "찾고 고르기"], "author"), (["초고 v01을", "직접 쓰기"], "author"),
             (["AI와 함께", "검토, 수정"], "ai"), (["최종본", "확정"], "author"),
             (["삽화 생성,", "보관"], "run"), (["네이버", "비공개 초안"], "run"), (["다시 열어", "확인"], "run")]
    w, gap, y0 = 212, 32, 140
    for i, (lab, who) in enumerate(steps):
        x = i * (w + gap)
        fill, stroke, sw = {"author": (AMBER_SOFT, AMBER, 3.5), "ai": (BLUE_SOFT, BLUE, 3.5),
                            "run": (WHITE, INK, 2.5)}[who]
        s.rect(x, y0, w, 140, fill=fill, stroke=stroke, sw=sw, extra=f' data-step="{i + 1}" data-role="{who}"')
        s.lines(x + w / 2, y0 + 70, lab, size=28, weight=800, anchor="middle")
        s.num(x, y0, i + 1, fill=AMBER if who == "author" else BLUE if who == "ai" else INK)
        if i < len(steps) - 1:
            s.arrow([(x + w + 2, y0 + 70), (x + w + gap - 4, y0 + 70)])
    s.line(0, 316, 2 * w + gap, 316, color=AMBER, sw=4)
    s.text(0, 344, "작가의 몫", size=26, weight=800, fill=AMBER)
    s.line(2 * (w + gap), 316, 3 * (w + gap) - gap, 316, color=BLUE, sw=4)
    s.text(2 * (w + gap), 344, "AI와 함께", size=26, weight=800, fill=BLUE)
    s.line(3 * (w + gap), 316, 4 * (w + gap) - gap, 316, color=AMBER, sw=4)
    s.text(3 * (w + gap), 344, "작가가 결정", size=26, weight=800, fill=AMBER)
    s.line(4 * (w + gap), 316, 1680, 316, color=INK, sw=4)
    s.text(4 * (w + gap), 344, "확정 뒤 정해진 절차", size=26, weight=800)
    s.text(0, 398, "삽화는 4단계 작가 확정 뒤에, 확정 전이면 3단계로 돌아가 수정", size=26, weight=800, fill=AMBER)
    s.rect(1180, 372, 500, 52, fill="none", stroke=AMBER, sw=2, dash="8 7")
    s.text(1430, 398, "공개 발행은 이 흐름 밖", size=26, weight=700, fill=AMBER, anchor="middle")
    bottom = [("상태", "현재 버전, 확정 여부, 단계별 결과, 초안 번호"), ("검증", "저장본과 비교, 초안 다시 열어 확인")]
    for i, (t, d) in enumerate(bottom):
        x = i * 855
        s.rect(x, 460, 825, 110, fill=PAPER2)
        s.text(x + 28, 492, t, size=28, weight=800, fill=BLUE)
        s.text(x + 28, 536, d, size=26, fill=INK2)
    return s.render()


AI_NOTES = """<p><strong>화면 읽기:</strong> 가운데 일곱 단계는 2쪽 시작 화면과 같은 순서, 같은 색입니다. 작가가 주제를 찾고 고르고, 초고 v01을 직접 씁니다(AI가 만든 초안이 아님). 그다음 AI와 함께 검토하고 수정하며 새 버전으로 남기고, 작가가 최종본을 확정합니다. 확정 뒤에 삽화를 만들어 보관하고, 네이버 비공개 초안을 만든 뒤 다시 열어 확인합니다. 공개 발행은 이 흐름 밖입니다.</p>
<p><strong>질문에 대한 답:</strong> 확정 전에 삽화를 만들자는 요청이 오면, 4단계 작가 확정을 기다립니다. 확정되지 않았으면 3단계로 돌아가 다시 고칩니다. 확정은 사람이 정하는 단계이고, 확정 뒤 단계는 정해진 절차로 이어집니다.</p>
<p><strong>둘레의 다섯 칸:</strong> 위의 규칙, 컨텍스트, 도구와 아래의 상태, 검증이 일곱 단계를 받칩니다. 단계만 보면 워크플로우, 그 단계를 실행하고 확인하는 장치까지 보면 업무용 하네스입니다. 별도의 상태 머신이 전환을 자동으로 강제한다는 뜻은 아닙니다.</p>"""

CORRECTIONS = {
    25: ("v12부터 27쪽 가운데 흐름은 2쪽 시작 화면과 같은 일곱 단계(주제 찾고 고르기, 초고 v01 직접 쓰기, AI와 함께 검토와 수정, "
         "작가 최종 확정, 삽화 생성과 보관, 네이버 비공개 초안, 다시 열어 확인)로 바꿨다. 이전 판의 네 단계 압축 흐름(초고 보존, "
         "AI와 함께 수정, 작가 확정 마름모, 이후 단계 묶음)은 이 순서로 대체한다. 아래 v10 발췌(S21)의 '원문이 들어왔다'와 "
         "'원문 보존'은 작가가 직접 쓴 초고 v01을 가리키며, AI가 만든 초안이 아니다."),
}


def _ai_body(sl):
    body, n = re.subn(r'<svg class="svg".*?</svg>', lambda m: ai_svg(), sl["body"], count=1, flags=re.S)
    if n != 1:
        raise SystemExit("v12 slide 27: expected one diagram")
    sl["body"] = body
    sl["notes"] = AI_NOTES


def apply(orig, sl):
    if orig == 14:
        sl["body"] = omh_body()
        sl["notes"] = OMH_NOTES
    elif orig == 25:
        _ai_body(sl)


def apply_refs(slides):
    return [ref_a() if sl.get("reference") == "A" else sl for sl in slides]
