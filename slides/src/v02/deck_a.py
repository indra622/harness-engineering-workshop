"""Slides 1 to 21 of the v02 deck: opening, chapter 1, chapter 2, start of chapter 3."""

import kit
from kit import (AMBER, AMBER_SOFT, BLUE, BLUE_SOFT, INK, INK2, MUTED, PAPER2, RULE, WHITE, Svg,
                 case_head, diff, e, kicker, p, scene)

# ---------------------------------------------------------------- shared builders


def word_size(word):
    n = len(word)
    return 140 if n <= 4 else 120 if n == 5 else 100 if n == 6 else 88


def term_split(ch, idx, word, defn, quote, ask, art, diff_txt, mirror=False):
    """Family A: explanation column beside a lane or loop diagram."""
    body = [
        kicker("sp-kicker", ch, idx),
        p("sp-word", e(word), "h2", f"font-size:{word_size(word)}px"),
        p("sp-def", defn),
        scene("sp-scene", quote, ask),
        art,
        diff(diff_txt),
    ]
    return ("t-paper mirror" if mirror else "t-paper"), "\n  ".join(body)


def term_top(ch, idx, word, defn, quote, ask, art, diff_txt):
    """Families B and C: term and definition on top, full-width comparison or visual below."""
    body = [
        kicker("tp-kicker", ch, idx),
        p("tp-word", e(word), "h2"),
        p("tp-def", defn),
        scene("tp-scene", quote, ask),
        art,
        diff(diff_txt),
    ]
    return "t-paper", "\n  ".join(body)


def chapter(n, num, q_lines, goal, minutes, stations):
    """Chapter transition: the chapter question is the hero, the route below."""
    k = len(stations)
    x0, x1 = 230, 1690
    gap = (x1 - x0) / (k - 1)
    alternate = gap < 260
    s = Svg(f"s{n}", 0, 700, 1920, 300, "이번 장의 경로: " + ", ".join(st[0] for st in stations))
    s.line(128, 150, 1792, 150, color="#FFFFFF", sw=3)
    s.parts[-1] = s.parts[-1].replace("/>", ' stroke-opacity="0.45"/>')
    for i, st in enumerate(stations):
        name, kind = st[0], st[1]
        sub = st[2] if len(st) > 2 else None
        x = round(x0 + i * gap)
        if kind == "term":
            s.add(f'<circle cx="{x}" cy="150" r="15" fill="#FFFFFF"/>')
        else:
            s.rect(x - 26, 124, 52, 52, fill="#FFFFFF")
        label = ("사례 " + name) if kind == "case" else name
        if alternate:
            y = 92 if i % 2 == 0 else 214
            s.text(x, y, label, size=32, weight=800, fill="#FFFFFF", anchor="middle")
        else:
            s.text(x, 96, label, size=38, weight=800, fill="#FFFFFF", anchor="middle")
            if sub:
                s.text(x, 212, sub, size=28, fill="#BFD3FF", anchor="middle")
    body = [
        p("ch-num", f"0{num}", "div").replace('class="abs ch-num"', 'class="abs ch-num" aria-hidden="true"'),
        p("ch-label", f'{num}장<span class="min">약 {minutes}분</span>'),
        p("ch-question", "<br>".join(e(x) for x in q_lines), "h2"),
        p("ch-goal", goal),
        s.render(),
    ]
    return "t-chapter", "\n  ".join(body)


# ---------------------------------------------------------------- 1 cover

def s1():
    body = '''<p class="abs cover-eyebrow">120분 워크숍</p>
  <h1 class="abs cover-title">하네스<br>엔지니어링</h1>
  <p class="abs cover-sub">AI에게 일을 맡기는<br>구조를 설계하는 법</p>
  <div class="abs cover-rule"></div>
  <p class="abs cover-foot">용어 25개와 사례 5개로 읽는 작업의 틀</p>
  <svg class="svg" style="left:1030px;top:140px" width="800" height="800" viewBox="0 0 800 800" role="img" aria-label="모델을 둘러싼 하네스 구조도">
    <rect x="40" y="40" width="720" height="720" fill="none" stroke="#3B4552" stroke-width="2"/>
    <path d="M40 92 V40 H92 M708 40 H760 V92 M760 708 V760 H708 M92 760 H40 V708" fill="none" stroke="#8DB4FF" stroke-width="5"/>
    <text x="70" y="92" font-size="34" font-weight="800" fill="#8DB4FF" letter-spacing="2">하네스</text>
    <circle cx="400" cy="400" r="250" fill="none" stroke="#2C3440" stroke-width="2" stroke-dasharray="6 10"/>
    <g stroke="#4A5564" stroke-width="2.5">
      <line x1="400" y1="400" x2="400" y2="150"/>
      <line x1="400" y1="400" x2="638" y2="323"/>
      <line x1="400" y1="400" x2="547" y2="602"/>
      <line x1="400" y1="400" x2="253" y2="602"/>
      <line x1="400" y1="400" x2="162" y2="323"/>
    </g>
    <g font-size="32" font-weight="700" fill="#ECEEF1" text-anchor="middle" dominant-baseline="central">
      <rect x="300" y="112" width="200" height="76" fill="#1B2129" stroke="#5B6675" stroke-width="2"/><text x="400" y="150">컨텍스트</text>
      <rect x="548" y="285" width="180" height="76" fill="#1B2129" stroke="#5B6675" stroke-width="2"/><text x="638" y="323">도구</text>
      <rect x="452" y="564" width="190" height="76" fill="#1B2129" stroke="#5B6675" stroke-width="2"/><text x="547" y="602">검증</text>
      <rect x="148" y="564" width="210" height="76" fill="#1B2129" stroke="#5B6675" stroke-width="2"/><text x="253" y="602">실행 위치</text>
      <rect x="72" y="285" width="180" height="76" fill="#1B2129" stroke="#5B6675" stroke-width="2"/><text x="162" y="323">상태</text>
    </g>
    <rect x="300" y="300" width="200" height="200" fill="#2457A6"/>
    <text x="400" y="400" font-size="60" font-weight="800" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">모델</text>
    <rect x="378" y="738" width="44" height="44" transform="rotate(45 400 760)" fill="#B45309"/>
    <text x="400" y="700" font-size="28" font-weight="800" fill="#E8A86A" text-anchor="middle">사람의 확인</text>
  </svg>'''
    notes = '''<p>이 워크숍의 주제는 하네스 엔지니어링이다. 모델 하나를 바꾸는 이야기가 아니라, 모델이 일하도록 둘러싼 구조를 설계하는 이야기다.</p>
<p>그림 읽기: 가운데가 모델이다. 그 둘레에 컨텍스트, 도구, 실행 위치, 상태, 검증이 있고, 바깥 틀 전체를 하네스라고 부른다. 틀의 아래쪽에는 사람의 확인이 있다. 결과를 넘길지 정하는 마지막 결정은 사람에게 남는다.</p>
<p>이 정의는 이 워크숍의 작업 정의다. 제품마다 하네스의 범위는 다를 수 있다. 하네스를 바꾼다고 결과가 반드시 좋아진다고 말하지 않는다.</p>
<p>진행: 오늘은 다섯 가지 질문을 따라간다. 용어 25개를 하나씩 설명하고, 사례 다섯 개를 관련 용어 바로 뒤에 둔다. 참가자 실습은 없다. 듣고 질문만 한다.</p>'''
    return dict(kind="cover", label="표지", theme="t-night", body=body, notes=notes)


# ---------------------------------------------------------------- 2 opening scene (S1)

def s2():
    return s2_v03() if kit.VERSION >= "v03" else s2_v02()


def s2_v03():
    """v03: the author finds the topic and writes v01; AI joins only from review onward."""
    s = Svg("s2", 120, 360, 1680, 440, "AI교양 글 한 편: 작가가 주제를 고르고 초고를 직접 쓴 뒤, AI와 함께 다듬고, 작가가 확정한 다음 제작이 이어진다")
    steps = [(["주제를", "찾고 고른다"], "author"), (["초고 v01을", "직접 쓴다"], "author"),
             (["AI와 함께", "검토, 수정"], "ai"), (["최종본", "확정"], "author"),
             (["삽화 생성,", "보관"], "run"), (["네이버", "비공개 초안"], "run"), (["다시 열어", "확인"], "run")]
    w, gap = 212, 32
    for i, (lab, who) in enumerate(steps):
        x = i * (w + gap)
        fill, stroke, sw = {"author": (AMBER_SOFT, AMBER, 3.5), "ai": (BLUE_SOFT, BLUE, 3.5),
                            "run": (WHITE, INK, 2.5)}[who]
        s.box(x, 110, w, 140, lab, size=28, weight=800, fill=fill, stroke=stroke, sw=sw)
        s.num(x, 110, i + 1, fill=AMBER if who == "author" else BLUE if who == "ai" else INK)
        if i < len(steps) - 1:
            s.arrow([(x + w + 2, 180), (x + w + gap - 4, 180)])
    # who does what, under the steps
    s.line(0, 290, 2 * w + gap, 290, color=AMBER, sw=4)
    s.text(0, 322, "작가가 한다", size=26, weight=800, fill=AMBER)
    s.line(2 * (w + gap), 290, 3 * (w + gap) - gap, 290, color=BLUE, sw=4)
    s.text(2 * (w + gap), 322, "AI와 함께", size=26, weight=800, fill=BLUE)
    s.line(3 * (w + gap), 290, 4 * (w + gap) - gap, 290, color=AMBER, sw=4)
    s.text(3 * (w + gap), 322, "작가가 정한다", size=26, weight=800, fill=AMBER)
    s.line(4 * (w + gap), 290, 1680, 290, color=INK, sw=4)
    s.text(4 * (w + gap), 322, "확정 뒤 정해진 절차", size=26, weight=800)
    s.text(0, 30, "v01은 작가가 직접 쓴 원고다. AI가 만든 초안이 아니다.", size=28, weight=800, fill=AMBER)
    s.rect(1180, 370, 500, 60, fill="none", stroke=AMBER, sw=2, dash="8 7")
    s.text(1430, 400, "공개 발행은 이 흐름에 없다", size=28, weight=700, fill=AMBER, anchor="middle")
    body = "\n  ".join([
        p("kicker op-kicker", "시작"),
        p("op-title", "완성된 업무 한 건에서 출발한다", "h2"),
        p("qline", "AI교양 글 한 편이 끝났다. 작가가 주제를 고르고 초고를 직접 썼다. AI와 함께 다듬은 뒤 작가가 확정했고, 그다음 삽화와 비공개 초안을 만들어 다시 열어 확인했다.",
          style="left:120px;top:262px;width:1680px;margin:0"),
        s.render(),
        p("big-q", "이 흐름이 단계를 건너뛰지 않게 하는 것은 누구일까?", "h3",
          "left:120px;top:830px;width:1680px;font-size:56px"),
        p("foot", "설명용 정리다. 실제 화면, 계정 정보, 공개 발행은 보여 주지 않는다. 낯선 라벨은 뒤에서 하나씩 설명한다.",
          style="left:120px;top:960px;width:1680px;margin:0"),
    ])
    notes = '''<p>장면부터 말한다. AI교양 글 한 편이 끝났다. 순서가 중요하다. 작가가 주제를 찾고 골랐다. 작가가 초고 v01을 직접 썼다. v01은 작가의 원고이며 AI가 만든 초안이 아니다. 그다음에야 AI와 함께 문장과 논지를 검토하고 고쳤다(v02, v03처럼 새 버전으로 남기고 이전 본은 보존). 작가가 최종본을 확정했고, 확정 뒤에 삽화를 만들어 보관하고, 네이버 비공개 초안을 만든 뒤 다시 열어 확인했다. 공개 발행은 이 흐름에 없다.</p>
<p>색 읽기: 호박색은 작가가 하거나 정하는 단계, 파랑은 AI와 함께하는 단계, 흰 상자는 확정 뒤 정해진 절차다.</p>
<p>질문을 던지고 답은 받지 않는다: 이 흐름이 단계를 건너뛰지 않게 하는 것은 누구일까? 답은 3장의 AI교양 사례(25번)와 5장의 워크플로우(33번)에서 돌아온다.</p>'''
    return dict(kind="opening", label="시작: 완성된 업무 한 건", theme="t-paper", body=body, notes=notes, v10=[1])


def s2_v02():
    s = Svg("s2", 120, 380, 1680, 400, "AI교양 글 한 편이 끝나기까지의 다섯 단계")
    xs = [0, 350, 700, 1050, 1400]
    labels = [["원문을 받아", "v01로 보존"], ["최종본", "확정"], ["삽화를 만들어", "보관"],
              ["비공개 초안", "작성"], ["다시 열어", "확인"]]
    for i, (x, lab) in enumerate(zip(xs, labels)):
        human = i == 1
        s.box(x, 90, 280, 150, lab, size=32, weight=800,
              fill=AMBER_SOFT if human else WHITE, stroke=AMBER if human else INK, sw=3.5 if human else 2.5)
        s.num(x, 90, i + 1, fill=AMBER if human else INK)
        if i < 4:
            s.arrow([(x + 284, 165), (x + 344, 165)])
    s.text(490, 290, "사람이 정한다", size=28, weight=800, fill=AMBER, anchor="middle")
    s.text(1540, 290, "본문, 대표 이미지, 순서", size=26, fill=MUTED, anchor="middle")
    s.rect(1180, 340, 500, 60, fill="none", stroke=AMBER, sw=2, dash="8 7")
    s.text(1430, 370, "공개 발행은 이 흐름에 없다", size=28, weight=700, fill=AMBER, anchor="middle")
    body = "\n  ".join([
        p("kicker op-kicker", "시작"),
        p("op-title", "완성된 업무 한 건에서 출발한다", "h2"),
        p("qline", "AI교양 글 한 편의 제작이 끝났다. 원문을 받고, 최종본을 확정하고, 삽화와 비공개 초안을 만든 뒤 다시 열어 확인했다.",
          style="left:120px;top:262px;width:1500px;margin:0"),
        s.render(),
        p("big-q", "이 흐름이 단계를 건너뛰지 않게 하는 것은 누구일까?", "h3",
          "left:120px;top:830px;width:1680px;font-size:56px"),
        p("foot", "설명용 정리다. 실제 화면, 계정 정보, 공개 발행은 보여 주지 않는다. 낯선 라벨은 뒤에서 하나씩 설명한다.",
          style="left:120px;top:960px;width:1680px;margin:0"),
    ])
    notes = '''<p>장면부터 말한다. AI교양 글 한 편이 끝났다. 사용자가 원문을 보냈고, 최종본이 확정됐고, 삽화를 만들어 보관했고, 비공개 초안을 만든 뒤 다시 열어 확인했다.</p>
<p>질문을 던지고 답은 받지 않는다: 이 흐름이 단계를 건너뛰지 않게 하는 것은 누구일까? 답은 3장의 AI교양 사례(25번)와 5장의 워크플로우(33번)에서 돌아온다.</p>'''
    return dict(kind="opening", label="시작: 완성된 업무 한 건", theme="t-paper", body=body, notes=notes, v10=[1])


# ---------------------------------------------------------------- 3 roadmap (S2)

ROAD = [
    ("01", "AI는 무엇을 하고, 누가 실행할까?", "모델, 에이전트, 런타임, 하네스", "OpenClaw", 18),
    ("02", "일하는 방법을 어디에 담을까?", "오케스트레이션, 도구, 스킬, 플러그인, 커넥터, MCP", "OMH, Grokbot", 25),
    ("03", "AI는 무엇을 알고 있을까?", "프롬프트, 컨텍스트, 토큰, 컨텍스트 창, 메모리", "AI교양", 20),
    ("04", "누가 이어서 일할까?", "세션, 워커, 서브에이전트", "CEO Agent", 13),
    ("05", "끝났다는 말을 어떻게 믿을까?", "워크플로우, 자동화, 완료 보고, 검증, 로컬 실행, 클라우드 실행, 리모트 컨트롤", "종합", 24),
]


def s3():
    cols = []
    for i, (num, q, terms, case, mins) in enumerate(ROAD):
        left = 120 + i * 344 + (56 if i >= 3 else 0)
        cols.append(f'''<div class="abs road-col" style="left:{left}px">
    <p class="road-num">{num}</p><p class="road-q">{e(q)}</p>
    <p class="road-terms">{e(terms)}</p><p class="road-case">사례 {e(case)}</p><p class="road-min">{mins}분</p></div>''')
    brk = '<div class="abs road-break" style="left:1144px"><span>휴식 10분</span></div>'
    body = "\n  ".join([
        p("kicker op-kicker", "오늘의 길"),
        p("op-title", "다섯 개의 질문을 따라간다", "h2"),
        *cols, brk,
        p("foot", "개념과 사례를 번갈아 본다. 아직 배우지 않은 용어는 사례에서 이름만 보이고, 해당 슬라이드에서 설명한다.",
          style="left:120px;top:960px;width:1680px;margin:0"),
    ])
    notes = '''<p>오늘은 개념과 사례를 번갈아 본다. 각 장은 질문 하나로 시작하고, 그 질문에 답하는 용어를 하나씩 익힌 뒤 사례에서 다시 찾는다.</p>
<p>시간: 여는 부분 4분, 1장 18분, 2장 25분, 3장 20분, 휴식 10분, 4장 13분, 5장 24분, 마무리와 질의응답 6분, 합계 120분.</p>'''
    return dict(kind="roadmap", label="오늘의 길", theme="t-paper", body=body, notes=notes, v10=[2])


# ---------------------------------------------------------------- 4 chapter 1

def s4():
    theme, body = chapter(4, 1, ["AI는 무엇을 하고,", "누가 실행할까?"],
                          "이 장을 마치면 모델이 하는 일과 실행하는 쪽을 나눠 말할 수 있다. 네 개념을 익힌 뒤 OpenClaw 구조에서 직접 찾는다.",
                          18, [("모델", "term", "판단과 생성"), ("에이전트", "term", "반복과 종료"),
                               ("런타임", "term", "실제 실행"), ("하네스", "term", "작업 틀 전체"),
                               ("OpenClaw", "case", "구조 안에서 찾기")])
    notes = '''<p>질문: AI는 무엇을 하고, 누가 실행할까?</p>
<p>순서: 모델(3분), 에이전트(3분), 런타임(3분), 하네스(3분), 사례 OpenClaw(5분). 전환 1분을 더해 약 18분이다.</p>
<p>왜 이 순서인가: 모델이 요청만 만든다는 점을 먼저 세우고, 반복 구조(에이전트), 실제 실행(런타임), 작업 틀(하네스)로 넓힌다. 그다음 OpenClaw 구조에서 방금 배운 네 개념을 찾는다. 워커와 세션은 OpenClaw에서 이름만 미리 보고 4장에서 다룬다.</p>
<p>말할 것: 이 장이 끝나면 "모델이 파일을 열었다"는 말이 왜 부정확한지 설명할 수 있다.</p>'''
    return dict(kind="chapter", label="1장 AI는 무엇을 하고, 누가 실행할까?", theme=theme, body=body, notes=notes)


# ---------------------------------------------------------------- 5 model (S3): one model, two inputs

def s5():
    s = Svg("s5", 120, 440, 1680, 460, "같은 모델에 두 입력을 넣으면 출력이 달라진다")
    s.box(0, 10, 540, 130, [("입력 A", {"size": 24, "fill": MUTED, "weight": 800}), '"내일 회의 준비해 줘"'],
          size=30, weight=700)
    s.box(0, 200, 540, 170, [("입력 B", {"size": 24, "fill": MUTED, "weight": 800}), '"내일 회의 준비해 줘"',
                             ("+ 안건 세 줄", {"fill": BLUE})], size=30, weight=700)
    s.rect(680, 60, 300, 260, fill=BLUE)
    s.text(830, 172, "모델", size=56, weight=800, fill=WHITE, anchor="middle")
    s.text(830, 240, "같은 모델", size=26, fill=WHITE, anchor="middle")
    s.arrow([(540, 75), (610, 75), (610, 150), (674, 150)])
    s.arrow([(540, 285), (610, 285), (610, 230), (674, 230)])
    s.arrow([(980, 150), (1050, 150), (1050, 75), (1114, 75)], color="blue")
    s.arrow([(980, 230), (1050, 230), (1050, 285), (1114, 285)], color="blue")
    s.box(1120, 10, 560, 130, [("출력 A", {"size": 24, "fill": MUTED, "weight": 800}), "일반적인 준비 목록",
                               ("추측이 섞인다", {"size": 26, "weight": 400, "fill": INK2})], size=30)
    s.box(1120, 200, 560, 170, [("출력 B", {"size": 24, "fill": MUTED, "weight": 800}), "안건 중심 준비안",
                                ("주제가 안건 쪽으로 바뀐다", {"size": 26, "weight": 400, "fill": INK2})], size=30)
    s.rect(0, 398, 1680, 62, fill=PAPER2)
    s.text(28, 429, "출력에는 도구 호출 요청도 있다", size=28, weight=800)
    s.text(500, 429, "read_file(path=tickets.csv)", size=26, fill=BLUE, mono=True)
    s.text(1652, 429, "요청만 나온다. 파일은 여기서 열리지 않는다.", size=28, fill=INK2, anchor="end")
    theme, body = term_top(1, 1, "모델",
                           "입력된 텍스트와 맥락을 받아 다음 출력을 만드는 학습된 계산 장치. 출력에는 답변과 도구 호출 요청이 들어갈 수 있다.",
                           '"내일 회의 준비해 줘." 안건도 참석자도 없다.', "그럴듯한 준비안이 나올까?",
                           s.render(), "모델은 출력을 만든다. 출력이 도구 실행과 결과 확인으로 이어져 여러 단계를 도는 구성은 에이전트다.")
    return dict(kind="term", term="모델", term_index=1, chapter=1, v10=[3], label="용어 1 모델",
                theme=theme, body=body, layout="compare")


# ---------------------------------------------------------------- 6 agent (S4): loop with exit

def s6():
    s = Svg("s6", 770, 120, 1040, 760, "모델 판단, 도구 실행, 결과 확인, 종료 조건으로 도는 루프")
    s.box(400, 80, 260, 110, "모델 판단", size=32, weight=800, stroke=INK)
    s.box(760, 325, 260, 110, "도구 실행", size=32, weight=800, stroke=BLUE, sw=3.5)
    s.box(400, 575, 260, 110, "결과 확인", size=32, weight=800, stroke=INK)
    s.add('<polygon points="240,270 350,380 240,490 130,380" fill="#FBECDB" stroke="#B45309" stroke-width="3"/>')
    s.lines(240, 380, ["종료", "조건?"], size=28, weight=800, fill=AMBER, anchor="middle")
    s.arrow([(660, 135), (890, 135), (890, 319)])
    s.arrow([(890, 435), (890, 630), (666, 630)])
    s.arrow([(400, 630), (240, 630), (240, 496)])
    s.arrow([(240, 270), (240, 135), (394, 135)], color="amber")
    s.text(262, 205, "아니오", size=26, weight=800, fill=AMBER)
    s.arrow([(130, 380), (60, 380), (60, 594)])
    s.text(78, 350, "예", size=26, weight=800)
    s.box(0, 600, 200, 90, "종료", size=30, weight=800, fill=INK, stroke=INK, color=WHITE)
    s.lines(555, 380, ["목표: 초안 완성", "종료: 빠진 일정 확인", "발송은 루프 밖"], size=26, fill=INK2, anchor="middle", lh=1.45)
    theme, body = term_split(1, 2, "에이전트",
                             "목표를 받아 모델의 판단, 도구 실행, 결과 확인을 반복하고, 종료 조건이 충족되면 멈추는 실행 구성.",
                             "일정 안내 메일 초안을 맡긴다. 빠진 일정은 되물어 채우고 고친다. 발송은 하지 않는다.",
                             "끝나는 조건이 있는 반복이면 에이전트일까?", s.render(),
                             "응답 횟수로 판단하지 않는다. 결과를 보고 다음 행동이나 종료를 정하는 구조인지 본다.")
    return dict(kind="term", term="에이전트", term_index=2, chapter=1, v10=[4], label="용어 2 에이전트",
                theme=theme, body=body, layout="split")


# ---------------------------------------------------------------- 7 runtime (S5): three lanes

def s7():
    art = '''<svg class="svg" style="left:740px;top:120px" width="1080" height="740" viewBox="0 0 1080 740" role="img" aria-label="모델, 런타임, 도구 세 줄 사이의 요청과 결과 흐름">
    <defs><marker id="s7-ink" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="13" markerHeight="13" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0.5 L10,5 L0,9.5 z" fill="#14171C"/></marker><marker id="s7-blue" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="13" markerHeight="13" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0.5 L10,5 L0,9.5 z" fill="#2457A6"/></marker></defs>
    <rect x="0" y="40" width="1080" height="200" fill="#ECE9E1"/><rect x="0" y="270" width="1080" height="200" fill="#E1E9F6"/><rect x="0" y="270" width="10" height="200" fill="#2457A6"/><rect x="0" y="500" width="1080" height="200" fill="#ECE9E1"/>
    <g font-size="32" font-weight="800"><text x="30" y="148" fill="#14171C">모델</text><text x="30" y="378" fill="#2457A6">런타임</text><text x="30" y="590" fill="#14171C">도구와</text><text x="30" y="632" fill="#14171C">파일</text></g>
    <polyline points="330,140 344,140 344,370 357,370" fill="none" stroke="#14171C" stroke-width="3" marker-end="url(#s7-ink)"/><polyline points="478,370 505,370" fill="none" stroke="#2457A6" stroke-width="3" marker-end="url(#s7-blue)"/><polyline points="626,370 640,370 640,600 653,600" fill="none" stroke="#2457A6" stroke-width="3" marker-end="url(#s7-blue)"/><polyline points="774,600 788,600 788,370 801,370" fill="none" stroke="#14171C" stroke-width="3" marker-end="url(#s7-ink)"/><polyline points="922,370 936,370 936,140 949,140" fill="none" stroke="#2457A6" stroke-width="3" marker-end="url(#s7-blue)"/>
    <g font-size="30" font-weight="700" text-anchor="middle" fill="#14171C"><rect x="180" y="84" width="150" height="112" fill="#FFFFFF" stroke="#14171C" stroke-width="2.5"/><text x="255" y="126">요청</text><text x="255" y="168" font-size="24" font-family="SF Mono, Menlo, monospace" fill="#2457A6">read_file</text><rect x="358" y="314" width="120" height="112" fill="#FFFFFF" stroke="#2457A6" stroke-width="3.5"/><text x="418" y="356">권한</text><text x="418" y="396">확인</text><rect x="506" y="314" width="120" height="112" fill="#FFFFFF" stroke="#2457A6" stroke-width="3.5"/><text x="566" y="356">도구</text><text x="566" y="396">호출</text><rect x="654" y="544" width="120" height="112" fill="#FFFFFF" stroke="#14171C" stroke-width="2.5"/><text x="714" y="586">파일</text><text x="714" y="626">읽기</text><rect x="802" y="314" width="120" height="112" fill="#FFFFFF" stroke="#2457A6" stroke-width="3.5"/><text x="862" y="356">결과</text><text x="862" y="396">정리</text><rect x="950" y="84" width="120" height="112" fill="#FFFFFF" stroke="#14171C" stroke-width="2.5"/><text x="1010" y="126">다음</text><text x="1010" y="166">판단</text></g>
    <g font-size="24" font-weight="800" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central"><circle cx="180" cy="84" r="18" fill="#14171C"/><text x="180" y="85">1</text><circle cx="358" cy="314" r="18" fill="#2457A6"/><text x="358" y="315">2</text><circle cx="506" cy="314" r="18" fill="#2457A6"/><text x="506" y="315">3</text><circle cx="654" cy="544" r="18" fill="#14171C"/><text x="654" y="545">4</text><circle cx="802" cy="314" r="18" fill="#2457A6"/><text x="802" y="315">5</text><circle cx="950" cy="84" r="18" fill="#14171C"/><text x="950" y="85">6</text></g>
    <rect x="372" y="96" width="550" height="88" fill="none" stroke="#5E6570" stroke-width="2" stroke-dasharray="8 7"/><text x="647" y="140" font-size="28" fill="#3A4049" text-anchor="middle" dominant-baseline="central">모델 쪽에서는 파일이 열리지 않는다</text><rect x="808" y="540" width="262" height="120" fill="none" stroke="#5E6570" stroke-width="2" stroke-dasharray="8 7"/><text x="939" y="586" font-size="26" fill="#3A4049" text-anchor="middle">오류도 같은 길로</text><text x="939" y="624" font-size="26" fill="#3A4049" text-anchor="middle">돌아온다</text>
  </svg>'''
    theme, body = term_split(1, 3, "런타임",
                             "모델의 도구 호출 요청을 받아 권한을 확인하고 도구를 실행한 뒤, 결과를 다시 모델 입력으로 돌려주는 실행 계층.",
                             '"지난주 회의 메모 파일 열어 줘."', "실제로 파일을 여는 쪽은 누구일까?", art,
                             "Python, Node.js 같은 언어 실행 환경과 다르다. 하네스보다 좁은, 실행을 잇는 층이다.")
    return dict(kind="term", term="런타임", term_index=3, chapter=1, v10=[5], label="용어 3 런타임",
                theme=theme, body=body, layout="split")


# ---------------------------------------------------------------- 8 harness (S6): frame around five parts

def s8():
    s = Svg("s8", 120, 440, 1680, 460, "모델 바깥을 감싼 하네스의 다섯 칸")
    s.rect(0, 130, 230, 200, fill=BLUE)
    s.text(115, 230, "모델", size=48, weight=800, fill=WHITE, anchor="middle")
    s.line(230, 230, 320, 230, color=INK, sw=3)
    s.rect(320, 0, 1360, 460, fill="none", stroke=RULE, sw=2)
    s.add(f'<path d="M320 52 V0 H372 M1628 0 H1680 V52 M1680 408 V460 H1628 M372 460 H320 V408" fill="none" stroke="{BLUE}" stroke-width="5"/>')
    s.text(352, 46, "하네스", size=32, weight=800, fill=BLUE)
    cells = [("컨텍스트", "rules.md", "무엇을 읽힐까"), ("도구", "read_file", "무엇을 쓸까"),
             ("실행 위치", "작업 폴더", "어디서 돌까"), ("상태", "handoff.md", "무엇을 남길까"),
             ("검증", "checklist.md", "무엇으로 끝낼까")]
    for i, (t, f, q) in enumerate(cells):
        x = 352 + i * 262
        last = i == 4
        s.rect(x, 90, 240, 240, fill=BLUE_SOFT if last else WHITE, stroke=BLUE if last else INK, sw=3.5 if last else 2)
        s.text(x + 120, 140, t, size=32, weight=800, anchor="middle")
        s.text(x + 120, 210, f, size=24, fill=BLUE, anchor="middle", mono=not f.startswith("작업"))
        s.text(x + 120, 280, q, size=24, fill=MUTED, anchor="middle")
    s.text(352, 400, "파일이 폴더에 있는 것만으로는 틀이 아니다. 읽히고 확인되는 경로까지 정한다.", size=28, fill=INK2)
    theme, body = term_top(1, 4, "하네스",
                           "모델이 안정적으로 일하도록 컨텍스트, 도구와 실행 위치, 상태 저장, 검증 절차를 묶은 작업 틀 전체. 이 워크숍의 정의이며 제품마다 범위가 다를 수 있다.",
                           "검토자가 체크리스트 파일을 폴더에 넣고 검토를 시작한다.", "파일이 폴더에 있으면 검토 틀이 갖춰진 걸까?",
                           s.render(), "하네스는 틀이고, 오케스트레이션은 그 안의 순서와 역할 배정이다. 런타임은 실행을 잇는 층이다.")
    return dict(kind="term", term="하네스", term_index=4, chapter=1, v10=[6], label="용어 4 하네스",
                theme=theme, body=body, layout="boundary")


# ---------------------------------------------------------------- 9 case OpenClaw (S7)

def s9():
    s = Svg("s9", 120, 370, 1680, 570, "OpenClaw 요청 흐름: 요청, 게이트웨이와 세션, 코디네이터, 직접 도구 또는 원격 워커, 파일과 테스트, 부모 검증, 답장")
    s.rect(0, 0, 1680, 570, fill="none", stroke=RULE, sw=2)
    s.add(f'<path d="M0 48 V0 H48 M1632 0 H1680 V48 M1680 522 V570 H1632 M48 570 H0 V522" fill="none" stroke="{BLUE}" stroke-width="5"/>')
    s.text(32, 40, "하네스: 이 구조 전체", size=28, weight=800, fill=BLUE)
    sm = {"size": 24, "weight": 400, "fill": INK2}
    s.box(40, 130, 250, 120, ["요청", ("Discord, Control UI", sm)], size=32, weight=800)
    s.box(350, 130, 270, 120, ["게이트웨이", ("채널과 세션", sm)], size=32, weight=800)
    s.box(680, 130, 300, 120, ["코디네이터", ("직접 할까, 맡길까", {"size": 24, "weight": 400, "fill": WHITE})],
          size=32, weight=800, fill=BLUE, stroke=BLUE, color=WHITE)
    s.box(1060, 70, 280, 110, ["직접 도구", ("조회, 단순 편집", sm)], size=30, weight=800)
    s.box(1060, 250, 280, 120, ["원격 워커", ("Codex 또는 Claude", sm)], size=30, weight=800)
    s.box(1400, 250, 240, 120, ["프로젝트", "파일과 테스트"], size=28, weight=800)
    s.box(1400, 430, 240, 110, ["부모의", "독립 검증"], size=28, weight=800, stroke=BLUE, sw=4)
    s.box(1060, 430, 280, 110, ["답장", ("요약과 로그 경로", sm)], size=30, weight=800)
    s.box(560, 430, 400, 110, ["원격 앱", ("같은 워커를 보고 개입", sm)], size=30, weight=800, stroke=MUTED, dash="9 7")
    s.arrow([(290, 190), (344, 190)])
    s.arrow([(620, 190), (674, 190)])
    s.arrow([(980, 165), (1020, 165), (1020, 125), (1054, 125)], color="blue")
    s.arrow([(980, 215), (1020, 215), (1020, 310), (1054, 310)], color="blue")
    s.arrow([(1340, 310), (1394, 310)])
    s.arrow([(1340, 125), (1520, 125), (1520, 244)])
    s.arrow([(1520, 370), (1520, 424)])
    s.arrow([(1400, 485), (1346, 485)])
    s.arrow([(760, 430), (760, 400), (1200, 400), (1200, 376)], color="muted", dash="9 7")
    tag = {"size": 24, "weight": 700, "fill": BLUE}
    s.text(485, 280, "세션은 4장", **tag, anchor="middle")
    s.text(830, 280, "모델이 판단하고 반복", **tag, anchor="middle")
    s.text(1200, 214, "런타임이 실행", **tag, anchor="middle")
    s.text(1310, 400, "워커는 4장", **tag, anchor="start")
    theme = "t-paper"
    body = "\n  ".join([
        case_head(1, "OpenClaw"),
        p("qline case-q", '<b>질문</b>디스코드에서 "보고서 검증해 줘"가 왔다. 받는 쪽, 맡기는 쪽, 확인하는 쪽은 누구일까?'),
        p("case-title", "요청을 받고, 맡기고, 따로 확인하는 작업 구조", "h2"),
        s.render(),
        p("foot", "운영 문서 기준의 가상 예시이며 실시간 상태는 확인하지 않았다. 위임 기준은 운영 지침이지 자동 라우터가 아니다. 모델 추론 위치는 따로 본다.",
          style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    return dict(kind="case", case="OpenClaw", case_index=1, chapter=1, v10=[7], label="사례 1 OpenClaw",
                theme=theme, body=body, layout="case")


# ---------------------------------------------------------------- 10 chapter 2

def s10():
    theme, body = chapter(10, 2, ["일하는 방법을", "어디에 담을까?"],
                          "역할과 순서, 실행되는 기능, 다시 쓰는 절차를 나눈다. 그다음 설치와 연결을 맡는 부품을 구분하고, 두 사례에서 확인한다.",
                          25, [("오케스트레이션", "term"), ("도구", "term"), ("스킬", "term"), ("OMH", "case"),
                               ("플러그인", "term"), ("커넥터", "term"), ("MCP", "term"), ("Grokbot", "case")])
    notes = '''<p>질문: 일하는 방법을 어디에 담을까?</p>
<p>순서: 오케스트레이션(3분), 도구(3분), 스킬(3분), 사례 OMH(5분), 플러그인(2분), 커넥터(2분), MCP(3분), 사례 Grokbot(3분). 전환 1분을 더해 약 25분이다.</p>
<p>왜 이 순서인가: 먼저 누가 언제 무엇을 하는지(오케스트레이션), 실제로 실행되는 기능(도구), 다시 쓰는 절차(스킬)를 나눈다. OMH에서 이 셋을 바꾼 사례를 본 뒤, 포장(플러그인), 외부 연결(커넥터), 통신 규약(MCP)을 구분하고 Grokbot 설명으로 비교한다.</p>
<p>플러그인과 커넥터는 앞의 개념에 기대므로 2분으로 짧게 간다. 강사용 보충 예시는 필요할 때만 쓴다.</p>'''
    return dict(kind="chapter", label="2장 일하는 방법을 어디에 담을까?", theme=theme, body=body, notes=notes)


# ---------------------------------------------------------------- 11 orchestration (S8): swimlanes

def s11():
    s = Svg("s11", 120, 440, 1680, 460, "기획, 실행, 검토 세 레인과 전환 조건")
    lanes = ["기획", "실행", "검토"]
    for i, name in enumerate(lanes):
        y = i * 160
        s.rect(0, y, 1680, 140, fill=BLUE_SOFT if i == 1 else PAPER2)
        if i == 1:
            s.rect(0, y, 10, 140, fill=BLUE)
        s.text(36, y + 70, name, size=32, weight=800, fill=BLUE if i == 1 else INK)
    s.box(220, 25, 300, 90, "안건 목록", size=30, weight=800)
    s.box(660, 185, 300, 90, "준비 초안", size=30, weight=800, stroke=BLUE, sw=3.5)
    s.box(1100, 345, 300, 90, "체크 결과", size=30, weight=800)
    s.arrow([(520, 70), (590, 70), (590, 230), (654, 230)])
    s.text(610, 150, "안건이 정해지면", size=26, weight=700, fill=INK2)
    s.arrow([(960, 230), (1030, 230), (1030, 390), (1094, 390)])
    s.text(1050, 256, "초안이 저장되면", size=26, weight=700, fill=INK2)
    s.arrow([(1250, 345), (1250, 300), (810, 300), (810, 281)], color="amber", dash="10 8")
    s.text(1010, 344, "빠진 항목이 있으면", size=26, weight=800, fill=AMBER, anchor="end")
    s.lines(1420, 70, ["누가, 무엇을, 언제", "넘기는지 정한다"], size=26, fill=MUTED, lh=1.4)
    theme, body = term_top(2, 5, "오케스트레이션",
                           "여러 단계나 실행 주체에 순서, 입출력, 역할, 다음 단계로 넘어가는 조건을 배정하고 조율하는 일.",
                           "회의 준비에 안건 초안, 확인, 최종 정리가 필요하다. 맡을 사람은 아직 없다.",
                           "맡는 사람이 정해지지 않으면 같은 일을 두 번 할까?", s.render(),
                           "역할을 나눴다고 독립 검토자가 생기지 않는다. 단일 에이전트 안의 단계 배정도 오케스트레이션이다.")
    return dict(kind="term", term="오케스트레이션", term_index=5, chapter=2, v10=[8], label="용어 5 오케스트레이션",
                theme=theme, body=body, layout="lane")


# ---------------------------------------------------------------- 12 tool (S9): executable card vs memo

def s12():
    s = Svg("s12", 120, 440, 1680, 460, "실행되는 도구 카드와 실행되지 않는 절차 메모의 비교")
    s.rect(0, 0, 780, 380, fill=WHITE, stroke=INK, sw=2.5)
    s.rect(0, 0, 780, 76, fill=INK)
    s.text(32, 38, "list_files", size=34, weight=700, fill=WHITE, mono=True)
    s.text(748, 38, "도구", size=26, weight=800, fill="#BFD3FF", anchor="end")
    for i, (k, v) in enumerate([("설명", "폴더의 파일 목록을 가져온다"), ("입력", "folder, sort"),
                                ("결과", "파일 이름 목록, 또는 오류")]):
        y = 124 + i * 58
        s.text(32, y, k, size=26, weight=800, fill=MUTED)
        s.text(140, y, v, size=30, mono=(k == "입력"))
    s.line(32, 280, 748, 280, color=RULE, sw=2)
    s.text(32, 330, "list_files(folder=meetings, sort=date)", size=26, fill=BLUE, mono=True)
    s.check(0, 412, True, 44)
    s.text(64, 434, "실행되는 기능. 모델이 요청하고 런타임이 실행한다.", size=30, weight=800, fill=BLUE)
    s.add(f'<path d="M900 0 H1640 L1680 40 V380 H900 Z" fill="{WHITE}" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="10 8"/>')
    s.text(932, 50, "찾는 순서 메모", size=30, weight=800, fill=INK2)
    for i, t in enumerate(["meetings 폴더를 연다", "날짜순으로 정렬한다", "최근 파일부터 적는다"]):
        y = 124 + i * 58
        s.text(932, y, str(i + 1), size=30, weight=800, fill=MUTED)
        s.text(980, y, t, size=30, fill=INK2)
    s.line(932, 280, 1648, 280, color=RULE, sw=2)
    s.text(932, 330, "읽으면 이해되지만, 스스로 하지는 않는다", size=28, fill=MUTED)
    s.check(900, 412, False, 44)
    s.text(964, 434, "절차다. 실행하는 수단이 있어야 결과가 생긴다.", size=30, weight=800, fill=AMBER)
    theme, body = term_top(2, 6, "도구",
                           "모델이 요청하고 런타임이 실행하는, 이름과 입력 형식과 결과 형식이 정해진 호출 가능한 기능.",
                           "폴더에서 최근 회의 파일 목록을 만든다.", "목록을 가져오는 기능과 찾는 순서 메모, 무엇이 실행될까?",
                           s.render(), '"날짜를 ISO 형식으로 바꾼다"는 절차다. 그 변환을 실행하는 호출이 도구다. MCP는 도구를 잇는 규약이다.')
    return dict(kind="term", term="도구", term_index=6, chapter=2, v10=[9], label="용어 6 도구",
                theme=theme, body=body, layout="compare")


# ---------------------------------------------------------------- 13 skill (S10): folder tree, mirrored

def s13():
    s = Svg("s13", 120, 120, 1020, 780, "스킬 폴더 구조: 절차 설명, 체크리스트, 출력 형식, 선택 스크립트")
    s.rect(30, 30, 56, 40, fill=BLUE)
    s.text(110, 50, "report-skill/", size=36, weight=700, mono=True)
    s.line(58, 90, 58, 520, color=INK, sw=3)
    rows = [("절차 설명 파일", "행 수, 중복, 모호 행, 보고서, 대조 순서", False),
            ("checklist.md", "끝났는지 대조할 항목", True),
            ("schema.md", "출력 형식", True),
            ("scripts/  (선택)", "보조 스크립트", True)]
    for i, (name, desc, mono) in enumerate(rows):
        y = 170 + i * 118
        s.line(58, y, 110, y, color=INK, sw=3)
        if i == 3:
            s.rect(122, y - 18, 44, 34, fill=BLUE)
        else:
            s.rect(124, y - 26, 38, 50, fill=WHITE, stroke=INK, sw=2.5)
        s.text(190, y - 12, name, size=32, weight=800, mono=mono and i < 3)
        s.text(190, y + 30, desc, size=26, fill=MUTED)
    s.rect(560, 430, 420, 120, fill=AMBER_SOFT, stroke=AMBER, sw=2.5, dash="9 7")
    s.lines(770, 490, ["실행은 런타임과", "도구가 맡는다"], size=30, weight=800, fill=AMBER, anchor="middle")
    s.arrow([(440, 524), (554, 524)], color="amber", dash="9 7")
    s.rect(30, 640, 990, 110, fill=PAPER2)
    s.text(60, 695, "입력", size=26, weight=800, fill=MUTED)
    s.text(140, 695, "새 주간 CSV와 이 묶음", size=30, weight=700)
    s.arrow([(500, 695), (566, 695)], color="blue")
    s.text(590, 695, "출력", size=26, weight=800, fill=MUTED)
    s.text(670, 695, "같은 형식의 요약", size=30, weight=700)
    theme, body = term_split(2, 7, "스킬",
                             "특정 작업의 절차, 입력과 출력 규칙, 필요한 자원을 묶어 다시 쓸 수 있게 만든 지침 묶음.",
                             "주간 고객 문의 요약을 매주 같은 순서로 만든다.", "그 순서를 묶어 둔 것을 무엇이라 부를까?",
                             s.render(), "스킬은 도구가 아니며 스스로 실행되지 않는다. 플러그인은 스킬 등을 배포하는 포장이다.",
                             mirror=True)
    return dict(kind="term", term="스킬", term_index=7, chapter=2, v10=[10], label="용어 7 스킬",
                theme=theme, body=body, layout="split-mirror")


# ---------------------------------------------------------------- 14 case OMH (S11)

def s14():
    body = '''<p class="abs kicker case-head"><span class="tag-case">사례 2 / 5</span>OMH</p>
  <p class="abs qline case-q"><b>질문</b>모델만 더 좋은 것으로 바꾸면 이 일이 해결될까?</p>
  <h2 class="abs case-title">모델은 그대로 두고, 일하는 틀을 바꿨다</h2>
  <div class="abs omh-left">
    <p class="col-lab">현장 제약</p>
    <ol>
      <li><span>1</span>오프라인 설치만</li>
      <li><span>2</span>로컬 파일만</li>
      <li><span>3</span>설정된 모델 하나</li>
    </ol>
  </div>
  <div class="abs omh-stack">
    <div class="slab slab-add">
      <p class="slab-lab">추가한 것: 업무 도구와 절차</p>
      <div class="chips">
        <div class="chip"><code>data_inspect</code><span>구조 점검</span></div>
        <div class="chip"><code>data_compare</code><span>키 기준 비교</span></div>
        <div class="chip"><code>omh-rigorous</code><span>선택형 절차</span></div>
      </div>
    </div>
    <div class="slab slab-keep"><b>유지</b><span>OpenCode와 OMO의 기존 역할</span></div>
    <div class="slab slab-keep"><b>유지</b><span>설정된 단일 모델, 재학습 없음</span></div>
  </div>
  <div class="abs omh-right">
    <p class="col-lab">확인 가능한 증거</p>
    <div class="ev"><svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><rect x="1" y="1" width="32" height="32" fill="#E1E9F6"/><path d="M8 17 L14.5 23.5 L26 10" fill="none" stroke="#2457A6" stroke-width="4"/></svg><span>설치와 점검 기록</span></div>
    <div class="ev"><svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><rect x="1" y="1" width="32" height="32" fill="#E1E9F6"/><path d="M8 17 L14.5 23.5 L26 10" fill="none" stroke="#2457A6" stroke-width="4"/></svg><span>모의 환경 테스트</span></div>
    <div class="ev warn"><svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><rect x="1" y="1" width="32" height="32" fill="#FBECDB"/><path d="M17 7 V20" stroke="#B45309" stroke-width="4"/><circle cx="17" cy="26" r="2.6" fill="#B45309"/></svg><span>사내 모델 품질은 미검증</span></div>
    <p class="ev-note">모의, 오프라인 점검은 기능이 연결됐다는 증거다. 실제 사내 모델의 품질을 보여 주지 않는다.</p>
  </div>
  <div class="abs omh-flow">
    <span class="lab">가상 예시</span>
    <span class="step">새 CSV</span><span class="arr">→</span>
    <span class="step">구조 점검<small>행 값 없이</small></span><span class="arr">→</span>
    <span class="step">변경</span><span class="arr">→</span>
    <span class="step">키 기준 비교<small>자동 병합 없음</small></span>
  </div>'''
    return dict(kind="case", case="OMH", case_index=2, chapter=2, v10=[11], label="사례 2 OMH",
                theme="t-paper", body=body, layout="case")


# ---------------------------------------------------------------- 15 plugin (S12): package, then separate gates

def s15():
    s = Svg("s15", 120, 440, 1680, 460, "플러그인 포장 안의 세 칸과, 설치 뒤에 따로 남는 인증과 권한 단계")
    s.rect(0, 0, 820, 400, fill=WHITE, stroke=INK, sw=4)
    s.rect(0, 0, 820, 70, fill=INK)
    s.text(30, 35, "플러그인", size=30, weight=800, fill=WHITE)
    s.text(790, 35, "설치하고 버전으로 관리하는 묶음", size=24, fill="#BFD3FF", anchor="end")
    for i, (t, sub) in enumerate([("스킬", "쓰기 지침"), ("도구 설정", "서식 기능"), ("커넥터 설정", "계정 연결 정보")]):
        x = 30 + i * 260
        s.box(x, 110, 240, 190, [t, (sub, {"size": 24, "weight": 400, "fill": MUTED})], size=30, weight=800,
              fill=PAPER2, stroke=None)
    s.text(30, 350, "일부 또는 전부가 들어 있을 수 있다. 구조는 제품마다 다르다.", size=26, fill=MUTED)
    s.arrow([(820, 120), (934, 120)])
    steps = [("설치", "포장을 가져온다", True), ("계정 인증", "따로 한다", None), ("권한 허용", "따로 확인한다", None)]
    for i, (t, sub, ok) in enumerate(steps):
        y = 70 + i * 120
        s.check(940, y + 6, ok, 48)
        s.text(1010, y + 30, t, size=34, weight=800, fill=INK if ok else AMBER)
        s.text(1220, y + 30, sub, size=30, fill=INK2)
        if i < 2:
            s.line(964, y + 62, 964, y + 118, color=RULE, sw=3)
    s.text(940, 20, "설치 뒤에도 남는 단계", size=26, weight=800, fill=MUTED)
    theme, body = term_top(2, 8, "플러그인",
                           "여러 기능, 지침, 설정을 한 번에 설치하고 버전으로 관리하려고 배포하는 패키지 단위. 범위와 설치 방식은 제품마다 다르다.",
                           "쓰기 지침, 서식 기능, 계정 연결 설정이 한 묶음으로 설치된다.", "계정 연결까지 끝난 걸까?",
                           s.render(), "MCP 서버 설정이 플러그인에 들어갈 수는 있지만 배포 단위와 통신 규약은 다른 층이다.")
    return dict(kind="term", term="플러그인", term_index=8, chapter=2, v10=[12], label="용어 8 플러그인",
                theme=theme, body=body, layout="boundary")


# ---------------------------------------------------------------- 16 connector (S13): chain to a service

def s16():
    s = Svg("s16", 120, 440, 1680, 460, "모델과 런타임에서 커넥터를 거쳐 외부 서비스로 가는 연결과 두 가지 결과")
    s.box(0, 40, 300, 170, ["모델과", "런타임"], size=32, weight=800)
    s.rect(380, 20, 840, 210, fill=BLUE_SOFT, stroke=BLUE, sw=3.5)
    s.text(410, 54, "커넥터", size=30, weight=800, fill=BLUE)
    for i, t in enumerate(["인증", "권한 범위", "대상 서비스"]):
        s.box(410 + i * 270, 90, 240, 110, t, size=30, weight=800)
    s.box(1300, 40, 380, 170, ["외부 서비스", ("캘린더", {"size": 26, "weight": 400, "fill": MUTED})], size=32,
          weight=800, stroke=MUTED, dash="9 7")
    s.arrow([(300, 125), (374, 125)])
    s.arrow([(1220, 125), (1294, 125)])
    s.check(380, 300, True, 48)
    s.text(448, 312, "연결과 권한이 살아 있으면", size=28, fill=INK2)
    s.text(448, 356, "일정 목록, 권한 범위만큼", size=32, weight=800, fill=BLUE)
    s.check(840, 300, False, 48)
    s.text(908, 312, "연결이 없거나 만료되면", size=28, fill=INK2)
    s.text(908, 356, "연결 오류", size=32, weight=800, fill=AMBER)
    s.lines(1300, 330, ["목록에 보이는 것과", "실제로 호출되는 것은 다르다.", "호출 결과로 확인한다."], size=26, fill=MUTED, lh=1.4)
    theme, body = term_top(2, 9, "커넥터",
                           "모델과 런타임이 외부 서비스, 데이터 저장소, 다른 앱의 기능에 닿도록 만든 연결 지점. 연결 설정과 인증 절차를 포함한다.",
                           "이번 주 회의 일정을 캘린더에서 가져와야 한다.", "AI가 캘린더를 바로 읽을 수 있을까?",
                           s.render(), "커넥터는 외부와의 연결 지점, 도구는 모델이 호출하는 기능이다. 커넥터 하나가 여러 도구를 노출할 수 있다.")
    return dict(kind="term", term="커넥터", term_index=9, chapter=2, v10=[13], label="용어 9 커넥터",
                theme=theme, body=body, layout="sequence")


# ---------------------------------------------------------------- 17 MCP (S14): protocol line

def s17():
    s = Svg("s17", 120, 440, 1680, 460, "호스트와 MCP 서버 사이의 세 가지 메시지, 그리고 규약과 접근 권한의 차이")
    s.box(0, 30, 420, 240, ["호스트", ("Claude Code 같은 앱", {"size": 26, "weight": 400, "fill": INK2}),
                            ("목록을 모델에 보여 준다", {"size": 24, "weight": 400, "fill": MUTED})], size=34, weight=800, lh=1.45)
    s.box(1260, 30, 420, 240, ["MCP 서버", ("도구와 자원을 노출", {"size": 26, "weight": 400, "fill": INK2})],
          size=34, weight=800, stroke=BLUE, sw=3.5, lh=1.45)
    s.text(840, 14, "공통 규약", size=26, weight=800, fill=BLUE, anchor="middle")
    for i, t in enumerate(["목록 조회", "도구 호출", "자원 읽기"]):
        y = 80 + i * 72
        s.arrow([(430, y + 20), (1250, y + 20)], color="blue", tail=True)
        s.rect(740, y + 2, 200, 36, fill="#F5F3EE")
        s.text(840, y + 20, t, size=28, weight=800, anchor="middle")
    s.line(0, 320, 1680, 320, color=RULE, sw=2)
    s.check(0, 360, True, 48)
    s.text(68, 372, "규약을 따른다", size=32, weight=800, fill=BLUE)
    s.text(68, 418, "메시지 형식과 교환 절차가 맞는다", size=28, fill=INK2)
    s.text(840, 395, "다른 문제", size=28, weight=800, fill=MUTED, anchor="middle")
    s.check(1060, 360, False, 48)
    s.text(1128, 372, "접근 권한을 얻었다", size=32, weight=800, fill=AMBER)
    s.text(1128, 418, "계정 연결과 허용 범위는 따로 정한다", size=28, fill=INK2)
    theme, body = term_top(2, 10, "MCP",
                           "Model Context Protocol. 호스트 앱과 외부 도구, 자원 서버가 도구 목록 조회, 도구 호출, 자원 읽기를 주고받는 방식을 정한 통신 규약.",
                           "여러 도구가 파일 목록과 내용을 같은 방식으로 주고받아야 한다.", "도구마다 따로 약속을 만들어야 할까?",
                           s.render(), "모든 도구가 MCP는 아니다. 로컬 함수나 셸 명령도 MCP 없이 도구가 된다.")
    return dict(kind="term", term="MCP", term_index=10, chapter=2, v10=[14], label="용어 10 MCP",
                theme=theme, body=body, layout="sequence")


# ---------------------------------------------------------------- 18 case Grokbot (S15)

def s18():
    axes = '''<div class="abs grok-axes">
    <p class="col-lab">네 개의 비교 축</p>
    <div class="axis first"><p class="axis-q"><span>1</span>누가 책임지는가?</p>
      <p class="axis-a"><b>Grokbot 설명</b>역할별 봇이 각자 책임을 나눈다</p>
      <p class="axis-a"><b>OpenClaw</b>코디네이터가 판단하고, 워커가 쓰고, 부모가 검증한다</p>
      <p class="axis-a"><b>CEO Agent</b>실무자가 반영 책임을 지고, 에이전트는 초안까지 낸다</p></div>
    <div class="axis"><p class="axis-q"><span>2</span>작업은 어디서 실행되는가?</p></div>
    <div class="axis"><p class="axis-q"><span>3</span>상태는 어디에 남는가?</p></div>
    <div class="axis"><p class="axis-q"><span>4</span>사람은 어디서 개입하는가?</p></div>
  </div>'''
    s = Svg("s18", 120, 390, 580, 560, "사용자가 설명한 패턴: 역할별 봇 네 개가 공유 환경과 커넥터, 루틴을 쓴다. 원자료 미확인")
    s.text(0, 14, "사용자가 설명한 패턴", size=26, weight=800, fill=MUTED)
    dash = "9 7"
    s.rect(170, 200, 240, 150, fill=BLUE_SOFT, stroke=BLUE, sw=3, dash=dash)
    s.lines(290, 275, ["공유 환경", ("클라우드, 설명상", {"size": 24, "weight": 400, "fill": INK2})], size=30,
            weight=800, anchor="middle", lh=1.45)
    for i, (x, y) in enumerate([(0, 60), (380, 60), (0, 400), (380, 400)]):
        s.box(x, y, 200, 90, f"역할 봇 {i + 1}", size=28, weight=800, stroke=MUTED, dash=dash)
        cx, cy = x + 100, (y + 90) if y < 200 else y
        tx, ty = (240 if x == 0 else 340), (200 if y < 200 else 350)
        s.line(cx, cy, tx, ty, color=MUTED, sw=2.5, dash="6 6")
    s.box(0, 245, 130, 60, "커넥터", size=26, weight=800, fill=PAPER2, stroke=None)
    s.box(450, 245, 130, 60, "루틴", size=26, weight=800, fill=PAPER2, stroke=None)
    s.line(130, 275, 170, 275, color=MUTED, sw=2.5, dash="6 6")
    s.line(410, 275, 450, 275, color=MUTED, sw=2.5, dash="6 6")
    s.rect(0, 506, 580, 54, fill=AMBER_SOFT)
    s.text(20, 533, "사용자 설명을 그린 것. 원자료 미확인", size=26, weight=800, fill=AMBER)
    left = s.render()
    body = "\n  ".join([
        case_head(3, "Grokbot"),
        p("qline case-q", "<b>질문</b>여러 봇이 역할을 나누고 공유 공간을 쓴다. 우리 팀에도 이런 구조가 맞을까?"),
        p("case-title", "봇의 수가 아니라, 책임과 위치를 비교한다", "h2"),
        left, axes,
        p("foot", "사용자 설명, 첨부 미확인, 패턴 비교만 한다. 제품 사양이나 성능 주장이 아니다.",
          style="left:120px;top:968px;width:1680px;margin:0;color:#B45309;font-weight:700"),
    ])
    return dict(kind="case", case="Grokbot", case_index=3, chapter=2, v10=[15], label="사례 3 Grokbot",
                theme="t-paper", body=body, layout="case")


# ---------------------------------------------------------------- 19 chapter 3

def s19():
    theme, body = chapter(19, 3, ["AI는 무엇을", "알고 있을까?"],
                          "이 업무의 맥락을 이해하려면, 이번 호출에 실제로 들어간 정보를 확인해야 한다. 지시, 입력, 단위와 한계, 저장과 불러오기를 본 뒤 AI교양 흐름에서 확인한다.",
                          20, [("프롬프트", "term", "지시와 제약"), ("컨텍스트", "term", "이번 호출의 입력"),
                               ("토큰", "term", "세는 단위"), ("컨텍스트 창", "term", "한 호출의 한계"),
                               ("메모리", "term", "저장과 불러오기"), ("AI교양", "case", "확정 게이트")])
    notes = '''<p>질문: AI는 무엇을 알고 있을까?</p>
<p>순서: 프롬프트(3분), 컨텍스트(3분), 토큰(2분), 컨텍스트 창(3분), 메모리(3분), 사례 AI교양(5분). 전환 1분을 더해 약 20분이다.</p>
<p>핵심 구분: 디스크에 있는 파일이 아니라, 이번 호출에 실제로 들어간 정보가 컨텍스트다. 모델은 학습으로 얻은 일반 지식도 갖고 있지만, 이 업무의 파일, 결정, 규칙은 입력에 들어가야 근거로 쓸 수 있다.</p>
<p>이 장이 끝나면 쉬는 시간 10분이다.</p>'''
    return dict(kind="chapter", label="3장 AI는 무엇을 알고 있을까?", theme=theme, body=body, notes=notes)


# ---------------------------------------------------------------- 20 prompt (S16): request A vs B

def s20():
    s = Svg("s20", 120, 440, 1680, 460, "한 줄 요청과 맥락을 더한 요청의 비교")
    for col, x in ((0, 0), (1, 900)):
        s.text(x, 14, "요청 A" if col == 0 else "요청 B", size=26, weight=800, fill=MUTED)
    s.box(0, 40, 780, 210, ['"회의 준비해 줘"'], size=34, weight=700)
    s.box(900, 40, 780, 210, ['"회의 준비해 줘"', ("+ 안건 세 줄", {"fill": BLUE}), ("+ 참석자 명단", {"fill": BLUE}),
                              ("+ 지난 회의 결정", {"fill": BLUE})], size=30, weight=700, stroke=BLUE, sw=3.5, lh=1.3)
    s.arrow([(390, 250), (390, 294)])
    s.arrow([(1290, 250), (1290, 294)], color="blue")
    s.box(0, 300, 780, 90, "일반적인 준비 목록", size=32, weight=800, fill=PAPER2, stroke=None)
    s.box(900, 300, 780, 90, "안건 중심 준비안", size=32, weight=800, fill=BLUE_SOFT, stroke=None)
    s.text(900, 436, "입력에 없는 사실은 여전히 확인이 필요하다", size=28, weight=700, fill=AMBER)
    s.text(0, 436, "모델은 빈 곳을 추측으로 채운다", size=28, fill=MUTED)
    theme, body = term_top(3, 11, "프롬프트",
                           "모델 입력 중 지시, 질문, 역할, 제약을 담은 부분. 한 번 쓰는 요청일 수도, 여러 실행에 반복되는 지속 지침일 수도 있다.",
                           '"회의 준비해 줘"와, 안건과 참석자와 지난 결정을 넣은 요청.', "어느 쪽이 결과를 더 좌우할까?",
                           s.render(), "프롬프트는 지시 문장이고, 컨텍스트는 실제로 입력된 전체다. 폴더의 규칙 파일은 읽혀야 입력이 된다.")
    return dict(kind="term", term="프롬프트", term_index=11, chapter=3, v10=[16], label="용어 11 프롬프트",
                theme=theme, body=body, layout="compare")


# ---------------------------------------------------------------- 21 context (S17): inside vs outside the call

def s21():
    s = Svg("s21", 120, 440, 1680, 460, "이번 호출에 들어간 입력과 디스크에만 있는 파일")
    s.rect(0, 0, 1060, 460, fill=BLUE_SOFT, stroke=BLUE, sw=4)
    s.text(30, 38, "이번 호출에 들어간 입력", size=30, weight=800, fill=BLUE)
    rows = ["지시: \"지난 결정 반영해서 회의 준비해 줘\"", "규칙 파일 내용", "tickets.csv 앞 20행", "도구 결과",
            "이전 대화 중 포함된 부분"]
    for i, t in enumerate(rows):
        y = 74 + i * 76
        s.rect(30, y, 1000, 62, fill=WHITE)
        s.text(56, y + 31, t, size=28, weight=700)
    s.text(1140, 38, "디스크에만 있는 것", size=30, weight=800, fill=MUTED)
    for i, t in enumerate(["지난 회의록 내용", "checklist.md", "tickets.csv 21행부터"]):
        y = 74 + i * 90
        s.rect(1140, y, 540, 70, fill="none", stroke=MUTED, sw=2.5, dash="9 7")
        s.text(1168, y + 35, t, size=28, fill=INK2, mono=(i == 1))
    s.arrow([(1140, 380), (1066, 380)], color="blue", dash="9 7")
    s.lines(1160, 400, ["읽어서 넣어야", "모델이 안다"], size=26, weight=800, fill=BLUE, lh=1.35)
    theme, body = term_top(3, 12, "컨텍스트",
                           "특정 호출에서 모델이 실제로 입력받은 모든 내용. 지시, 파일 내용, 도구 결과, 이전 대화 중 포함된 부분이 여기에 들어간다.",
                           "지난 회의록의 경로만 알려 주고 내용은 넣지 않았다.", "AI는 지난 결정을 떠올릴 수 있을까?",
                           s.render(), "메모리는 나중에 불러오려고 저장한 정보, 컨텍스트는 지금 입력에 들어 있는 정보다.")
    return dict(kind="term", term="컨텍스트", term_index=12, chapter=3, v10=[17], label="용어 12 컨텍스트",
                theme=theme, body=body, layout="boundary")


SLIDES_A = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21]
