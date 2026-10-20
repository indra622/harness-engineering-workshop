"""All 35 slides for the HTML deck, keyed by the canonical v10 slide ID.

Each function draws one native SVG diagram on the shared frame. On-screen
wording is a short draft from the production brief; the full v10 text and
the brief entry go to presenter notes. Diagram coordinates are inches on a
13.333 x 7.5 stage; labels are 20 pt or larger.
"""

from deck import theme as T

from . import frame, kit

C = T.COLORS
L = T.SIZE["label"]
M = T.MARGIN
R = T.RIGHT
W = R - M

# on-screen titles that differ from the canonical v10 title (kept in notes)
SCREEN_TITLES = {26: "CEO Agent: 상황에 맞는 페르소나"}


def start(page, h, section, question, lead_tag, lead, footnote, kind=None):
    spec = dict(sid=page.sid, section=section,
                time=f"{h['start']}분부터 {h['end']}분까지, {h['minutes']}분",
                title=SCREEN_TITLES.get(page.sid, h["title"]), question=question,
                lead_tag=lead_tag, lead=lead, footnote=footnote, kind=kind)
    return frame.build(page, spec)


def tags(page, xs, w, y, labels, colors=None, bold=None, h=0.4):
    for i, (x, lab) in enumerate(zip(xs, labels)):
        kit.text(page, x, y, w, h, [[(lab, L, (bold or {}).get(i, False),
                                       (colors or {}).get(i, C["muted"]))]],
                 align="center", hint=f"tag{i}")


def chain(page, nodes, **kw):
    for a, b in zip(nodes, nodes[1:]):
        kit.arrow(page, a, b, **kw)


def hline_arrow(page, x1, x2, y, **kw):
    kit.path_arrow(page, [(x1, y), (x2, y)], **kw)


# ======================================================== 1. opening

def s01(page, h):
    y0 = start(page, h, "시작", "이 흐름이 단계를 건너뛰지 않게 하는 것은 누구일까?", "장면",
               "AI교양 글 한 편의 작업이 끝났다. 어떤 단계를 거쳤을까?",
               "비공개 초안에는 설정된 광고와 안내 이미지가 들어간다. 실제 화면과 계정 정보는 보여 주지 않는다.") + 0.3
    scope = kit.container(page, M, y0, 10.15, 2.85, hint="workflow-scope")
    kit.text(page, M + 0.2, y0 + 0.12, 4.2, 0.42, [[("이 업무 흐름의 범위", L, True, C["primary"])]],
             parent=scope.name, hint="scope-label")
    ny, nh, nw, pitch = y0 + 0.72, 1.35, 1.75, 2.0
    xs = [M + 0.2 + i * pitch for i in range(5)]
    labels = ["원문 보존\nv01, v02", "사용자\n최종 확정", "삽화 한 장\nObsidian\n보관",
              "네이버\n비공개 초안", "다시 열어\n확인"]
    styles = ["base", "gate", "base", "base", "base"]
    ns = [kit.node(page, x, ny, nw, nh, lab, style=st, parent=scope.name)
          for x, lab, st in zip(xs, labels, styles)]
    chain(page, ns)
    tags(page, xs, nw, ny + nh + 0.12, ["버전 기록", "사람이 결정", "이미지 보관", "초안 저장", "재열람 결과"],
         colors={1: C["warning"]}, bold={1: True})
    ox = 10.9
    kit.node(page, ox, ny, R - ox, nh, "공개 발행\n범위 밖", style="out", hint="publish-out")
    kit.text(page, ox, ny + nh + 0.12, R - ox, 0.4, [[("흐름에 없음", L, False, C["muted"])]],
             align="center", hint="publish-tag")


def s02(page, h):
    y0 = start(page, h, "시작", "이 워크샵 뒤에 AI교양 흐름을 용어로 다시 읽을 수 있을까?", "핵심",
               "오늘은 개념과 사례를 번갈아 본다.",
               "장면은 가상 초안이다. 참가자는 실습하지 않고 듣고 질문한다.")
    per = W / 120
    segs = [(0, 5, "intro", ""), (5, 17, "term", "용어 4"), (17, 22, "case", ""),
            (22, 31, "term", "용어 3"), (31, 36, "case", ""), (36, 45, "term", "용어 3"),
            (45, 48, "case", ""), (48, 63, "term", "용어 5"), (63, 68, "case", ""),
            (68, 78, "break", "휴식"), (78, 87, "term", "용어 3"), (87, 90, "case", ""),
            (90, 111, "term", "용어 7"), (111, 115, "synth", ""), (115, 120, "qa", "")]
    by, bh = y0 + 0.6, 0.62
    style = {"intro": "chip", "term": "focus", "case": "solid", "break": "out", "synth": "solid",
             "qa": "chip"}
    for a, b, kind, lab in segs:
        x, w = M + a * per, (b - a) * per
        kit.node(page, x, by, w, bh, lab, style=style[kind], radius=0.02,
                 hint=f"seg{a}")
    cases = [(17, 22, "OpenClaw"), (31, 36, "OMH"), (45, 48, "Grokbot"), (63, 68, "AI교양"),
             (87, 90, "CEO Agent"), (111, 115, "종합")]
    for a, b, name in cases:
        cx = M + (a + b) / 2 * per
        w = kit.width_in(name, L, True) + 0.2
        kit.text(page, cx - w / 2, by - 0.48, w, 0.42, [[(name, L, True, C["primary"])]],
                 align="center", hint=f"case-{name}")
    for minute in (0, 30, 60, 90, 120):
        x = M + minute * per
        w = 1.0
        xx = min(max(x - w / 2, M), R - w)
        kit.text(page, xx, by + bh + 0.06, w, 0.4,
                 [[(f"{minute}분", L, False, C["muted"])]], align="center", hint=f"tick{minute}")
    kit.text(page, M, by + bh + 0.5, 8.0, 0.4,
             [[("120분 진행 순서.  짙은 칸: 사례,  옅은 칸: 용어", L, False, C["muted"])]], hint="legend")
    cy = y0 + 2.62
    kit.text(page, M, cy, 1.6, 0.82, [[("반복 장면", L, True, C["ink"])]], hint="scenes-label")
    chips = ["회의 준비", "메일 초안\n(발송 없음)", "문서 검토", "파일 찾기와\n인계", "주간 요약"]
    cw = (R - 2.2 - 4 * 0.14) / 5
    for i, lab in enumerate(chips):
        kit.node(page, 2.2 + i * (cw + 0.14), cy, cw, 0.82, lab, style="plain")


# ======================================================== 2. execution basics

def s03(page, h):
    y0 = start(page, h, "용어   실행 틀의 기본", "안건을 모르는데도 그럴듯한 준비안이 나올까?", "정의",
               "모델은 입력으로 다음 출력을 계산한다.",
               "결과는 가상 예시다. 같은 모델이라도 입력이 다르면 출력이 달라진다.")
    ra, rb, nh = y0 + 0.15, y0 + 1.6, 0.9
    a = kit.node(page, M, ra, 3.6, nh, "요청 A\n회의 준비해 줘")
    b = kit.node(page, M, rb, 3.6, nh, "요청 B\n+ 안건 세 줄", style="base")
    model = kit.node(page, 5.25, y0 + 0.15, 2.5, 2.35, "같은\n모델", style="focus", size=24)
    kit.node(page, 5.25, y0 + 2.7, 2.5, 0.82, "파일은 여기서\n열리지 않는다", style="note")
    oa = kit.node(page, 9.4, ra, R - 9.4, nh, "결과 A (가상)\n일반 회의 목록")
    ob = kit.node(page, 9.4, rb, R - 9.4, nh, "결과 B (가상)\n안건 반영 목록", style="focus")
    for n, o in ((a, oa), (b, ob)):
        y = n.y + n.h / 2
        kit.path_arrow(page, [(n.x + n.w, y), (model.x, y)], src=n, dst=model)
        kit.path_arrow(page, [(model.x + model.w, y), (o.x, y)], src=model, dst=o)
    kit.text(page, M, y0 + 2.7, 4.4, 0.82,
             [[("입력", L, True, C["primary"])], [("모델이 볼 수 있는 것", L, False, C["muted"])]],
             hint="col-in")
    kit.text(page, 9.4, y0 + 2.7, R - 9.4, 0.82,
             [[("출력", L, True, C["primary"])], [("다음 텍스트 또는 도구 요청", L, False, C["muted"])]],
             hint="col-out")


def s04(page, h):
    y0 = start(page, h, "용어   실행 틀의 기본", "확인과 수정을 끝나는 조건이 있는 반복으로 돌리면 에이전트일까?", "정의",
               "목표, 행동, 결과 확인, 종료 조건이 도는 구성이다.",
               "한 번에 끝났는지가 아니라, 결과를 보고 다음 행동을 고를 수 있는 구조인지가 핵심이다.")
    kit.node(page, 3.3, y0, 6.0, 0.55, "목표: 일정 안내 메일 초안 완성 (발송 없음)", style="chip",
             hint="goal")
    nw, nh = 2.3, 0.7
    j = kit.node(page, 3.3, y0 + 0.95, nw, nh, "모델 판단")
    t = kit.node(page, 7.0, y0 + 0.95, nw, nh, "도구 실행")
    r = kit.node(page, 7.0, y0 + 2.45, nw, nh, "결과 확인")
    e = kit.node(page, 3.3, y0 + 2.45, nw, nh, "종료 조건?", style="focus")
    kit.arrow(page, j, t)
    kit.arrow(page, t, r, sa="bottom", sb="top")
    kit.arrow(page, r, e, sa="left", sb="right")
    kit.arrow(page, e, j, sa="top", sb="bottom", color="primary", width=2.0)
    kit.text(page, 4.55, y0 + 1.85, 1.9, 0.4, [[("아니오: 다시", L, True, C["primary"])]],
             hint="no-label")
    done = kit.node(page, M, y0 + 2.45, 2.1, nh, "종료: 초안", hint="done")
    kit.arrow(page, e, done, sa="left", sb="right")
    kit.text(page, 2.6, y0 + 2.0, 0.7, 0.4, [[("예", L, True, C["ink"])]], align="center",
             hint="yes-label")
    kit.node(page, 10.1, y0 + 1.6, R - 10.1, 0.82, "메일 발송\n루프 밖", style="out", hint="send-out")


def s05(page, h):
    y0 = start(page, h, "용어   실행 틀의 기본", "AI 모델이 파일을 직접 열까?", "정의",
               "모델은 요청만 만들고, 런타임이 실행해 결과를 돌려준다.",
               "여기서 런타임은 Python이나 Node.js 같은 언어 실행 환경이 아니다. 흐름은 가상 예시다.")
    lane_h, gap = 1.1, 0.1
    lanes = [("모델", "lane", False), ("런타임", "lane_focus", True), ("도구와\n파일", "lane", False)]
    ly = []
    for k, (name, style, focus) in enumerate(lanes):
        y = y0 + k * (lane_h + gap)
        ly.append(y)
        b = kit.band(page, M, y, W, lane_h, style=style, hint=f"lane{k}")
        kit.text(page, M + 0.15, y, 1.45, lane_h,
                 kit.runs_of(name, L, True, C["primary"] if focus else C["ink"]),
                 parent=b.name, hint=f"lane-label{k}")
    x0, pitch, nw, nh = 2.2, 1.77, 1.47, 0.82
    plan = [(0, 0, "1. 요청\nread_file", "base"), (1, 1, "2. 권한\n확인", "focus"),
            (2, 1, "3. 도구\n호출", "focus"), (3, 2, "4. 파일\n읽기", "base"),
            (4, 1, "5. 결과\n정리", "focus"), (5, 0, "6. 다음\n판단", "base")]
    ns = [kit.node(page, x0 + c * pitch, ly[ln] + (lane_h - nh) / 2, nw, nh, lab, style=st)
          for c, ln, lab, st in plan]
    kit.arrow(page, ns[0], ns[1], elbow=True)
    kit.arrow(page, ns[1], ns[2])
    kit.arrow(page, ns[2], ns[3], elbow=True)
    kit.arrow(page, ns[3], ns[4], elbow=True)
    kit.arrow(page, ns[4], ns[5], elbow=True)
    kit.node(page, 4.2, ly[0] + 0.25, 6.3, 0.6, "모델 쪽에서는 파일이 열리지 않는다", style="note")
    kit.node(page, 9.45, ly[2] + 0.12, 3.2, 0.86, "오류(파일 없음)도\n같은 길로 돌아온다", style="note")


def s06(page, h):
    y0 = start(page, h, "용어   실행 틀의 기본", "체크리스트 파일이 폴더에 있으면 검토 틀이 갖춰질까?", "정의",
               "컨텍스트, 도구, 실행 위치, 상태, 검증을 묶은 작업 틀이다.",
               "하네스의 범위는 제품마다 다를 수 있다. 이 워크샵의 작업 정의를 쓴다.")
    outer = kit.container(page, M, y0, 7.9, 3.5, hint="harness")
    kit.text(page, M + 0.2, y0 + 0.06, 4.0, 0.42, [[("하네스: 작업 틀 전체", L, True, C["primary"])]],
             parent=outer.name, hint="harness-label")
    mid = kit.container(page, 2.75, y0 + 0.95, 3.4, 1.75, style="retained", hint="runtime")
    kit.text(page, 2.75, y0 + 1.0, 3.4, 0.42, [[("런타임 (실행 연결)", L, False, C["ink"])]],
             align="center", parent=mid.name, hint="runtime-label")
    kit.node(page, 3.6, y0 + 1.55, 1.7, 0.7, "모델", style="focus", parent=mid.name, size=24)
    comps = [(0.75, 0.6, "컨텍스트"), (6.4, 0.6, "도구"), (0.75, 2.85, "실행 위치"),
             (3.55, 2.85, "검증"), (6.4, 2.85, "상태")]
    for x, dy, lab in comps:
        kit.node(page, x, y0 + dy, 1.8, 0.5, lab, style="plain", parent=outer.name)
    kit.text(page, 8.8, y0, R - 8.8, 0.42, [[("검토 장면에 대입 (가상)", L, True, C["ink"])]],
             hint="map-title")
    rows = ["컨텍스트: rules.md", "도구: 파일 읽기", "상태: handoff.md", "검증: checklist.md",
            "모델: 그대로, 재학습 없음"]
    for i, lab in enumerate(rows):
        kit.node(page, 8.8, y0 + 0.5 + i * 0.6, R - 8.8, 0.5, lab, style="retained" if i == 4
                 else "chip", align="left")


# ======================================================== 3. case: OpenClaw

def s07(page, h):
    y0 = start(page, h, "사례   OpenClaw", "이 요청을 받는 쪽, 맡기는 쪽, 확인하는 쪽은 각각 누구일까?", "핵심",
               "요청은 세션을 거쳐 코디네이터가 처리하거나 워커에 맡긴다.",
               "위임 기준은 운영 지침이며 자동 라우터가 아니다. 원격 앱은 두 번째 작성자가 아니다.")
    my, nh, nw = y0 + 1.1, 0.82, 1.75
    req = kit.node(page, M, my, 1.55, nh, "요청\n디스코드 등")
    gw = kit.node(page, 2.35, my, nw, nh, "게이트웨이\n와 세션")
    co = kit.node(page, 4.45, my, nw, nh, "코디네이터", style="focus")
    tool = kit.node(page, 6.65, y0, nw, nh, "직접 도구")
    wk = kit.node(page, 6.65, y0 + 2.2, nw, nh, "원격 워커", style="focus")
    proj = kit.node(page, 8.85, my, nw, nh, "프로젝트\n파일, 테스트")
    ver = kit.node(page, 11.05, my, R - 11.05, nh, "부모 검증", style="gate")
    rep = kit.node(page, 11.05, y0 + 2.2, R - 11.05, nh, "답장")
    kit.arrow(page, req, gw)
    kit.arrow(page, gw, co)
    kit.arrow(page, co, tool, elbow=True)
    kit.arrow(page, co, wk, elbow=True)
    kit.arrow(page, tool, proj, elbow=True)
    kit.arrow(page, wk, proj, elbow=True)
    kit.arrow(page, proj, ver)
    kit.arrow(page, ver, rep, sa="bottom", sb="top")
    kit.text(page, 4.45, my + nh + 0.08, nw, 0.4, [[("에이전트", L, True, C["primary"])]],
             align="center", hint="tag-agent")
    kit.text(page, 6.65, y0 + nh + 0.06, nw, 0.4, [[("런타임 실행", L, True, C["primary"])]],
             align="center", hint="tag-runtime")
    kit.text(page, 6.5, y0 + 2.2 - 0.46, 2.05, 0.4, [[("모델 + 런타임", L, True, C["primary"])]],
             align="center", hint="tag-model")
    kit.node(page, M, y0 + 2.2, 1.55, nh, "하네스 =\n전체 틀", style="note", hint="harness-note",
             paragraphs=[[("하네스 =", L, True, C["primary"])], [("전체 틀", L, False, C["muted"])]])
    kit.node(page, 2.35, y0 + 2.2, nw, nh, "세션, 워커는\nS23, S24", style="note",
             hint="preview")
    kit.node(page, 8.85, y0 + 2.2, nw, nh, "원격 앱\n보기와 개입", style="out", hint="remote-app")
    kit.line(page, [(8.85, y0 + 2.2 + nh / 2), (6.65 + nw, y0 + 2.2 + nh / 2)])


# ======================================================== 4. roles, tools, skills

def s08(page, h):
    y0 = start(page, h, "용어   역할, 도구, 스킬", "맡는 사람이 정해지지 않으면 같은 일을 두 번 하게 될까?", "정의",
               "누가 언제 무엇을 맡을지 정하는 조율이다.",
               "전환 조건 예: 안건 확정 뒤 초안, 초안 저장 뒤 체크, 기준 미달이면 고치기. 독립 검토가 아니다.")
    lane_h, gap = 1.1, 0.1
    names = ["기획", "실행", "검토"]
    ly = []
    for k, name in enumerate(names):
        y = y0 + k * (lane_h + gap)
        ly.append(y)
        b = kit.band(page, M, y, W, lane_h, style="lane", hint=f"lane{k}")
        kit.text(page, M + 0.15, y, 1.4, lane_h, kit.runs_of(name, L, True, C["ink"]),
                 parent=b.name, hint=f"lane-label{k}")
    x0, pitch, nw, nh = 2.1, 2.15, 1.8, 0.7
    plan = [(0, 0, "안건 정하기", "base"), (1, 1, "초안 쓰기", "base"), (2, 2, "체크하기", "focus"),
            (3, 1, "고치기", "base"), (4, 2, "다시 체크", "focus")]
    ns = [kit.node(page, x0 + c * pitch, ly[ln] + (lane_h - nh) / 2, nw, nh, lab, style=st)
          for c, ln, lab, st in plan]
    for a, b in zip(ns, ns[1:]):
        kit.arrow(page, a, b, elbow=True)


def s09(page, h):
    y0 = start(page, h, "용어   역할, 도구, 스킬", "목록을 가져오는 기능과 찾는 순서 메모 중 무엇이 실행될까?", "정의",
               "모델이 요청하고 런타임이 실행하는, 형식이 정해진 기능이다.",
               "날짜 형식을 바꾸라는 문장은 절차다. 그 일을 실제로 수행하는 호출이 도구다.")
    card = kit.container(page, M, y0, 5.8, 1.95, style="tile", hint="tool-card")
    kit.text(page, M + 0.2, y0 + 0.05, 5.4, 0.42, [[("도구 정의", L, True, C["primary"])]],
             parent=card.name, hint="card-title")
    rows = [("이름", "list_files"), ("입력", "folder, sort"), ("결과", "파일 목록 또는 오류")]
    for i, (k, v) in enumerate(rows):
        kit.text(page, M + 0.2, y0 + 0.5 + i * 0.46, 5.4, 0.42,
                 [[(f"{k}   ", L, True, C["muted"]), (v, L, False, C["ink"])]],
                 parent=card.name, hint=f"card-row{i}")
    memo = kit.container(page, 6.9, y0, R - 6.9, 1.95, style="note", hint="memo")
    kit.text(page, 7.1, y0 + 0.05, 5.5, 0.42, [[("메모: 찾는 순서", L, True, C["muted"])]],
             parent=memo.name, hint="memo-title")
    kit.text(page, 7.1, y0 + 0.5, 5.5, 0.84,
             [[("1. 회의 폴더를 연다", L, False, C["muted"])], [("2. 날짜순으로 본다", L, False, C["muted"])]],
             parent=memo.name, hint="memo-body")
    kit.text(page, 7.1, y0 + 1.42, 5.5, 0.42, [[("실행되지 않는 절차", L, True, C["warning"])]],
             parent=memo.name, hint="memo-tag")
    call = kit.node(page, M, y0 + 2.55, 5.8, 0.9, "", hint="call",
                    paragraphs=[[("호출 (모델의 요청)", L, True, C["primary"])],
                                [("list_files(folder=meetings)", L, False, C["ink"])]])
    res = kit.node(page, 6.9, y0 + 2.55, R - 6.9, 0.9, "", style="focus", hint="result",
                   paragraphs=[[("결과 (가상)", L, True, C["primary"])],
                               [("memo-1014.md, memo-1021.md", L, False, C["ink"])]])
    kit.arrow(page, call, res)
    kit.arrow(page, card, call, sa="bottom", sb="top")
    kit.text(page, M + 3.0, y0 + 2.0, 2.6, 0.4, [[("모델이 고름", L, False, C["muted"])]],
             hint="pick")


def s10(page, h):
    y0 = start(page, h, "용어   역할, 도구, 스킬", "매주 다시 쓸 수 있도록 순서를 묶어 둔 것은 무엇일까?", "정의",
               "절차, 입력과 출력 규칙, 자원을 묶은 재사용 지침이다.",
               "이 워크샵에서 스킬을 설치하지 않는다. 포장과 호출 방식은 도구마다 다르다.")
    tree = kit.container(page, M, y0, 6.1, 3.45, style="tile", hint="skill-tree")
    kit.text(page, M + 0.2, y0 + 0.05, 5.7, 0.42, [[("스킬 폴더 (가상 예시)", L, True, C["primary"])]],
             parent=tree.name, hint="tree-title")
    lines = [("report-skill/", "", True), ("  절차.md", "언제, 어떤 순서로", False),
             ("  checklist.md", "확인 기준", False), ("  schema.md", "출력 형식", False),
             ("  scripts/", "선택", False)]
    for i, (a, b, bold) in enumerate(lines):
        runs = [(a, L, bold, C["ink"])]
        if b:
            runs.append((f"   {b}", L, False, C["muted"]))
        kit.text(page, M + 0.25, y0 + 0.55 + i * 0.55, 5.7, 0.45, [runs], parent=tree.name,
                 hint=f"tree{i}")
    sk = kit.node(page, 7.4, y0, R - 7.4, 0.95, "스킬: 읽히는 절차\n스스로 실행되지 않음", style="focus",
                  hint="skill")
    tl = kit.node(page, 7.4, y0 + 2.45, R - 7.4, 0.95, "도구: 실제 실행\n파일 읽기, 명령", hint="tool")
    kit.path_arrow(page, [(12.45, sk.y + sk.h), (12.45, tl.y)], color="primary", width=2.0,
                   src=sk, dst=tl)
    kit.text(page, 7.5, y0 + 1.42, 4.7, 0.42, [[("런타임이 도구를 호출", L, True, C["primary"])]],
             hint="call-label")
    kit.path_arrow(page, [(M + 6.1, y0 + 2.9), (7.4, y0 + 2.9)], color="muted", dash=True)


# ======================================================== 5. case: OMH

def s11(page, h):
    y0 = start(page, h, "사례   OMH", "모델만 더 좋은 것으로 바꾸면 이 일이 해결될까?", "핵심",
               "기존 모델과 역할은 유지하고, 업무 도구와 작업 절차를 보강했다.",
               "모의, 오프라인 점검은 실제 사내 모델 품질을 보여 주지 않는다. CSV 흐름은 가상 예시다.")
    x1, w1, x2, w2, x3 = M, 2.35, 3.2, 6.6, 10.15
    w3 = R - x3
    for x, w, head in [(x1, w1, "실제 제약"), (x2, w2, "기반은 유지, 도구와 절차는 보강"),
                       (x3, w3, "증거와 한계")]:
        kit.text(page, x, y0, w, 0.4, [[(head, L, True, C["ink"])]], hint="head")
    cy = y0 + 0.5
    for i, lab in enumerate(["오프라인 설치만", "로컬 파일만", "설정된 모델 하나"]):
        kit.node(page, x1, cy + i * 0.75, w1, 0.6, lab, style="chip")
    box = kit.container(page, x2, cy, w2, 1.05, style="scope", hint="added")
    cw = 2.04
    for i, lab in enumerate(["data_inspect\n구조 점검", "data_compare\n키 기준 비교", "선택형 절차\npstack 일부"]):
        kit.node(page, x2 + 0.12 + i * (cw + 0.1), cy + 0.13, cw, 0.79, lab, parent=box.name)
    kit.node(page, x2, cy + 1.15, w2, 0.45, "OpenCode + OMO 기존 역할 (유지)", style="retained")
    kit.node(page, x2, cy + 1.65, w2, 0.45, "설정된 단일 모델 (유지, 재학습 없음)", style="retained")
    kit.node(page, x3, cy, w3, 0.55, "설치와 점검 기록")
    kit.node(page, x3, cy + 0.65, w3, 0.55, "모의 환경 테스트")
    kit.node(page, x3, cy + 1.3, w3, 0.8, "사내 모델 품질\n미검증", style="caution")
    hline_arrow(page, x1 + w1 + 0.04, x2 - 0.04, cy + 1.05)
    hline_arrow(page, x2 + w2 + 0.04, x3 - 0.04, cy + 1.05)
    ry = cy + 2.37
    kit.text(page, M, ry, 1.45, 0.55, [[("가상 예시", L, True, C["muted"])]], hint="csv-tag")
    sn = [kit.node(page, 2.0 + i * 2.75, ry, 2.3, 0.55, lab, style="focus" if i in (1, 3) else "base")
          for i, lab in enumerate(["새 CSV", "구조 점검", "변경", "키 기준 비교"])]
    chain(page, sn)


# ======================================================== 6. extension parts

def s12(page, h):
    y0 = start(page, h, "용어   확장 부품", "이 묶음을 설치하면 계정 연결까지 끝난 것으로 봐도 될까?", "정의",
               "여러 기능과 지침을 한 번에 배포하는 포장 단위다.",
               "포장 구조와 이름은 제품마다 다르다. 플러그인은 MCP와 같은 층이 아니다.")
    pkg = kit.container(page, M, y0, 6.4, 3.4, hint="package")
    kit.text(page, M + 0.2, y0 + 0.06, 6.0, 0.42, [[("플러그인 (배포 묶음, 버전)", L, True, C["primary"])]],
             parent=pkg.name, hint="pkg-label")
    for i, lab in enumerate(["스킬", "도구\n설정", "커넥터\n설정"]):
        kit.node(page, M + 0.25 + i * 2.02, y0 + 0.8, 1.85, 1.3, lab, parent=pkg.name)
    kit.text(page, M + 0.25, y0 + 2.4, 5.9, 0.42, [[("설치 = 포장을 가져온다", L, False, C["muted"])]],
             parent=pkg.name, hint="install-note")
    host = kit.node(page, 8.0, y0, R - 8.0, 0.82, "호스트 앱\n설치됨", style="focus")
    hline_arrow(page, M + 6.4 + 0.04, 8.0 - 0.04, y0 + 0.41)
    kit.text(page, 8.0, y0 + 1.05, R - 8.0, 0.4, [[("설치 뒤에 따로 확인", L, True, C["ink"])]],
             hint="after")
    a1 = kit.node(page, 8.0, y0 + 1.55, R - 8.0, 0.6, "계정 인증: 별도 단계", style="caution")
    kit.node(page, 8.0, y0 + 2.3, R - 8.0, 0.6, "권한 허용: 별도 단계", style="caution")
    del host, a1


def s13(page, h):
    y0 = start(page, h, "용어   확장 부품", "AI가 캘린더를 바로 읽을 수 있을까?", "정의",
               "외부 서비스와 연결하는 지점이며, 인증과 권한 범위를 가진다.",
               "목록에 보이는 것과 호출이 성공하는 것은 다르다. 결과로 확인한다. 외부 조회는 하지 않는다.")
    left = kit.node(page, M, y0 + 0.45, 2.5, 1.2, "모델과\n런타임")
    br = kit.container(page, 3.7, y0, 5.4, 2.1, style="scope", hint="connector")
    kit.text(page, 3.9, y0 + 0.05, 5.0, 0.42, [[("커넥터", L, True, C["primary"])]],
             parent=br.name, hint="conn-label")
    for i, lab in enumerate(["연결 설정", "인증 (계정)", "권한 범위"]):
        kit.node(page, 3.95 + i * 1.72, y0 + 0.6, 1.58, 1.2, lab.replace(" (", "\n("),
                 style="focus" if i else "base", parent=br.name)
    right = kit.node(page, 10.3, y0 + 0.45, R - 10.3, 1.2, "외부 서비스\n캘린더 (가상)")
    hline_arrow(page, M + 2.5 + 0.04, 3.7 - 0.04, y0 + 1.05, src=left)
    hline_arrow(page, 3.7 + 5.4 + 0.04, 10.3 - 0.04, y0 + 1.05, dst=right)
    kit.text(page, 9.12, y0 + 0.55, 1.15, 0.4, [[("호출", L, True, C["ink"])]], align="center",
             hint="call")
    kit.node(page, M, y0 + 2.55, 6.0, 0.7, "연결과 권한이 있음: 일정 목록", style="focus")
    kit.node(page, 6.83, y0 + 2.55, 6.0, 0.7, "연결이나 권한이 없음: 오류", style="caution")


def s14(page, h):
    y0 = start(page, h, "용어   확장 부품", "도구마다 따로 약속을 만들어야 할까, 공통 약속이면 될까?", "정의",
               "도구와 자원을 주고받는 통신 규약이다.",
               "로컬 함수나 명령은 MCP 없이도 도구가 된다. 특정 제품의 지원 여부는 주장하지 않는다.")
    host = kit.node(page, M, y0, 2.6, 3.0, "호스트 앱", style="base", size=24)
    srv = kit.node(page, 10.23, y0, R - 10.23, 3.0, "MCP 서버\n도구, 자원", style="focus", size=24)
    rows = [("목록 조회", "도구 목록"), ("도구 호출", "결과"), ("자원 읽기", "내용")]
    xa, xb = M + 2.6 + 0.08, 10.23 - 0.08
    for i, (req, res) in enumerate(rows):
        yc = y0 + 0.5 + i * 1.0
        kit.text(page, xa + 0.1, yc - 0.5, 3.2, 0.4, [[(f"요청: {req}", L, False, C["ink"])]],
                 hint=f"req{i}")
        kit.text(page, xb - 3.3, yc - 0.5, 3.2, 0.4, [[(f"응답: {res}", L, False, C["primary"])]],
                 align="right", hint=f"res{i}")
        kit.path_arrow(page, [(xa, yc - 0.04), (xb, yc - 0.04)])
        kit.path_arrow(page, [(xb, yc + 0.14), (xa, yc + 0.14)], color="primary")
    kit.node(page, xa, y0 + 3.0, xb - xa, 0.5, "규약을 따른다고 접근 권한이 생기지는 않는다",
             style="caution")
    del host, srv


# ======================================================== 7. case: Grokbot

def s15(page, h):
    y0 = start(page, h, "사례   Grokbot", "우리 팀에도 이런 구조가 맞을까?", "핵심",
               "역할별 봇과 공유 환경의 패턴만 비교한다.",
               "첨부 자료를 열지 못해 설명 요약만 쓴다. 구조와 성능 수치는 확인하지 않았다.")
    bw, bh = 2.2, 0.7
    xl, xr = 2.4, 8.75
    center = kit.node(page, 5.15, y0 + 0.1, 3.0, 2.2, "공유 환경\n커넥터, 루틴", style="out")
    for x, y, lab in [(xl, y0 + 0.25, "역할 봇 A"), (xr, y0 + 0.25, "역할 봇 B"),
                      (xl, y0 + 1.45, "역할 봇 C"), (xr, y0 + 1.45, "역할 봇 D")]:
        b = kit.node(page, x, y, bw, bh, lab, style="out")
        yy = y + bh / 2
        if x < center.x:
            kit.line(page, [(b.x + b.w, yy), (center.x, yy)])
        else:
            kit.line(page, [(b.x, yy), (center.x + center.w, yy)])
    kit.node(page, 4.45, y0 + 2.45, 4.4, 0.42, "사용자 설명, 출처 검증 대기", style="caution")
    kit.text(page, M, y0 + 3.0, 1.4, 0.5, [[("비교 축", L, True, C["ink"])]], hint="axes-label")
    for i, lab in enumerate(["책임", "실행 위치", "상태 위치", "사람 개입"]):
        kit.node(page, 2.0 + i * 2.72, y0 + 3.0, 2.5, 0.5, lab, style="chip")


# ======================================================== 8. inputs and limits

def s16(page, h):
    y0 = start(page, h, "용어   입력과 한계", "한 줄 요청과 안건을 넣은 요청 중 어느 쪽이 결과를 더 좌우할까?", "정의",
               "지시와 제약을 담은 입력의 일부이며, 지속 지침일 수도 있다.",
               "규칙 파일이 폴더에 있다고 입력에 들어간 것은 아니다. 읽혔는지 확인한다.")
    kit.text(page, M, y0, 4.0, 0.4, [[("전", L, True, C["muted"])]], hint="before-label")
    before = kit.node(page, M, y0 + 0.45, 4.0, 0.8, "회의 준비해 줘", hint="before")
    kit.node(page, M, y0 + 1.6, 4.0, 0.82, "지속 지침 파일도\n프롬프트의 일부가 된다", style="note")
    kit.text(page, 5.6, y0, 4.0, 0.4, [[("후", L, True, C["primary"])]], hint="after-label")
    lines = [("회의 준비해 줘", C["ink"]), ("+ 안건 세 줄", C["primary"]), ("+ 참석자", C["primary"]),
             ("+ 지난 결정 (회의록 읽기 지시)", C["primary"]), ("+ 출력 형식: 안건별 목록", C["primary"])]
    after = kit.node(page, 5.6, y0 + 0.45, R - 5.6, 2.0, "", style="focus", align="left",
                     hint="after", paragraphs=[[(t, L, False, c)] for t, c in lines])
    hline_arrow(page, M + 4.0 + 0.05, 5.6 - 0.05, before.y + before.h / 2, src=before, dst=after)
    kit.band(page, M, y0 + 2.75, W, 0.6, style="lane",
             paragraphs=[[("같은 모델, 다른 입력. 입력에 없는 사실은 여전히 확인이 필요하다.", L, False, C["ink"])]],
             hint="same-model")


def s17(page, h):
    y0 = start(page, h, "용어   입력과 한계", "AI는 지난 회의의 결정을 떠올릴 수 있을까?", "정의",
               "이번 호출에 실제로 들어간 입력 전체가 컨텍스트다.",
               "읽힌 내용은 근거가 될 뿐 정답을 보장하지 않는다. 출력은 가상 예시다.")
    panels = [
        (M, "요청만 보냈을 때", C["ink"], [("요청 한 줄", "chip"), ("파일 경로만", "note")],
         ("회의록 파일 (디스크)", "읽히지 않음", "out"), "출력 (예시)\n일반 목록", "base"),
        (6.88, "회의록을 명시적으로 읽혔을 때", C["primary"],
         [("요청 한 줄", "chip"), ("안건과 참석자", "chip"), ("지난 결정 (회의록)", "focus")],
         ("회의록 파일 (디스크)", "명시적으로 읽음", "base"), "출력 (예시)\n결정을 반영한\n준비안", "focus"),
    ]
    for px, head, hcol, chips, disk, out, ost in panels:
        kit.text(page, px, y0, 5.95, 0.4, [[(head, L, True, hcol)]], hint="panel-head")
        by, bh = y0 + 0.5, 1.97
        box = kit.container(page, px, by, 3.55, bh, hint="context")
        kit.text(page, px + 0.15, by + 0.05, 3.25, 0.38, [[("이번 호출의 컨텍스트", L, True, C["primary"])]],
                 parent=box.name, hint="context-label")
        for i, (lab, st) in enumerate(chips):
            kit.node(page, px + 0.2, by + 0.45 + i * 0.5, 3.15, 0.42, lab, style=st, parent=box.name)
        name, state, dst = disk
        scol = C["primary"] if dst == "base" else C["muted"]
        dnode = kit.node(page, px, by + bh + 0.28, 3.55, 0.8, "", style=dst, hint="disk",
                         paragraphs=[[(name, L, False, C["ink"] if dst == "base" else C["muted"])],
                                     [(state, L, True, scol)]])
        if dst == "base":
            kit.arrow(page, dnode, box, sa="top", sb="bottom", color="primary", width=2.25)
        onode = kit.node(page, px + 3.85, by + (bh - 1.3) / 2, 2.1, 1.3, out, style=ost)
        kit.arrow(page, box, onode)


def s18(page, h):
    y0 = start(page, h, "용어   입력과 한계", "두 메일의 글자 수가 같으면 토큰 수도 같을까?", "정의",
               "모델이 세는 텍스트 조각의 단위이며, 단어 수와 다르다.",
               "칸 나누기는 개념 예시이며 실제 분할이 아니다. 토큰 수와 언어별 비율은 추정하지 않는다.")
    rows = [("한국어 예시", ["회의", "일정을", "다시", "안내", "드립", "니다"]),
            ("영어 예시", ["We", "will", "re", "send", "the", "sched", "ule"])]
    for r, (label, parts) in enumerate(rows):
        y = y0 + 0.2 + r * 1.05
        kit.text(page, M, y, 1.9, 0.62, [[(label, L, True, C["ink"])]], hint=f"row{r}")
        x = 2.6
        for i, p in enumerate(parts):
            w = max(0.62, kit.width_in(p, L) + 0.3)
            kit.node(page, x, y, w, 0.62, p, style="focus" if i % 2 == 0 else "chip",
                     radius=0.04)
            x += w + 0.08
    kit.text(page, 2.6, y0 + 2.25, 4.0, 0.4, [[("조각 수는 다를 수 있다", L, True, C["primary"])]],
             hint="diff")
    kit.node(page, 2.6, y0 + 2.75, 9.2, 0.62, "정확한 수는 그 모델이 제공하는 계산 방식으로 확인한다",
             style="note")


def s19(page, h):
    y0 = start(page, h, "용어   입력과 한계", "문서 전체가 한 번에 들어가고, 앞부분도 끝까지 남을까?", "정의",
               "한 호출에서 다룰 수 있는 입력과 출력의 한계다.",
               "창 크기 수치는 쓰지 않는다. 실제 도구에서 확인한다.")
    kit.text(page, M, y0, 8.0, 0.42, [[("한 호출의 창 (크기는 제품마다 다름)", L, True, C["ink"])]],
             hint="window-label")
    bar = kit.container(page, M, y0 + 0.5, 10.3, 1.0, style="scope", hint="window", radius=0.05)
    segs = [("지시", 1.2, "chip"), ("규칙 파일", 1.9, "chip"), ("문서 앞부분", 2.5, "chip"),
            ("이전 대화", 2.1, "chip"), ("출력 공간", 2.2, "focus")]
    x = M + 0.08
    seg_nodes = []
    for lab, w, st in segs:
        seg_nodes.append(kit.node(page, x, y0 + 0.62, w, 0.76, lab, style=st, parent=bar.name,
                                  radius=0.03))
        x += w + 0.06
    kit.node(page, 11.05, y0 + 0.5, R - 11.05, 1.0, "넘친 부분\n문서 뒷부분", style="out")
    kit.text(page, 9.6, y0 + 1.55, 1.3, 0.4, [[("한계", L, True, C["ink"])]], align="center",
             hint="limit")
    conv = seg_nodes[3]
    comp = kit.node(page, 4.1, y0 + 2.3, 4.0, 0.9, "압축: 이전 대화 요약\n세부 일부 손실 가능", style="note")
    kit.path_arrow(page, [(conv.x + conv.w / 2, conv.y + conv.h + 0.14),
                          (conv.x + conv.w / 2, comp.y)], color="muted", dash=True, dst=comp)
    kit.node(page, 8.5, y0 + 2.3, R - 8.5, 0.9, "대안: 장별로 나눠 넣고\n메모는 따로 저장")


def s20(page, h):
    y0 = start(page, h, "용어   입력과 한계", "새 대화를 열면 어제의 결정이 자동으로 따라올까?", "정의",
               "나중에 다시 읽을 수 있게 저장된 정보이며, 재학습이 아니다.",
               "세션 복원이나 메모리 검색 방식은 제품마다 다르다. 실제로 읽혔는지 확인한다.")
    ry, rh = y0 + 0.3, 1.0
    a = kit.node(page, M, ry, 2.4, rh, "어제 세션\n결정: 회의 날짜")
    s = kit.node(page, 3.7, ry, 2.6, rh, "저장소\n인계 파일, 노트", style="focus")
    c = kit.node(page, 7.1, ry, 2.4, rh, "오늘 호출의\n컨텍스트")
    o = kit.node(page, 10.3, ry, R - 10.3, rh, "결정 반영\n답변 (가상)")
    chain(page, [a, s, c, o])
    kit.text(page, 2.9, ry - 0.02, 0.8, 0.4, [[("저장", L, False, C["muted"])]], align="center",
             hint="save")
    kit.text(page, 6.3, ry - 0.02, 0.8, 0.4, [[("읽기", L, True, C["primary"])]], align="center",
             hint="read")
    miss = kit.node(page, 7.1, y0 + 1.75, 2.4, 0.82, "읽지 않으면\n결정을 모름", style="out")
    miss_o = kit.node(page, 10.3, y0 + 1.75, R - 10.3, 0.82, "모른다는 답", style="out")
    kit.arrow(page, s, miss, sa="bottom", sb="left", color="muted", dash=True, elbow=True)
    kit.arrow(page, miss, miss_o, color="muted", dash=True)
    kit.node(page, M, y0 + 2.85, W, 0.6, "모델 가중치는 그대로다. 입력에 무엇이 들어가는지만 달라진다.",
             style="retained")


# ======================================================== 9. case: AI literacy

def s21(page, h):
    y0 = start(page, h, "사례   AI교양", "확정 전에 삽화를 만들어도 될까?", "핵심",
               "사람이 확정해야 다음 단계가 열리는 좁은 업무용 하네스다.",
               "교육용 인용이며 제작을 실행하지 않았다. 초안 식별자와 계정 화면은 쓰지 않는다.")
    nw, nh, pitch = 1.83, 1.15, 2.08
    labels = ["원문 보존\nv01", "수정과\n버전", "사용자\n최종 확정", "삽화 한 장\nObsidian\n보관",
              "네이버\n비공개 초안", "다시 열어\n확인"]
    styles = ["base", "base", "gate", "base", "base", "focus"]
    ns = [kit.node(page, M + i * pitch, y0, nw, nh, lab, style=st)
          for i, (lab, st) in enumerate(zip(labels, styles))]
    chain(page, ns)
    gate, rev = ns[2], ns[1]
    gx, rx = gate.x + gate.w / 2, rev.x + rev.w / 2
    ly = y0 + nh + 0.42
    kit.path_arrow(page, [(gx, y0 + nh), (gx, ly), (rx, ly), (rx, y0 + nh)], color="warning",
                   dash=True, src=gate, dst=rev)
    kit.text(page, rx - 0.6, ly + 0.04, gx - rx + 1.2, 0.4, [[("수정 요청이면 되돌아감", L, True, C["warning"])]],
             align="center", hint="back")
    kit.node(page, ns[4].x, y0 + 1.45, R - ns[4].x, 0.6, "공개 발행: 이 흐름에 없음", style="out")
    hy = y0 + 2.65
    kit.text(page, M, hy, 1.9, 0.7, [[("좁은 하네스", L, True, C["primary"])]], hint="harness")
    kit.node(page, 2.5, hy, 3.0, 0.7, "규칙: 원문 보존", style="chip")
    kit.node(page, 5.65, hy, 3.2, 0.7, "상태: 버전, 확정 여부", style="chip")
    kit.node(page, 9.0, hy, R - 9.0, 0.7, "검증: 저장본 대조, 재열람", style="chip")


def s22(page, h):
    y0 = start(page, h, "휴식", "", "", "", "", kind="break")
    kit.text(page, M, y0 + 0.6, W, 2.2, [[("10분", 120, True, C["primary"])]], align="center",
             hint="minutes")
    kit.text(page, M, y0 + 3.0, W, 0.6, [[("질문은 메모해 두었다가 마지막 질의응답에서 받습니다", T.SIZE["body"],
                                           False, C["muted"])]], align="center", hint="memo")


# ======================================================== 10. sessions and actors

def s23(page, h):
    y0 = start(page, h, "용어   세션과 주체", "같은 대화를 두 화면에서 보면 작업자도 두 명일까?", "정의",
               "대화와 상태가 묶인 작업 흐름의 단위이며, 실행 주체가 아니다.",
               "세션에 저장된 이력 전체가 곧 이번 호출의 컨텍스트는 아니다.")
    a = kit.node(page, M, y0 + 0.4, 2.4, 0.95, "화면 A\n노트북")
    b = kit.node(page, M, y0 + 2.1, 2.4, 0.95, "화면 B\n휴대폰")
    ses = kit.container(page, 3.9, y0, 5.9, 3.45, hint="session")
    kit.text(page, 4.1, y0 + 0.05, 5.5, 0.42, [[("세션 하나", L, True, C["primary"])]],
             parent=ses.name, hint="session-label")
    for i, lab in enumerate(["대화 이력", "도구 기록", "상태 파일 링크"]):
        kit.node(page, 4.2, y0 + 0.55 + i * 0.6, 5.3, 0.5, lab, style="chip", parent=ses.name)
    kit.node(page, 4.2, y0 + 2.45, 5.3, 0.7, "워커 하나 (쓰기 주체)", style="focus", parent=ses.name)
    kit.arrow(page, a, ses, elbow=True)
    kit.arrow(page, b, ses, elbow=True)
    kit.node(page, 10.2, y0 + 1.1, R - 10.2, 1.25, "화면이 둘이어도\n세션과 작업자는\n하나", style="note")


def s24(page, h):
    y0 = start(page, h, "용어   세션과 주체", "문서를 실제로 고칠 담당은 누구로 정해야 할까?", "정의",
               "배정받은 작업을 수행하는 실행 주체다. 읽기 전용일 수도 있다.",
               "작업 지시는 기술적 접근 차단이 아니다. 실제 권한은 도구와 실행 설정이 정한다.")
    bound = kit.container(page, M, y0, 7.7, 3.45, style="note", hint="instruction-bound")
    kit.text(page, M + 0.2, y0 + 0.05, 7.3, 0.42, [[("작업 지시의 범위 (기술적 샌드박스 아님)", L, True, C["muted"])]],
             parent=bound.name, hint="bound-label")
    inp = kit.node(page, M + 0.25, y0 + 0.75, 2.0, 0.95, "작업 지시\n고칠 부분 목록", parent=bound.name)
    wa = kit.node(page, 3.25, y0 + 0.75, 2.0, 0.95, "워커 A\n수정 담당", style="focus", parent=bound.name)
    out = kit.node(page, 5.75, y0 + 0.75, 2.2, 0.95, "쓰기 허용\noutput/", parent=bound.name)
    chain(page, [inp, wa, out])
    kit.node(page, M + 0.25, y0 + 2.2, 7.2, 0.7, "tickets.csv: 원본 수정 금지 지시", style="caution",
             parent=bound.name)
    wb = kit.node(page, 8.6, y0, R - 8.6, 0.95, "워커 B\n읽기 전용 조사")
    memo = kit.node(page, 8.6, y0 + 1.35, R - 8.6, 0.6, "조사 메모")
    kit.arrow(page, wb, memo, sa="bottom", sb="top")
    kit.node(page, 8.6, y0 + 2.35, R - 8.6, 0.9, "쓰기 담당은 한 명\n보고는 자기 보고", style="note")


def s25(page, h):
    y0 = start(page, h, "용어   세션과 주체", "하위 작업을 맡은 작업자가 원문을 고쳐도 될까?", "정의",
               "상위가 맡긴 하위 작업을 별도 입력으로 수행하는 하위 실행이다.",
               "공유 범위와 권한은 제품과 설정에 따라 다르다. 이 워크샵은 서브에이전트를 직접 실행하지 않는다.")
    par = kit.node(page, M, y0 + 0.05, 3.5, 0.9, "상위 작업\n보고서 작성")
    ch = kit.node(page, 5.3, y0 + 1.6, 3.9, 0.9, "서브에이전트\n용어 목록 추출", style="focus")
    px = par.x + par.w / 2
    kit.path_arrow(page, [(px, par.y + par.h), (px, ch.y + ch.h / 2), (ch.x, ch.y + ch.h / 2)],
                   src=par, dst=ch)
    kit.text(page, px + 0.15, ch.y + ch.h / 2 - 0.46, 2.8, 0.4, [[("별도 입력: 문서와 지시", L, False, C["ink"])]],
             hint="in-label")
    cx = ch.x + ch.w / 2
    py = par.y + par.h / 2
    kit.path_arrow(page, [(cx, ch.y), (cx, py), (par.x + par.w, py)], color="primary",
                   src=ch, dst=par)
    kit.text(page, par.x + par.w + 0.15, py - 0.46, 2.4, 0.4, [[("결과: 용어 목록", L, True, C["primary"])]],
             hint="out-label")
    kit.node(page, 5.3, y0 + 2.75, 3.9, 0.6, "읽기 전용 작업 지시 (이번 예시)", style="chip")
    kit.node(page, 9.75, y0 + 0.05, R - 9.75, 1.15, "지시만으로\n권한이 제거되지는\n않는다", style="caution")
    kit.node(page, 9.75, y0 + 1.5, R - 9.75, 1.15, "같은 모델이면\n독립 검토가\n보장되지 않는다", style="note")


# ======================================================== 11. case: CEO Agent

def s26(page, h):
    y0 = start(page, h, "사례   CEO Agent", "같은 사실이라면 사내 보고와 외부 발언의 강조도 같아야 할까?", "핵심",
               "조사한 근거에서 나온 페르소나를 과업, 독자, 자리에 맞게 고른다.",
               "2차 언론 보도는 보조 근거로만 쓴다. 원자료와 인물 정보는 공개하지 않으며, 모델을 학습시키지 않는다.")
    lab_w = 1.6
    for name, eng, y, hgt in [("조사", "RESEARCH", y0, 1.42), ("실행", "EXECUTION", y0 + 1.5, 1.05)]:
        b = kit.band(page, M, y, W, hgt, hint=f"lane-{name}")
        kit.text(page, M + 0.12, y, lab_w, hgt, [[(name, L, True, C["primary"])], [(eng, 16, False, C["muted"])]],
                 parent=b.name, hint="lane-label")
    sx, sw = 2.3, 2.75
    src = [kit.node(page, sx, y0 + 0.08 + i * 0.44, sw, 0.4, lab, style="plain")
           for i, lab in enumerate(["본인이 쓴 글과 서신", "본인 편집 변경 기록", "실제 피드백"])]
    nh = 0.82
    ay = y0 + (1.42 - nh) / 2
    trait = kit.node(page, 5.45, ay, 1.6, nh, "상황별\n특성")
    spec_n = kit.node(page, 7.45, ay, 1.6, nh, "페르소나\n명세", style="focus")
    fb = kit.node(page, 11.15, ay, R - 11.15, nh, "사람\n피드백", style="gate")
    kit.arrow(page, src[1], trait)
    kit.arrow(page, trait, spec_n)
    by = y0 + 1.5 + (1.05 - 0.8) / 2
    kit.node(page, sx, by, sw, 0.8, "관찰과 가설은\n구분해 표시", style="note")
    task = kit.node(page, 5.45, by, 1.6, 0.8, "과업, 독자,\n자리")
    pick = kit.node(page, 7.45, by, 1.6, 0.8, "등록과\n기준 선택", style="focus")
    ctx = kit.node(page, 9.35, by, 1.55, 0.8, "관련\n맥락만")
    out = kit.node(page, 11.15, by, R - 11.15, 0.8, "결과물")
    kit.arrow(page, spec_n, pick, sa="bottom", sb="top", color="primary", width=2.25)
    chain(page, [task, pick, ctx, out])
    kit.arrow(page, out, fb, sa="top", sb="bottom")
    kit.arrow(page, fb, spec_n, sa="left", sb="right", color="muted", dash=True)
    ey = y0 + 2.7
    fact = kit.node(page, M, ey, 4.1, 0.82, "같은 사실 (가상)\n분기 일정 지연 두 건")
    o1 = kit.node(page, 5.1, ey, R - 5.1, 0.4, "사내 보고 검수: 원인과 조치 기한을 묻는다", style="chip",
                  align="left")
    o2 = kit.node(page, 5.1, ey + 0.42, R - 5.1, 0.4, "외부 발언: 같은 사실을 배경과 함께 설명한다",
                  style="chip", align="left")
    kit.path_arrow(page, [(4.64, ey + 0.41), (5.06, ey + 0.2)], src=fact, dst=o1)
    kit.path_arrow(page, [(4.64, ey + 0.41), (5.06, ey + 0.62)], src=fact, dst=o2)


# ======================================================== 12. flow and verification

def s27(page, h):
    y0 = start(page, h, "용어   흐름과 검증", "최종 확정 전에 삽화를 만들어도 될까?", "정의",
               "입력, 단계, 산출물, 넘어가는 조건을 정한 흐름이다.",
               "AI교양 흐름을 다시 쓴다. 공개 발행은 이 흐름에 없다.")
    cy, nh = y0 + 0.2, 1.0
    n1 = kit.node(page, M, cy, 2.2, nh, "원문 보존\nv01")
    n2 = kit.node(page, 3.25, cy, 2.2, nh, "수정과 확인\nv02, v03")
    dm = kit.node(page, 6.2, cy - 0.2, 2.2, 1.4, "확정?", style="gate", shape="diamond")
    n4 = kit.node(page, 9.15, cy, R - 9.15, nh, "삽화, 보존,\n비공개 초안, 재열람")
    chain(page, [n1, n2])
    kit.arrow(page, n2, dm)
    kit.arrow(page, dm, n4)
    kit.text(page, 8.4, cy + 0.05, 0.75, 0.4, [[("예", L, True, C["ink"])]], align="center",
             hint="yes")
    dx, rx = dm.x + dm.w / 2, n2.x + n2.w / 2
    ly = cy + nh + 0.75
    kit.path_arrow(page, [(dx, dm.y + dm.h), (dx, ly), (rx, ly), (rx, cy + nh)], color="warning",
                   dash=True, src=dm, dst=n2)
    kit.text(page, rx + 0.2, ly + 0.04, dx - rx - 0.4, 0.4, [[("아니오: 다시 수정", L, True, C["warning"])]],
             align="center", hint="no")
    kit.text(page, 7.45, cy + 1.25, 2.15, 0.4, [[("사람이 결정", L, True, C["warning"])]],
             align="center", hint="human")
    kit.node(page, M, y0 + 2.75, 6.0, 0.7, "사람이 단계를 따라 해도 워크플로우다", style="note")
    kit.node(page, 6.83, y0 + 2.75, 6.0, 0.7, "자동화는 일부 단계를 시작하는 장치 (S28)", style="note")


def s28(page, h):
    y0 = start(page, h, "용어   흐름과 검증", "확정 메시지 하나로 뒤의 제작 전체를 시작해도 될까?", "정의",
               "조건이 맞으면 정해진 작업을 시작하는 장치다.",
               "자동 실행이 성공해도 결과가 맞다는 보장은 없다. 검증은 따로 한다. 설명용이며 실행하지 않았다.")
    gate = kit.node(page, M, y0 + 1.1, 2.2, 1.0, "사람\n최종 확정", style="gate")
    box = kit.container(page, 3.1, y0, 7.1, 3.45, style="scope", hint="automation")
    kit.text(page, 3.3, y0 + 0.05, 6.7, 0.42, [[("자동화 범위", L, True, C["primary"])]],
             parent=box.name, hint="auto-label")
    trig = kit.node(page, 3.35, y0 + 1.1, 1.95, 1.0, "트리거\n확정 메시지", style="focus", parent=box.name)
    tasks = [kit.node(page, 5.85, y0 + 0.6 + i * 0.85, 2.1, 0.6, lab, parent=box.name)
             for i, lab in enumerate(["삽화와 보존", "비공개 초안", "재열람"])]
    log = kit.node(page, 8.35, y0 + 1.1, 1.65, 1.0, "기록\n실행, 실패", parent=box.name)
    kit.arrow(page, gate, trig)
    kit.arrow(page, trig, tasks[0], elbow=True)
    for a, b in zip(tasks, tasks[1:]):
        kit.arrow(page, a, b, sa="bottom", sb="top")
    kit.arrow(page, tasks[2], log, elbow=True)
    kit.node(page, 10.6, y0 + 1.1, R - 10.6, 1.0, "공개 발행\n조건에 없음", style="out")
    kit.text(page, M, y0 + 2.25, 2.2, 0.82, [[("자동화", L, True, C["warning"])], [("바깥", L, True, C["warning"])]],
             align="center", hint="outside")


def s29(page, h):
    y0 = start(page, h, "용어   흐름과 검증", "'검토 완료' 한 줄이면 검토가 끝났다고 말할 수 있을까?", "정의",
               "끝났다고 말한 기록이며, 증거와 함께 있어야 쓸모가 있다.",
               "보고 문구와 숫자는 가상이다. done 표시는 실행이 끝났다는 증거일 뿐이다.")
    card = kit.container(page, M, y0, 4.7, 2.55, style="tile", hint="report")
    kit.text(page, M + 0.2, y0 + 0.05, 4.3, 0.42, [[("완료 보고 (가상)", L, True, C["ink"])]],
             parent=card.name, hint="card-title")
    for i, (k, v) in enumerate([("상태", "완료"), ("산출물", "report.md"), ("확인", "건수 검증 완료"),
                                ("미확인", "없음")]):
        kit.text(page, M + 0.2, y0 + 0.55 + i * 0.47, 4.3, 0.42,
                 [[(f"{k}   ", L, True, C["muted"]), (v, L, False, C["ink"])]], parent=card.name,
                 hint=f"card{i}")
    kit.text(page, 5.3, y0 + 0.9, 0.9, 0.4, [[("대조", L, True, C["primary"])]], align="center",
             hint="compare")
    hline_arrow(page, M + 4.7 + 0.05, 6.3 - 0.05, y0 + 1.3)
    kit.text(page, 6.3, y0, R - 6.3, 0.42, [[("증거", L, True, C["ink"])]], hint="ev-title")
    rows = [("파일 있음", "예", "focus"), ("건수 일치", "아니오: 42는 40, 38과 다름", "caution"),
            ("테스트 출력", "첨부 없음", "out")]
    for i, (k, v, st) in enumerate(rows):
        y = y0 + 0.5 + i * 0.7
        kit.node(page, 6.3, y, 2.0, 0.58, k, style="chip")
        kit.node(page, 8.4, y, R - 8.4, 0.58, v, style=st)
    kit.node(page, M, y0 + 2.85, 4.7, 0.6, "보고: 완료", style="focus")
    kit.node(page, 6.3, y0 + 2.85, R - 6.3, 0.6, "검증: 실패", style="caution")


def s30(page, h):
    y0 = start(page, h, "용어   흐름과 검증", "이 숫자가 맞는지 한 번 보는 것으로 충분할까?", "정의",
               "미리 정한 기준을 작업자의 말과 독립된 방법으로 확인한다.",
               "숫자는 가상 예시다. 의미 판단이 필요한 항목은 사람이 따로 확인한다.")
    src = kit.node(page, M, y0 + 0.5, 2.2, 1.0, "원본 CSV\n(가상)")
    c1 = kit.node(page, 3.3, y0, 3.3, 0.7, "행 수 세기: 40")
    c2 = kit.node(page, 3.3, y0 + 0.95, 3.3, 0.7, "고유 ID 세기: 38")
    rep = kit.node(page, 3.3, y0 + 1.9, 3.3, 0.7, "보고서 기재: 42", style="chip")
    cmp_ = kit.node(page, 7.4, y0 + 0.5, 1.8, 1.0, "대조", style="focus")
    res = kit.node(page, 9.9, y0 + 0.25, R - 9.9, 1.5, "실패로 기록\n42는 40과도\n38과도 다르다", style="caution")
    kit.arrow(page, src, c1, elbow=True)
    kit.arrow(page, src, c2, elbow=True)
    kit.arrow(page, c1, cmp_, elbow=True)
    kit.arrow(page, c2, cmp_, elbow=True)
    kit.arrow(page, rep, cmp_, sa="right", sb="bottom", elbow=False)
    kit.arrow(page, cmp_, res)
    kit.node(page, M, y0 + 2.85, W, 0.6, "결정적 검증: 같은 입력이면 같은 결과. 두 번째 모델이 필요 없다.",
             style="retained")


# ======================================================== 13. location and intervention

def s31(page, h):
    y0 = start(page, h, "용어   실행 위치와 개입", "노트북에서 파일을 읽으면 답변도 노트북에서 만들어질까?", "정의",
               "도구는 내 기기에서 돌고, 모델 추론 위치는 따로 말한다.",
               "모델 서비스 연결에 인터넷과 계정이 필요할 수 있다. 위치는 구성 요소별로 적는다.")
    lap = kit.container(page, M, y0, 6.6, 3.45, hint="laptop")
    kit.text(page, M + 0.2, y0 + 0.05, 6.2, 0.42, [[("내 노트북 (로컬)", L, True, C["primary"])]],
             parent=lap.name, hint="lap-label")
    folder = kit.node(page, M + 0.3, y0 + 0.65, 2.6, 0.75, "메모 폴더 (가상)", parent=lap.name)
    tool = kit.node(page, M + 0.3, y0 + 1.75, 2.6, 0.75, "파일 읽기 도구", parent=lap.name)
    rt = kit.node(page, 3.85, y0 + 1.75, 2.9, 0.75, "런타임", style="focus", parent=lap.name)
    kit.arrow(page, folder, tool, sa="bottom", sb="top")
    kit.arrow(page, tool, rt)
    svc = kit.container(page, 8.3, y0 + 0.6, R - 8.3, 2.0, style="note", hint="service")
    kit.text(page, 8.5, y0 + 0.65, R - 8.7, 0.42, [[("모델 추론 서비스", L, True, C["muted"])]],
             parent=svc.name, hint="svc-label")
    inf = kit.node(page, 8.8, y0 + 1.3, R - 9.3, 0.75, "모델 추론", style="base", parent=svc.name)
    yr = rt.y + 0.22
    kit.path_arrow(page, [(rt.x + rt.w, yr), (inf.x, yr)], src=rt, dst=inf)
    kit.path_arrow(page, [(inf.x, yr + 0.32), (rt.x + rt.w, yr + 0.32)], color="primary", src=inf, dst=rt)
    kit.text(page, 6.85, yr - 0.5, 1.9, 0.4, [[("요청과 응답", L, False, C["ink"])]], align="center",
             hint="req")
    kit.node(page, 8.3, y0 + 2.85, R - 8.3, 0.6, "로컬이어도 권한 설정은 필요", style="note")


def s32(page, h):
    y0 = start(page, h, "용어   실행 위치와 개입", "추론은 외부, 파일은 내 노트북이면 클라우드 작업일까?", "정의",
               "실행 위치를 구성 요소별로 말한다.",
               "클라우드라는 말만으로는 어느 부분인지 알 수 없다. 전역 공유를 가정하지 않는다.")
    z1x, z1w, z2x = 1.9, 5.0, 7.3
    z2w = R - z2x
    kit.text(page, z1x, y0, z1w, 0.42, [[("내 기기", L, True, C["ink"])]], align="center", hint="z1")
    kit.text(page, z2x, y0, z2w, 0.42, [[("외부 서버", L, True, C["primary"])]], align="center", hint="z2")
    rows = [("예 A", ["파일 읽기 도구"], ["모델 추론"]),
            ("예 B", ["보기 화면"], ["워커, 파일 환경", "모델 추론"])]
    for r, (lab, local, remote) in enumerate(rows):
        y = y0 + 0.55 + r * 1.2
        b = kit.band(page, M, y, W, 1.0, hint=f"row{r}")
        kit.text(page, M + 0.1, y, 1.2, 1.0, [[(lab, L, True, C["ink"])]], parent=b.name, hint="rl")
        for i, t in enumerate(local):
            kit.node(page, z1x + 0.2 + i * 2.4, y + 0.2, 4.6, 0.6, t, parent=b.name)
        cw = (z2w - 0.4 - 0.15 * (len(remote) - 1)) / len(remote)
        for i, t in enumerate(remote):
            kit.node(page, z2x + 0.2 + i * (cw + 0.15), y + 0.2, cw, 0.6, t, style="focus", parent=b.name)
    kit.node(page, M, y0 + 2.95, W, 0.5, "공유 범위와 가용성은 설정에 따라 다르다", style="note")


def s33(page, h):
    y0 = start(page, h, "용어   실행 위치와 개입", "휴대폰에서 멈춤을 누르면 작업 장소가 휴대폰으로 옮겨질까?", "정의",
               "실행은 원래 환경에서, 보기와 중단은 다른 화면에서 한다.",
               "연결됨과 앱에서 보임은 다르다. 시연은 60초 이내, 실시간이 안 되면 정적 화면을 쓴다.")
    lap = kit.container(page, M, y0, 5.9, 3.45, hint="laptop")
    kit.text(page, M + 0.2, y0 + 0.05, 5.5, 0.42, [[("노트북 (실행 위치)", L, True, C["primary"])]],
             parent=lap.name, hint="lap")
    wk = kit.node(page, M + 0.3, y0 + 0.7, 2.6, 0.8, "워커", style="focus", parent=lap.name)
    kit.node(page, 3.6, y0 + 0.7, 2.5, 0.8, "파일", parent=lap.name)
    kit.node(page, M + 0.3, y0 + 1.9, 5.3, 0.7, "로그와 상태", parent=lap.name)
    app = kit.container(page, 8.0, y0 + 0.35, R - 8.0, 2.35, style="note", hint="app")
    kit.text(page, 8.2, y0 + 0.4, R - 8.4, 0.42, [[("휴대폰 앱 (보기와 지시)", L, True, C["muted"])]],
             parent=app.name, hint="app-label")
    view = kit.node(page, 8.3, y0 + 0.95, R - 8.6, 0.6, "같은 세션 화면", parent=app.name)
    stop = kit.node(page, 8.3, y0 + 1.75, R - 8.6, 0.6, "중단 버튼", style="gate", parent=app.name)
    y1 = wk.y + 0.22
    kit.path_arrow(page, [(M + 5.9 + 0.05, y1), (8.0 - 0.05, y1)], color="primary")
    kit.path_arrow(page, [(8.0 - 0.05, y1 + 0.85), (M + 5.9 + 0.05, y1 + 0.85)], color="warning")
    kit.text(page, 6.45, y1 - 0.48, 1.5, 0.4, [[("상태", L, False, C["primary"])]], align="center",
             hint="state")
    kit.text(page, 6.45, y1 + 0.95, 1.5, 0.4, [[("중단 신호", L, True, C["warning"])]], align="center",
             hint="stop-sig")
    kit.node(page, 8.0, y0 + 2.9, R - 8.0, 0.55, "앱은 두 번째 작성자가 아니다", style="note")
    del view, stop


# ======================================================== 14. synthesis, 15. Q&A

def s34(page, h):
    y0 = start(page, h, "종합", "다른 네 사례에서도 같은 질문이 통할까?", "핵심",
               "다섯 사례는 같은 요소를 쓰지만, 무게를 두는 곳이 다르다.",
               "성과를 비교한 그림이 아니다. Grokbot은 사용자 설명만 쓰며 출처를 확인하지 않았다.")
    xs = [M + i * 2.5 for i in range(5)]
    strip = [kit.node(page, x, y0, 2.1, 0.5, lab, style="gate" if i == 1 else "base")
             for i, (x, lab) in enumerate(zip(xs, ["원문 보존", "최종 확정", "삽화와 보관", "비공개 초안", "재열람"]))]
    chain(page, strip)
    tags(page, xs, 2.1, y0 + 0.52, ["상태: 버전", "사람 게이트", "도구 실행", "자동화", "검증"],
         colors={1: C["warning"]}, bold={1: True})
    ty = y0 + 1.02
    th = T.BOTTOM_LIMIT - ty
    tw, nw, rh = 2.3, 2.0, 0.44
    tiles = [("OpenClaw", "조율과 위임", C["ink"]), ("OMH", "유지 위에 보강", C["ink"]),
             ("Grokbot 설명", "출처 검증 대기", C["warning"]), ("AI교양", "승인과 재확인", C["ink"]),
             ("CEO Agent", "근거로 선택", C["ink"])]
    for i, (name, purpose, pcol) in enumerate(tiles):
        tx = M + i * 2.5
        box = kit.container(page, tx, ty, tw, th, style="tile", hint="tile")
        kit.text(page, tx + 0.12, ty + 0.04, tw - 0.24, 0.4, [[(name, L, True, C["ink"])]], align="center",
                 parent=box.name, hint="tile-head")
        kit.text(page, tx + 0.12, ty + th - 0.44, tw - 0.24, 0.4, [[(purpose, L, True, pcol)]],
                 align="center", parent=box.name, hint="tile-purpose")
        top, span = ty + 0.48, th - 0.96
        step = (span - 3 * rh) / 2
        rows = [top + k * (rh + step) for k in range(3)]
        nx = tx + (tw - nw) / 2
        if name == "OpenClaw":
            chain(page, [kit.node(page, nx, y, nw, rh, lab, parent=box.name)
                         for y, lab in zip(rows, ["코디네이터", "워커", "부모 검증"])], sa="bottom", sb="top")
        elif name == "OMH":
            for y, lab, st in zip(rows, ["도구와 절차", "역할 (유지)", "모델 (유지)"],
                                  ["focus", "retained", "retained"]):
                kit.node(page, nx, y, nw, rh, lab, style=st, parent=box.name)
        elif name == "Grokbot 설명":
            for y in (rows[0], rows[2]):
                for cx in (tx + 0.4, tx + tw - 0.4 - 0.66):
                    kit.node(page, cx, y, 0.66, rh, "봇", style="out", parent=box.name)
            kit.node(page, tx + 0.35, rows[1], tw - 0.7, rh, "공유 환경", style="out", parent=box.name)
        elif name == "AI교양":
            chain(page, [kit.node(page, nx, y, nw, rh, lab, style=st, parent=box.name)
                         for y, lab, st in zip(rows, ["원문 보존", "최종 확정", "재열람"], ["base", "gate", "base"])],
                  sa="bottom", sb="top")
        else:
            chain(page, [kit.node(page, nx, y, nw, rh, lab, style=st, parent=box.name)
                         for y, lab, st in zip(rows, ["조사 근거", "페르소나 명세", "상황별 선택"],
                                               ["base", "focus", "base"])], sa="bottom", sb="top")


def s35(page, h):
    y0 = start(page, h, "질의응답", "가장 헷갈렸던 용어 하나는 무엇이었나?", "정리",
               "질문을 받고, 다섯 문장으로 다시 묶는다.",
               "확인이 필요한 답은 확인 필요라고 말한다. 제품 기능과 성능은 단정하지 않는다.")
    anchors = [("모델은 요청을 만들고, 실행은 런타임이 한다", "S3, S5"),
               ("입력에 실제로 들어간 것만 컨텍스트다", "S17, S20"),
               ("완료 보고는 주장이고, 검증은 확인이다", "S29, S30"),
               ("위치는 구성 요소별로 말한다", "S31, S32, S33"),
               ("사람의 확정은 자동화 바깥에 둔다", "S21, S28")]
    for i, (text, refs) in enumerate(anchors):
        y = y0 + i * 0.7
        kit.node(page, M, y, 0.58, 0.58, str(i + 1), style="solid", radius=0.29)
        kit.node(page, 1.25, y, 8.4, 0.58, text, style="chip", align="left")
        kit.text(page, 9.8, y, R - 9.8, 0.58, [[(refs, L, False, C["muted"])]], align="right",
                 hint=f"refs{i}")


SLIDES = {n: globals()[f"s{n:02d}"] for n in range(1, 36)}
