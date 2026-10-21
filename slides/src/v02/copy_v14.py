"""v14: slide 14 shows the bare OpenCode process in four steps. Everything else as in v13.

The left panel no longer lists prepared parts; it walks the same plain request
through four steps (edit the table, compare with the original, review against
the criterion, hand back if needed), with a quiet dashed return from step 4 to
step 1. Bare OpenCode can do all four; the difference (prepared comparison tool
and review hand-off) stays in the bottom summary and the notes. The on-screen
footnote is gone; the summary sits lower in the freed space. The three roles,
six hand-offs and the change strip on the right are those of v13, re-spaced for
the taller panel. The factual boundary (real tool facts, illustrative role flow)
lives in the notes and docs/production/process-v14.md.
"""

from kit import AMBER, BLUE, BLUE_SOFT, INK, INK2, PAPER2, WHITE, Svg, case_head, p

import copy_v13

ROLES = copy_v13.ROLES
ROLE_Y, ROLE_H = 170, 350
ROWS = {222: 236, 310: 336, 410: 446}  # v13 row y -> v14 row y
FLOWS = [(label, src, dst, ROWS[y], colour, dashed, kind) for label, src, dst, y, colour, dashed, kind in copy_v13.FLOWS]
STEPS = [("표를 고침", "금액 빈칸에 0을 채움"), ("원본과 비교", "비교 코드를 짜서 맞춰 봄"),
         ("기준에 따라 검토", "번호, 상품이 그대로인지"), ("필요하면 다시 맡김", "고칠 것을 되돌림")]


def _edge(role, side):
    x, w = ROLES[role]
    return x + w if side == "right" else x


def omh_svg():
    s = Svg("s14", 120, 340, 1680, 650,
            "요청: 표의 금액 빈칸만 0으로 채우고 번호와 상품은 그대로. 왼쪽 OpenCode 순정은 네 단계로 진행한다: 표를 고침, 원본과 비교, "
            "기준에 따라 검토, 필요하면 다시 맡김. 오른쪽 OMH 통합 구성 안의 OMO 역할 협업: 총괄이 기준을 정해 작업 담당에게 맡기고, "
            "원본과 결과를 검토 담당에게 비교하게 한다. 검토 담당은 준비된 비교 도구로 금액 빈칸이 0이 된 것은 요청한 변경, "
            "상품 A의 번호가 0에서 3으로 바뀐 것은 요청 밖 변경이라고 찾는다. 같은 총괄이 다시 고치게 하고, 검토를 통과한 뒤 보고한다")
    s.rect(0, 0, 1680, 54, fill=PAPER2)
    s.text(24, 27, "요청", size=26, weight=800, fill=INK2)
    s.text(110, 27, "표의 금액 빈칸만 0으로 채워 줘. 번호와 상품은 그대로", size=28, weight=800)
    s.text(1656, 27, "같은 모델, 추가 학습 없음", size=26, fill=INK2, anchor="end")

    # left: bare OpenCode, the process it runs for this request
    s.rect(0, 80, 440, 460, fill=WHITE, stroke=INK, sw=2.5, extra=' data-box="opencode"')
    s.text(28, 118, "OpenCode 순정", size=30, weight=800)
    s.text(28, 156, "같은 일을 직접 꾸려 진행", size=24, weight=800, fill=AMBER)
    for k, (t, d) in enumerate(STEPS):
        y = 214 + k * 82
        s.add(f'<g data-step="{k + 1}">')
        s.text(28, y, str(k + 1), size=26, weight=800, fill=INK2)
        s.text(64, y, t, size=28, weight=800)
        s.text(64, y + 32, d, size=24, fill=INK2)
        s.add("</g>")
    # when the review finds a problem, step 4 goes back to step 1
    s.arrow([(376, 460), (410, 460), (410, 214), (376, 214)], color="amber", dash="8 6")

    # right: OMH boundary, OMO role collaboration inside it
    s.rect(470, 80, 1210, 460, fill="none", stroke=BLUE, sw=4, extra=' data-box="omh"')
    s.text(498, 106, "OMH 통합 구성", size=28, weight=800, fill=BLUE)
    s.text(1652, 106, "준비된 비교 도구와 절차 포함", size=24, weight=800, fill=BLUE, anchor="end")
    s.rect(490, 128, 1170, 400, fill="none", stroke=BLUE, sw=2, dash="8 6", extra=' data-box="omo"')
    s.text(510, 150, "OMO 역할 협업", size=24, weight=800, fill=BLUE)

    lead_x, lead_w = ROLES["lead"]
    work_x, _ = ROLES["worker"]
    rev_x, rev_w = ROLES["reviewer"]
    for role, (x, w) in ROLES.items():
        fill, stroke, sw = (BLUE_SOFT, BLUE, 3) if role == "lead" else (WHITE, INK, 2.5)
        s.rect(x, ROLE_Y, w, ROLE_H, fill=fill, stroke=stroke, sw=sw, extra=f' data-role="{role}"')
    s.text(work_x + 20, 202, "작업 담당", size=28, weight=800)
    s.text(work_x + 20, 236, "표를 고침", size=24, fill=INK2)
    s.text(work_x + 20, 376, "줄 수 3 → 3", size=24)
    s.text(work_x + 20, 408, "빈칸 1 → 0", size=24)
    s.text(work_x + 20, 482, "겉보기엔 끝", size=24, weight=800, fill=AMBER)
    s.text(lead_x + 20, 202, "총괄", size=28, weight=800, fill=BLUE)
    s.text(lead_x + 20, 236, "기준, 맡김", size=24, fill=INK2)
    s.text(lead_x + 20, 376, "기준", size=24, weight=800, fill=BLUE)
    s.text(lead_x + 20, 408, "번호, 상품 유지", size=24)
    s.text(lead_x + 20, 482, "줄 추가, 삭제 0", size=24)
    s.text(rev_x + 20, 202, "검토 담당", size=28, weight=800)
    s.text(rev_x + 20, 236, "원본과 결과 비교", size=24, fill=INK2)
    s.rect(rev_x + 12, 262, rev_w - 24, 160, fill=PAPER2)
    s.text(rev_x + 24, 290, "금액 빈칸 → 0", size=24, weight=800)
    s.text(rev_x + 24, 322, "요청한 변경", size=24, weight=800, fill=BLUE)
    s.text(rev_x + 24, 362, "상품 A 번호 0 → 3", size=24, weight=800)
    s.text(rev_x + 24, 394, "요청 밖 변경", size=24, weight=800, fill=AMBER)
    s.rect(rev_x + 12, 444, rev_w - 24, 64, fill=WHITE, stroke=BLUE, sw=2, extra=' data-box="tools"')
    s.text(rev_x + 28, 462, "준비된 비교 도구", size=24, weight=700, fill=BLUE)
    s.text(rev_x + 28, 490, "data_compare", size=24, weight=700, fill=BLUE, mono=True)

    for label, src, dst, y, colour, dashed, kind in FLOWS:
        left_to_right = ROLES[src][0] < ROLES[dst][0]
        x1 = _edge(src, "right" if left_to_right else "left")
        x2 = _edge(dst, "left" if left_to_right else "right")
        x1 += 2 if left_to_right else -2
        x2 += -6 if left_to_right else 6
        s.arrow([(x1, y), (x2, y)], color=colour, dash="9 7" if dashed else None)
        s.parts[-1] = s.parts[-1].replace(
            "<polyline ", f'<polyline data-from="{src}" data-to="{dst}" data-kind="{kind}" ', 1)
        fill = {"blue": BLUE, "amber": AMBER, "ink": INK}[colour]
        s.text((x1 + x2) / 2, y - 20, label, size=24, weight=800, fill=fill, anchor="middle")
    cx = lead_x + lead_w / 2
    s.arrow([(cx, ROLE_Y - 2), (cx, 58)], color="blue")
    s.parts[-1] = s.parts[-1].replace(
        "<polyline ", '<polyline data-from="lead" data-to="requester" data-kind="report" ', 1)
    s.text(cx + 16, 150, "검토 통과 뒤 보고", size=24, weight=800, fill=BLUE)

    s.rect(0, 560, 1680, 90, fill=WHITE, stroke=BLUE, sw=3, extra=' data-box="summary"')
    s.text(28, 588, "쓰는 이유", size=26, weight=800, fill=BLUE)
    s.text(190, 588, "역할을 나눠 맡기고, 준비된 비교로 요청 밖 변경을 보고 전에 확인", size=28, weight=800)
    s.text(190, 626, "OpenCode 순정도 네 단계를 할 수 있지만, 비교 도구와 검토 연결은 직접 준비해야 함", size=24, fill=INK2)
    return s.render()


def omh_body():
    return "\n  ".join([
        case_head(2, "OMH"),
        p("qline case-q", "<b>질문</b>OpenCode만으로도 되는 일, OMH로 하면 무엇이 달라질까?"),
        p("case-title", "빈칸만 채우랬는데, 번호까지 바뀌었다면?", "h2"),
        omh_svg(),
    ])


LEFT_NOTE = """<p><strong>왼쪽, OpenCode 순정의 진행:</strong> 같은 요청을 OpenCode 순정으로 하면 네 단계로 진행합니다. 표를 고치고(금액 빈칸에 0), 원본과 비교하고(비교 코드를 짜서), 기준에 따라 검토하고(번호와 상품이 그대로인지), 문제가 있으면 다시 맡깁니다. 호박색 점선은 검토에서 문제가 나오면 처음 단계로 돌아간다는 뜻입니다. 에이전트는 이 네 단계를 모두 할 수 있고, 하위 작업을 맡기거나 만들어 둔 스크립트를 다시 쓸 수도 있습니다. 다른 점은 전용 비교 도구와 검토 연결이 미리 준비돼 있느냐입니다.</p>
<p><strong>화면에서 뺀 각주:</strong> v13 화면 아래의 '역할 흐름은 설명용' 각주는 v14에서 화면에서 뺐습니다. 아래 '실제로 실행한 것'과 '설명용인 부분'이 그 경계를 그대로 설명합니다.</p>
"""


def _notes():
    anchor = "<p><strong>역할 흐름 (설명용):</strong>"
    notes = copy_v13.OMH_NOTES
    if notes.count(anchor) != 1:
        raise SystemExit("v14 slide 14 notes: expected one role-flow paragraph")
    return notes.replace(anchor, LEFT_NOTE + anchor, 1)


def apply(orig, sl):
    if orig == 14:
        sl["body"] = omh_body()
        sl["notes"] = _notes()
