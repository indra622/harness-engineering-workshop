"""Slide definitions keyed by the canonical v10 slide ID.

Each function draws the diagram for one slide on top of the shared frame.
Add the remaining slides here with the same pattern; build_deck.py picks
the set to render. On-screen wording is a short draft drawn from the
production brief; the full source text goes into speaker notes.
"""

from pptx.enum.text import PP_ALIGN

from . import frame, kit
from . import theme as T

C = T.COLORS
L = T.SIZE["label"]
M = T.MARGIN
R = T.RIGHT


def _tags(page, xs, w, y, labels, colors=None, bold=None):
    for i, (x, lab) in enumerate(zip(xs, labels)):
        col = (colors or {}).get(i, C["muted"])
        b = (bold or {}).get(i, False)
        kit.text(page, x, y, w, 0.4, [[(lab, L, b, col)]], align=PP_ALIGN.CENTER,
                 hint=f"tag-{lab}")


# ------------------------------------------------------------------ S1

def s01(page, h):
    spec = dict(sid=1, section="시작", time="0분부터 2분까지, 2분", title=h["title"],
                question="이 흐름이 단계를 건너뛰지 않게 하는 것은 누구일까?",
                lead_tag="장면",
                lead="AI교양 글 한 편의 작업이 끝났다. 어떤 단계를 거쳤을까?",
                footnote="비공개 초안에는 설정된 광고와 안내 이미지가 들어간다. "
                         "실제 화면과 계정 정보는 보여 주지 않는다.")
    y0 = frame.build(page, spec) + 0.3

    scope = kit.container(page, M, y0, 10.15, 2.85, style="scope", hint="workflow-scope")
    kit.text(page, M + 0.2, y0 + 0.12, 4.2, 0.42,
             [[("이 업무 흐름의 범위", L, True, C["primary"])]], parent=scope.name,
             hint="scope-label")

    ny, nh, nw, pitch = y0 + 0.72, 1.35, 1.75, 2.0
    xs = [M + 0.2 + i * pitch for i in range(5)]
    labels = ["원문 보존\nv01, v02", "사용자\n최종 확정", "삽화 한 장\nObsidian\n보관",
              "네이버\n비공개 초안", "다시 열어\n확인"]
    styles = ["base", "gate", "base", "base", "base"]
    nodes = [kit.node(page, x, ny, nw, nh, lab, style=st, parent=scope.name)
             for x, lab, st in zip(xs, labels, styles)]
    for a, b in zip(nodes, nodes[1:]):
        kit.arrow(page, a, b)
    _tags(page, xs, nw, ny + nh + 0.12,
          ["버전 기록", "사람이 결정", "이미지 보관", "초안 저장", "재열람 결과"],
          colors={1: C["warning"]}, bold={1: True})

    ox = 10.9
    kit.node(page, ox, ny, R - ox, nh, "공개 발행\n범위 밖", style="out", hint="publish-out")
    kit.text(page, ox, ny + nh + 0.12, R - ox, 0.4, [[("흐름에 없음", L, False, C["muted"])]],
             align=PP_ALIGN.CENTER, hint="publish-tag")
    return spec


# ------------------------------------------------------------------ S5

def s05(page, h):
    spec = dict(sid=5, section="용어   모델과 실행 틀", time="11분부터 14분까지, 3분",
                title=h["title"], question="AI 모델이 파일을 직접 열까?",
                lead_tag="정의",
                lead="모델은 요청만 만들고, 런타임이 실행해 결과를 돌려준다.",
                footnote="여기서 런타임은 Python이나 Node.js 같은 언어 실행 환경이 아니다. "
                         "흐름은 가상 예시다.")
    y0 = frame.build(page, spec)

    lane_h, gap = 1.1, 0.1
    lanes = [("모델", "band", None), ("런타임", "focus_fill", "primary"),
             ("도구와\n파일", "band", None)]
    ly = []
    for k, (name, color, line) in enumerate(lanes):
        y = y0 + k * (lane_h + gap)
        ly.append(y)
        b = kit.band(page, M, y, R - M, lane_h, color=color, line=line,
                     line_w="focus" if line else "hair", hint=f"lane-{name}")
        kit.text(page, M + 0.15, y, 1.45, lane_h,
                 kit.runs_of(name, L, True, C["primary"] if line else C["ink"]),
                 parent=b.name, hint=f"lane-label-{name}")

    x0, pitch, nw, nh = 2.2, 1.77, 1.47, 0.82
    plan = [(0, 0, "1. 요청\nread_file", "base"),
            (1, 1, "2. 권한\n확인", "focus"),
            (2, 1, "3. 도구\n호출", "focus"),
            (3, 2, "4. 파일\n읽기", "base"),
            (4, 1, "5. 결과\n정리", "focus"),
            (5, 0, "6. 다음\n판단", "base")]
    nodes = []
    for col, lane, lab, st in plan:
        nodes.append(kit.node(page, x0 + col * pitch, ly[lane] + (lane_h - nh) / 2,
                              nw, nh, lab, style=st))
    kit.arrow(page, nodes[0], nodes[1], elbow=True)
    kit.arrow(page, nodes[1], nodes[2])
    kit.arrow(page, nodes[2], nodes[3], elbow=True)
    kit.arrow(page, nodes[3], nodes[4], elbow=True)
    kit.arrow(page, nodes[4], nodes[5], elbow=True)

    kit.node(page, 4.2, ly[0] + 0.25, 6.3, 0.6, "모델 쪽에서는 파일이 열리지 않는다",
             style="note", hint="note-model")
    kit.node(page, 9.45, ly[2] + 0.12, 3.2, 0.86, "오류(파일 없음)도\n같은 길로 돌아온다",
             style="note", hint="note-error")
    return spec


# ------------------------------------------------------------------ S11

def s11(page, h):
    spec = dict(sid=11, section="사례   OMH", time="31분부터 36분까지, 5분",
                title=h["title"], title_break=8,
                question="모델만 더 좋은 것으로 바꾸면 이 일이 해결될까?",
                lead_tag="핵심",
                lead="기존 모델과 역할은 유지하고, 업무 도구와 작업 절차를 보강했다.",
                footnote="모의, 오프라인 점검은 실제 사내 모델 품질을 보여 주지 않는다. "
                         "CSV 흐름은 가상 예시다.")
    y0 = frame.build(page, spec)

    x1, w1 = M, 2.35            # constraints
    x2, w2 = 3.2, 6.6           # retained base and what we added
    x3 = 10.15                  # evidence and limits
    w3 = R - x3
    cols = [(x1, w1, "실제 제약"), (x2, w2, "기반은 유지, 도구와 절차는 보강"),
            (x3, w3, "증거와 한계")]
    for x, w, head in cols:
        kit.text(page, x, y0, w, 0.4, [[(head, L, True, C["ink"])]], hint=f"head-{head}")
    cy = y0 + 0.5

    for i, lab in enumerate(["오프라인 설치만", "로컬 파일만", "설정된 모델 하나"]):
        kit.node(page, x1, cy + i * 0.75, w1, 0.6, lab, style="chip")

    box = kit.container(page, x2, cy, w2, 1.05, style="focus", hint="added")
    adds = ["data_inspect\n구조 점검", "data_compare\n키 기준 비교", "선택형 절차\npstack 일부"]
    cw = 2.04
    for i, lab in enumerate(adds):
        kit.node(page, x2 + 0.12 + i * (cw + 0.1), cy + 0.13, cw, 0.79, lab, style="base",
                 parent=box.name)
    kit.node(page, x2, cy + 1.15, w2, 0.45, "OpenCode + OMO 기존 역할 (유지)",
             style="retained")
    kit.node(page, x2, cy + 1.65, w2, 0.45, "설정된 단일 모델 (유지, 재학습 없음)",
             style="retained")

    kit.node(page, x3, cy, w3, 0.55, "설치와 점검 기록", style="base")
    kit.node(page, x3, cy + 0.65, w3, 0.55, "모의 환경 테스트", style="base")
    kit.node(page, x3, cy + 1.3, w3, 0.8, "사내 모델 품질\n미검증", style="caution")

    kit.free_arrow(page, x1 + w1 + 0.03, cy + 1.05, x2 - 0.03, cy + 1.05)
    kit.free_arrow(page, x2 + w2 + 0.03, cy + 1.05, x3 - 0.03, cy + 1.05)

    ry = cy + 2.1 + 0.27
    kit.text(page, M, ry, 1.45, 0.55, [[("가상 예시", L, True, C["muted"])]], hint="csv-tag")
    steps = ["새 CSV", "구조 점검", "변경", "키 기준 비교"]
    sx = [2.0 + i * 2.75 for i in range(4)]
    sn = [kit.node(page, x, ry, 2.3, 0.55, lab, style="focus" if i in (1, 3) else "base")
          for i, (x, lab) in enumerate(zip(sx, steps))]
    for a, b in zip(sn, sn[1:]):
        kit.arrow(page, a, b)
    return spec


# ------------------------------------------------------------------ S17

def s17(page, h):
    spec = dict(sid=17, section="용어   입력과 한계", time="51분부터 54분까지, 3분",
                title=h["title"], question="AI는 지난 회의의 결정을 떠올릴 수 있을까?",
                lead_tag="정의",
                lead="이번 호출에 실제로 들어간 입력 전체가 컨텍스트다.",
                footnote="읽힌 내용은 근거가 될 뿐 정답을 보장하지 않는다. "
                         "출력은 가상 예시다.")
    y0 = frame.build(page, spec)

    panels = [
        (M, "요청만 보냈을 때", C["ink"],
         [("요청 한 줄", "chip"), ("파일 경로만", "note")],
         ("회의록 파일 (디스크)", "읽히지 않음", "out"),
         "출력 (예시)\n일반 목록", "base"),
        (6.88, "회의록을 명시적으로 읽혔을 때", C["primary"],
         [("요청 한 줄", "chip"), ("안건과 참석자", "chip"), ("지난 결정 (회의록)", "focus")],
         ("회의록 파일 (디스크)", "명시적으로 읽음", "base"),
         "출력 (예시)\n결정을 반영한\n준비안", "focus"),
    ]
    for px, head, hcol, chips, disk, out, ost in panels:
        kit.text(page, px, y0, 5.95, 0.4, [[(head, L, True, hcol)]], hint=f"panel-{head}")
        by, bh = y0 + 0.5, 1.97
        box = kit.container(page, px, by, 3.55, bh, style="scope", hint="context")
        kit.text(page, px + 0.15, by + 0.05, 3.25, 0.38,
                 [[("이번 호출의 컨텍스트", L, True, C["primary"])]], parent=box.name,
                 hint="context-label")
        for i, (lab, st) in enumerate(chips):
            kit.node(page, px + 0.2, by + 0.45 + i * 0.5, 3.15, 0.42, lab, style=st,
                     parent=box.name)
        name, state, dst = disk
        state_col = C["primary"] if dst == "base" else C["muted"]
        dnode = kit.node(page, px, by + bh + 0.28, 3.55, 0.8, "",
                         style=dst, hint=f"disk-{state}",
                         paragraphs=[[(name, L, False, C["ink"] if dst == "base" else C["muted"])],
                                     [(state, L, True, state_col)]])
        if dst == "base":
            kit.arrow(page, dnode, box, sa="top", sb="bottom", color="primary", width="focus")
        oh = 1.3
        onode = kit.node(page, px + 3.85, by + (bh - oh) / 2, 2.1, oh, out, style=ost)
        kit.arrow(page, box, onode)
    return spec


# ------------------------------------------------------------------ S26

def s26(page, h):
    spec = dict(sid=26, section="사례   CEO Agent", time="87분부터 90분까지, 3분",
                title=h["title"], title_break=11,
                question="같은 사실이라면 사내 보고와 외부 발언의 강조도 같아야 할까?",
                lead_tag="핵심",
                lead="조사한 근거에서 나온 페르소나를 과업, 독자, 자리에 맞게 고른다.",
                footnote="2차 언론 보도는 보조 근거로만 쓴다. 원자료와 인물 정보는 공개하지 않으며, "
                         "모델을 학습시키지 않는다.")
    y0 = frame.build(page, spec)

    lab_w = 1.6
    lanes = [("조사", "RESEARCH", y0, 1.42), ("실행", "EXECUTION", y0 + 1.5, 1.05)]
    for name, eng, y, hgt in lanes:
        b = kit.band(page, M, y, R - M, hgt, hint=f"lane-{name}")
        kit.text(page, M + 0.12, y, lab_w, hgt,
                 [[(name, L, True, C["primary"])], [(eng, 16, False, C["muted"])]],
                 parent=b.name, hint=f"lane-label-{name}")

    sx, sw = 2.3, 2.75
    src = ["본인이 쓴 글과 서신", "본인 편집 변경 기록", "실제 피드백"]
    srcn = [kit.node(page, sx, y0 + 0.08 + i * 0.44, sw, 0.4, lab, style="plain")
            for i, lab in enumerate(src)]
    nh = 0.82
    ay = y0 + (1.42 - nh) / 2
    trait = kit.node(page, 5.45, ay, 1.6, nh, "상황별\n특성")
    spec_n = kit.node(page, 7.45, ay, 1.6, nh, "페르소나\n명세", style="focus")
    fb = kit.node(page, 11.15, ay, R - 11.15, nh, "사람\n피드백", style="gate")
    kit.arrow(page, srcn[1], trait)
    kit.arrow(page, trait, spec_n)

    by = y0 + 1.5 + (1.05 - 0.8) / 2
    note = kit.node(page, sx, by, sw, 0.8, "관찰과 가설은\n구분해 표시", style="note")
    task = kit.node(page, 5.45, by, 1.6, 0.8, "과업, 독자,\n자리")
    pick = kit.node(page, 7.45, by, 1.6, 0.8, "등록과\n기준 선택", style="focus")
    ctx = kit.node(page, 9.35, by, 1.55, 0.8, "관련\n맥락만")
    out = kit.node(page, 11.15, by, R - 11.15, 0.8, "결과물")
    kit.arrow(page, spec_n, pick, sa="bottom", sb="top", color="primary", width="focus")
    kit.arrow(page, task, pick)
    kit.arrow(page, pick, ctx)
    kit.arrow(page, ctx, out)
    kit.arrow(page, out, fb, sa="top", sb="bottom")
    kit.arrow(page, fb, spec_n, sa="left", sb="right", color="muted", dash=True)
    del note

    ey = y0 + 2.7
    fact = kit.node(page, M, ey, 4.1, 0.82, "같은 사실 (가상)\n분기 일정 지연 두 건", style="base")
    o1 = kit.node(page, 5.1, ey, R - 5.1, 0.4, "사내 보고 검수: 원인과 조치 기한을 묻는다",
                  style="chip", align=PP_ALIGN.LEFT)
    o2 = kit.node(page, 5.1, ey + 0.42, R - 5.1, 0.4, "외부 발언: 같은 사실을 배경과 함께 설명한다",
                  style="chip", align=PP_ALIGN.LEFT)
    kit.free_arrow(page, 4.62, ey + 0.41, 5.08, ey + 0.2)
    kit.free_arrow(page, 4.62, ey + 0.41, 5.08, ey + 0.62)
    del o1, o2, fact
    return spec


# ------------------------------------------------------------------ S34

def s34(page, h):
    spec = dict(sid=34, section="종합", time="111분부터 115분까지, 4분", title=h["title"],
                question="다른 네 사례에서도 같은 질문이 통할까?",
                lead_tag="핵심",
                lead="다섯 사례는 같은 요소를 쓰지만, 무게를 두는 곳이 다르다.",
                footnote="성과를 비교한 그림이 아니다. Grokbot은 사용자 설명만 쓰며 "
                         "출처를 확인하지 않았다.")
    y0 = frame.build(page, spec)

    xs = [M + i * 2.5 for i in range(5)]
    labs = ["원문 보존", "최종 확정", "삽화와 보관", "비공개 초안", "재열람"]
    strip = [kit.node(page, x, y0, 2.1, 0.5, lab, style="gate" if i == 1 else "base")
             for i, (x, lab) in enumerate(zip(xs, labs))]
    for a, b in zip(strip, strip[1:]):
        kit.arrow(page, a, b)
    _tags(page, xs, 2.1, y0 + 0.52, ["상태: 버전", "사람 게이트", "도구 실행", "자동화", "검증"],
          colors={1: C["warning"]}, bold={1: True})

    ty = y0 + 1.02
    th = T.BOTTOM_LIMIT - ty
    tw = 2.3
    tiles = [
        ("OpenClaw", "조율과 위임", C["ink"]),
        ("OMH", "유지 위에 보강", C["ink"]),
        ("Grokbot 설명", "출처 검증 대기", C["warning"]),
        ("AI교양", "승인과 재확인", C["ink"]),
        ("CEO Agent", "근거로 선택", C["ink"]),
    ]
    nw = 2.0
    for i, (name, purpose, pcol) in enumerate(tiles):
        tx = M + i * 2.5
        box = kit.container(page, tx, ty, tw, th, style="tile", hint=f"tile-{name}")
        kit.text(page, tx + 0.12, ty + 0.04, tw - 0.24, 0.4, [[(name, L, True, C["ink"])]],
                 align=PP_ALIGN.CENTER, parent=box.name, hint=f"tile-head-{name}")
        kit.text(page, tx + 0.12, ty + th - 0.44, tw - 0.24, 0.4,
                 [[(purpose, L, True, pcol)]], align=PP_ALIGN.CENTER, parent=box.name,
                 hint=f"tile-purpose-{name}")
        rh = 0.44                       # row box height
        top = ty + 0.48
        span = th - 0.96
        step = (span - 3 * rh) / 2
        rows = [top + k * (rh + step) for k in range(3)]
        nx = tx + (tw - nw) / 2
        if name == "OpenClaw":
            ns = [kit.node(page, nx, y, nw, rh, lab, parent=box.name)
                  for y, lab in zip(rows, ["코디네이터", "워커", "부모 검증"])]
            for a, b in zip(ns, ns[1:]):
                kit.arrow(page, a, b, sa="bottom", sb="top")
        elif name == "OMH":
            kit.node(page, nx, rows[0], nw, rh, "도구와 절차", style="focus", parent=box.name)
            kit.node(page, nx, rows[1], nw, rh, "역할 (유지)", style="retained", parent=box.name)
            kit.node(page, nx, rows[2], nw, rh, "모델 (유지)", style="retained", parent=box.name)
        elif name == "Grokbot 설명":
            bw = 0.66
            for y in (rows[0], rows[2]):
                for cx in (tx + 0.4, tx + tw - 0.4 - bw):
                    kit.node(page, cx, y, bw, rh, "봇", style="out", parent=box.name)
            kit.node(page, tx + 0.35, rows[1], tw - 0.7, rh, "공유 환경", style="out",
                     parent=box.name)
        elif name == "AI교양":
            ns = [kit.node(page, nx, y, nw, rh, lab, style=st, parent=box.name)
                  for y, lab, st in zip(rows, ["원문 보존", "최종 확정", "재열람"],
                                        ["base", "gate", "base"])]
            for a, b in zip(ns, ns[1:]):
                kit.arrow(page, a, b, sa="bottom", sb="top")
        elif name == "CEO Agent":
            ns = [kit.node(page, nx, y, nw, rh, lab, style=st, parent=box.name)
                  for y, lab, st in zip(rows, ["조사 근거", "페르소나 명세", "상황별 선택"],
                                        ["base", "focus", "base"])]
            for a, b in zip(ns, ns[1:]):
                kit.arrow(page, a, b, sa="bottom", sb="top")
    return spec


SLIDES = {1: s01, 5: s05, 11: s11, 17: s17, 26: s26, 34: s34}
REPRESENTATIVE = [1, 5, 11, 17, 26, 34]
