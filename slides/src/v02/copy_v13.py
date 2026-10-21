"""v13: slide 14 retold as a role handoff. Everything else as in v12.

The request is said plainly (fill only the blank prices, keep numbers and
products). Inside the OMH boundary, the OMO role collaboration shows three
roles: 총괄 takes the request, sets the criterion and assigns; 작업 담당 edits
the table; 검토 담당 compares original and result with the prepared comparison
tool and flags the unrequested number change. The correction goes back through
the same 총괄, and 총괄 reports only after the re-check. Bare OpenCode can do the
same, but without a dedicated tool it prepares the comparison and the review
wiring itself.

The change facts are those of the real v12 tool run on the synthetic fixture
(examples/omh-v12/): first result, number 0 gone and number 3 new; fixed result,
no number added or removed, only the blank price changed. The role flow is
illustrative, not a recorded agent run. Role mapping in the notes follows the OMH
integrated v04 reference (orchestrator, fixer, oracle) as an example only.
"""

from kit import AMBER, BLUE, BLUE_SOFT, INK, INK2, PAPER2, WHITE, Svg, case_head, p

# roles inside OMO: x, width (shared y range)
ROLES = {"worker": (510, 210), "lead": (910, 210), "reviewer": (1310, 330)}
ROLE_Y, ROLE_H = 170, 296
# handoffs, one per role pair and direction; first pass and re-check share an arrow:
# (label, from, to, row y, colour, dashed, kind)
FLOWS = [
    ("맡김", "lead", "worker", 222, "blue", False, "assign"),
    ("고친 표", "worker", "lead", 310, "ink", False, "result"),
    ("다시 고침", "lead", "worker", 410, "amber", True, "return"),
    ("원본과 결과", "lead", "reviewer", 222, "blue", False, "assign"),
    ("검토 결과", "reviewer", "lead", 310, "amber", False, "evidence"),
]


def _edge(role, side):
    x, w = ROLES[role]
    return x + w if side == "right" else x


def omh_svg():
    s = Svg("s14", 120, 340, 1680, 600,
            "요청: 표의 금액 빈칸만 0으로 채우고 번호와 상품은 그대로. 왼쪽 OpenCode 순정은 전용 도구가 없으면 비교 코드, 검토 기준, "
            "다시 맡기는 연결을 직접 준비한다. 오른쪽 OMH 통합 구성 안의 OMO 역할 협업: 총괄이 기준을 정해 작업 담당에게 맡기고, "
            "원본과 결과를 검토 담당에게 비교하게 한다. 검토 담당은 준비된 비교 도구로 금액 빈칸이 0이 된 것은 요청한 변경, "
            "상품 A의 번호가 0에서 3으로 바뀐 것은 요청 밖 변경이라고 찾는다. 같은 총괄이 다시 고치게 하고, 검토를 통과한 뒤 보고한다")
    sm = {"size": 24, "weight": 400, "fill": INK2}
    s.rect(0, 0, 1680, 54, fill=PAPER2)
    s.text(24, 27, "요청", size=26, weight=800, fill=INK2)
    s.text(110, 27, "표의 금액 빈칸만 0으로 채워 줘. 번호와 상품은 그대로", size=28, weight=800)
    s.text(1656, 27, "같은 모델, 추가 학습 없음", size=26, fill=INK2, anchor="end")

    # left: bare OpenCode
    s.rect(0, 80, 440, 410, fill=WHITE, stroke=INK, sw=2.5, extra=' data-box="opencode"')
    s.text(28, 118, "OpenCode 순정", size=30, weight=800)
    s.text(28, 156, "전용 도구가 없으면", size=24, weight=800, fill=AMBER)
    s.text(28, 186, "직접 준비할 것", size=24, weight=800, fill=AMBER)
    prep = [("비교 코드", "원본과 결과를 맞춰 봄"), ("검토 기준", "번호, 상품은 그대로"), ("다시 맡기는 연결", "고칠 것을 되돌림")]
    for k, (t, d) in enumerate(prep):
        y = 236 + k * 68
        s.text(28, y, str(k + 1), size=26, weight=800, fill=INK2)
        s.text(64, y, t, size=28, weight=800)
        s.text(64, y + 32, d, size=24, fill=INK2)
    s.text(28, 444, "할 수는 있음, 직접 짜서 연결", size=24, weight=800, fill=INK2)
    s.text(28, 474, "빈칸만 세면 이 실수는 지나침", size=24, fill=AMBER)

    # right: OMH boundary, OMO role collaboration inside it
    s.rect(470, 80, 1210, 410, fill="none", stroke=BLUE, sw=4, extra=' data-box="omh"')
    s.text(498, 106, "OMH 통합 구성", size=28, weight=800, fill=BLUE)
    s.text(1652, 106, "준비된 비교 도구와 절차 포함", size=24, weight=800, fill=BLUE, anchor="end")
    s.rect(490, 128, 1170, 350, fill="none", stroke=BLUE, sw=2, dash="8 6", extra=' data-box="omo"')
    s.text(510, 150, "OMO 역할 협업", size=24, weight=800, fill=BLUE)

    lead_x, lead_w = ROLES["lead"]
    work_x, work_w = ROLES["worker"]
    rev_x, rev_w = ROLES["reviewer"]
    for role, (x, w) in ROLES.items():
        fill, stroke, sw = (BLUE_SOFT, BLUE, 3) if role == "lead" else (WHITE, INK, 2.5)
        s.rect(x, ROLE_Y, w, ROLE_H, fill=fill, stroke=stroke, sw=sw, extra=f' data-role="{role}"')
    # 작업 담당: edits the table, which looks finished
    s.text(work_x + 20, 202, "작업 담당", size=28, weight=800)
    s.text(work_x + 20, 236, "표를 고침", size=24, fill=INK2)
    s.text(work_x + 20, 326, "줄 수 3 → 3", size=24)
    s.text(work_x + 20, 358, "빈칸 1 → 0", size=24)
    s.text(work_x + 20, 390, "겉보기엔 끝", size=24, weight=800, fill=AMBER)
    # 총괄: criterion and assignment
    s.text(lead_x + 20, 202, "총괄", size=28, weight=800, fill=BLUE)
    s.text(lead_x + 20, 236, "기준, 맡김", size=24, fill=INK2)
    s.text(lead_x + 20, 326, "기준", size=24, weight=800, fill=BLUE)
    s.text(lead_x + 20, 358, "번호, 상품 유지", size=24)
    s.text(lead_x + 20, 390, "줄 추가, 삭제 0", size=24)
    # 검토 담당: compares with the prepared tool and flags the unrequested change
    s.text(rev_x + 20, 202, "검토 담당", size=28, weight=800)
    s.text(rev_x + 20, 236, "원본과 결과 비교", size=24, fill=INK2)
    s.rect(rev_x + 12, 256, rev_w - 24, 136, fill=PAPER2)
    s.text(rev_x + 24, 278, "금액 빈칸 → 0", size=24, weight=800)
    s.text(rev_x + 24, 308, "요청한 변경", size=24, weight=800, fill=BLUE)
    s.text(rev_x + 24, 342, "상품 A 번호 0 → 3", size=24, weight=800)
    s.text(rev_x + 24, 372, "요청 밖 변경", size=24, weight=800, fill=AMBER)
    s.rect(rev_x + 12, 400, rev_w - 24, 60, fill=WHITE, stroke=BLUE, sw=2, extra=' data-box="tools"')
    s.text(rev_x + 28, 416, "준비된 비교 도구", size=24, weight=700, fill=BLUE)
    s.text(rev_x + 28, 444, "data_compare", size=24, weight=700, fill=BLUE, mono=True)

    # handoffs between the roles; every arrow names its sender and receiver
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
    # report: the same 총괄, only after the review passes
    cx = lead_x + lead_w / 2
    s.arrow([(cx, ROLE_Y - 2), (cx, 58)], color="blue")
    s.parts[-1] = s.parts[-1].replace(
        "<polyline ", '<polyline data-from="lead" data-to="requester" data-kind="report" ', 1)
    s.text(cx + 16, 150, "검토 통과 뒤 보고", size=24, weight=800, fill=BLUE)

    s.rect(0, 510, 1680, 90, fill=WHITE, stroke=BLUE, sw=3)
    s.text(28, 538, "쓰는 이유", size=26, weight=800, fill=BLUE)
    s.text(190, 538, "역할을 나눠 맡기고, 준비된 비교로 요청 밖 변경을 보고 전에 확인", size=28, weight=800)
    s.text(190, 576, "OpenCode 순정도 할 수 있지만, 비교 코드와 검토 연결을 직접 준비해야 함", size=24, fill=INK2)
    return s.render()


def omh_body():
    return "\n  ".join([
        case_head(2, "OMH"),
        p("qline case-q", "<b>질문</b>OpenCode만으로도 되는 일, OMH로 하면 무엇이 달라질까?"),
        p("case-title", "빈칸만 채우랬는데, 번호까지 바뀌었다면?", "h2"),
        omh_svg(),
        p("foot", "역할 흐름은 설명용. 바뀐 내용은 합성 예시 표에 준비된 비교 도구를 실제로 실행한 결과",
          style="left:120px;top:968px;width:1680px;margin:0;color:#B45309;font-weight:700"),
    ])


OMH_NOTES = """<p><strong>장면:</strong> 요청은 '표의 금액 빈칸만 0으로 채워 줘. 번호와 상품은 그대로'입니다. 표에는 세 줄이 있습니다. 번호 0 상품 A 금액 1200, 번호 1 상품 B 금액 빈칸, 번호 2 상품 C 금액 800. 바뀌어야 할 것은 상품 B의 금액 빈칸 하나뿐입니다.</p>
<p><strong>역할 흐름 (설명용):</strong> 총괄이 요청을 받아 기준(번호와 상품은 그대로, 줄 추가와 삭제 0)을 정하고 작업 담당에게 맡깁니다. 작업 담당이 고친 표를 총괄에게 돌려줍니다. 줄 수는 3 그대로, 빈칸은 0이라 겉보기엔 끝났습니다. 총괄이 검토 담당에게 원본과 결과를 넘겨 비교를 맡깁니다. 검토 담당은 준비된 비교 도구의 결과를 읽고, 금액 빈칸이 0이 된 것은 요청한 변경이지만 상품 A의 번호가 0에서 3으로 바뀐 것은 요청 밖 변경이라고 총괄에게 알립니다. 같은 총괄이 작업 담당에게 다시 고치게 하고(호박색 점선), 고친 표를 다시 검토에 넘깁니다. 화살표 하나가 처음과 다시 확인을 함께 나타냅니다. 검토를 통과하면 그때 총괄이 요청한 사람에게 보고합니다.</p>
<p><strong>OMH를 쓰는 이유:</strong> OMH 통합 구성에는 이렇게 역할을 나눠 맡기고 결과를 돌려받는 OMO의 역할 협업과, 원본과 결과를 같은 형식으로 비교하는 도구(data_compare, data_inspect), 필요할 때 쓰는 절차(omh-rigorous)가 한 묶음으로 준비돼 있습니다. 그래서 '요청 밖 변경을 보고 전에 잡는' 검토를 이 일에 바로 붙일 수 있습니다. OMO는 OMH 경계 안에 들어 있습니다. OMH는 도구와 절차를 제공하는 묶음이지 따로 일하는 사람이 아닙니다.</p>
<p><strong>OpenCode 순정과의 차이:</strong> OpenCode 순정의 에이전트도 하위 작업을 맡기고, 스크립트로 비교하고, 기준을 프롬프트로 주면 같은 문제를 잡을 수 있습니다. 이미 만들어 둔 스크립트가 있으면 다시 쓸 수도 있습니다. 순정이 못 한다거나 늘 실패한다는 이야기가 아닙니다. 전용 도구가 없다면 비교 코드, 검토 기준, 고칠 것을 되돌리는 연결을 직접 준비해 이어 붙여야 한다는 것이 차이입니다.</p>
<p><strong>실제로 실행한 것:</strong> 바뀐 내용은 examples/omh-v12/의 합성 표(CSV 파일)에 OMH 통합 v04 묶음의 data_compare를 번호(id) 기준으로 실제로 실행한 결과입니다. 첫 결과는 원본에만 있는 번호 1개(left_only 1, 번호 0)와 결과에만 있는 번호 1개(right_only 1, 번호 3), 금액이 바뀐 줄 1개(value_changed 1, amount)였습니다. 수정 결과는 left_only 0, right_only 0, 금액 빈칸이 채워진 줄 1개만 바뀌었습니다. 비교 도구는 의도한 금액 변경도 차이로 보고하므로, 기준은 '차이 0'이 아니라 '번호 추가, 삭제 0, 금액만 변경'입니다. 도구 결과의 ok는 호출 성공이라는 뜻이지 기준 통과가 아닙니다.</p>
<p><strong>설명용인 부분:</strong> 첫 결과 표는 이 장면을 위해 손으로 만든 합성 데이터입니다. 역할 흐름은 실제 에이전트 실행 기록이 아니며, 모델이 늘 이렇게 판단한다는 뜻도, 자동으로 막는 관문이 있다는 뜻도 아닙니다.</p>
<p><strong>역할 이름:</strong> 총괄, 작업 담당, 검토 담당은 교육용 이름입니다. OMH 통합 v04 참고 문서의 역할로 옮기면 총괄은 orchestrator(작업 분해, 역할 배정, 결과 취합과 검증), 작업 담당은 fixer(한정한 수정과 지정한 검사, 재위임 없음), 검토 담당은 oracle(읽기 전용 원인 분석과 리뷰)에 가깝습니다. 이 세 역할 흐름이 늘 고정돼 있다는 뜻은 아니며, 검토 담당이 도구를 직접 실행하는 권한이나 처음부터 끝까지 실제로 돌린 기록을 말하는 것도 아닙니다. 검토 담당은 준비된 비교 결과를 읽는 역할로 그렸습니다. 모든 역할은 고른 같은 모델을 함께 쓰고, 추가 학습은 없습니다. OpenCode와 Python은 미리 설치해야 하는 전제이고 패키지에 들어 있지 않습니다.</p>
<p><strong>말하지 않는 것:</strong> 속도나 정확도 수치, 오류가 없다는 보장, 질문 횟수가 늘 준다는 주장은 하지 않습니다. 결과를 받아들일지는 여전히 사람이 결정합니다. 근거는 OMH 통합 v04 참고 문서(구성과 조건, 역할, 도구)이며 로컬 보관 자료로 이 저장소에 들어 있지 않습니다.</p>"""


def apply(orig, sl):
    if orig == 14:
        sl["body"] = omh_body()
        sl["notes"] = OMH_NOTES
