"""Slides 22 to 42 of the v02 deck: end of chapter 3, break, chapters 4 and 5, closing."""

from deck_a import chapter, term_split, term_top
from kit import (AMBER, AMBER_SOFT, BLUE, BLUE_SOFT, INK, INK2, MUTED, PAPER2, RULE, WHITE, Svg,
                 case_head, e, p)

# ---------------------------------------------------------------- 22 token (S18): a sentence cut into pieces


def s22():
    s = Svg("s22", 120, 440, 1680, 460, "같은 안내 문장을 한국어와 영어로 나눈 가상의 토큰 분할")
    rows = [("한국어", ["안내", "메일", "을", "보내", "드립니다"]),
            ("영어", ["We", "'ll", " send", " the", " notice"])]
    for r, (lab, chunks) in enumerate(rows):
        y = 40 + r * 150
        s.text(0, y + 50, lab, size=28, weight=800, fill=MUTED)
        x = 150
        for i, c in enumerate(chunks):
            latin = lab == "영어"
            w = round(len(c.strip() or c) * (34 if latin else 56) + 44)
            s.rect(x, y, w, 100, fill=BLUE_SOFT if i % 2 == 0 else PAPER2, stroke=BLUE if i % 2 == 0 else None, sw=2)
            s.text(x + w / 2, y + 50, c.strip(), size=52, weight=700, anchor="middle")
            x += w + 10
    s.rect(0, 360, 640, 64, fill=AMBER_SOFT)
    s.text(24, 392, "위 분할은 설명용 가상 예시다", size=28, weight=800, fill=AMBER)
    s.line(1060, 20, 1060, 430, color=RULE, sw=2)
    s.lines(1110, 120, ["글자 수가 같아도", "토큰 수는 다를 수 있다"], size=42, weight=800, lh=1.3)
    s.lines(1110, 300, ["언어별 보편 비율은 없다.", "정확한 수는 해당 모델의", "계산 방식으로 확인한다."], size=28, fill=INK2, lh=1.4)
    theme, body = term_top(3, 13, "토큰",
                           "모델이 입력과 출력을 처리할 때 세는 텍스트 조각의 단위. 단어 수나 글자 수와 같지 않다.",
                           "같은 안내 메일을 한국어와 영어로 준비한다.", "글자 수가 같으면 토큰 수도 같을까?",
                           s.render(), "토큰은 측정 단위이고, 컨텍스트 창은 그 단위로 잰 한계다. 이 워크숍에서는 개수를 추정하지 않는다.")
    return dict(kind="term", term="토큰", term_index=13, chapter=3, v10=[18], label="용어 13 토큰",
                theme=theme, body=body, layout="typographic")


# ---------------------------------------------------------------- 23 context window (S19): one bar, one limit

def s23():
    s = Svg("s23", 120, 440, 1680, 460, "한 호출의 창 안에 지시, 파일, 이전 대화, 출력 공간이 함께 들어가는 막대")
    s.text(0, 20, "한 번의 호출", size=26, weight=800, fill=MUTED)
    segs = [(0, 200, "지시", BLUE_SOFT), (200, 760, "규칙과 문서", "#C9D8F0"), (760, 1180, "이전 대화", PAPER2)]
    for x0, x1, t, f in segs:
        s.rect(x0, 60, x1 - x0, 130, fill=f, stroke=INK, sw=2)
        s.text((x0 + x1) / 2, 125, t, size=32, weight=800, anchor="middle")
    s.rect(1180, 60, 320, 130, fill=WHITE, stroke=INK, sw=2, dash="9 7")
    s.text(1340, 125, "출력 공간", size=32, weight=800, fill=INK2, anchor="middle")
    s.line(1500, 30, 1500, 230, color=AMBER, sw=6)
    s.text(1520, 50, "창의 한계", size=28, weight=800, fill=AMBER)
    s.lines(1520, 140, ["입력이 차면", "출력 공간이 준다"], size=26, fill=INK2, lh=1.35)
    s.arrow([(970, 196), (970, 290)], color="amber")
    s.box(760, 296, 420, 80, "요약본", size=30, weight=800, fill=AMBER_SOFT, stroke=AMBER, sw=2.5)
    s.lines(990, 430, ["압축: 이전 대화를 요약한다. 세부 일부가 사라질 수 있다."], size=26, fill=AMBER, anchor="middle")
    s.lines(0, 340, ["나눠서 넣기", ("장별로 넣고, 장마다 메모를 저장한다", {"size": 26, "weight": 400, "fill": INK2})],
            size=30, weight=800, lh=1.5)
    theme, body = term_top(3, 14, "컨텍스트 창",
                           "모델이 한 번의 호출에서 입력과 출력을 함께 처리할 수 있는 토큰 범위의 한계. 크기는 모델과 제품 설정마다 다르다.",
                           "100쪽 계약 문서를 한 번에 넣고 검토를 맡긴다.", "앞부분 내용도 끝까지 기억될까?",
                           s.render(), "압축은 창에 넣는 내용의 분량을 줄이는 일이다. 창의 크기는 그대로다. 메모리는 호출 밖에 저장했다가 다시 불러오는 일이다.")
    return dict(kind="term", term="컨텍스트 창", term_index=14, chapter=3, v10=[19], label="용어 14 컨텍스트 창",
                theme=theme, body=body, layout="typographic")


# ---------------------------------------------------------------- 24 memory (S20): yesterday, store, today

def s24():
    s = Svg("s24", 120, 440, 1680, 460, "어제 저장한 인계 파일이 오늘 읽힐 때와 읽히지 않을 때")
    s.text(0, 14, "어제", size=26, weight=800, fill=MUTED)
    s.text(920, 14, "오늘, 새 대화", size=26, weight=800, fill=MUTED)
    s.box(0, 70, 340, 140, ["어제 세션", ("회의 날짜를 정했다", {"size": 26, "weight": 400, "fill": INK2})], size=32, weight=800)
    s.rect(430, 50, 400, 300, fill=PAPER2)
    s.text(460, 90, "저장소", size=30, weight=800)
    s.box(460, 130, 340, 70, "인계 파일", size=28, weight=700)
    s.box(460, 220, 340, 70, "기록 파일", size=28, weight=700)
    s.arrow([(340, 140), (424, 140)])
    s.text(382, 112, "저장", size=24, weight=800, fill=MUTED, anchor="middle")
    s.lines(430, 405, ["자동으로 전부 불러오지 않는다", "모델의 가중치는 변하지 않는다"], size=26, fill=MUTED, lh=1.4)
    s.box(920, 60, 360, 120, ["읽지 않고", "\"날짜가 언제였지?\""], size=28, weight=700)
    s.box(1340, 60, 340, 120, '"모른다"', size=32, weight=800, stroke=AMBER, sw=3, color=AMBER)
    s.arrow([(1280, 120), (1334, 120)], color="amber")
    s.box(920, 240, 360, 120, ["인계 파일을 읽고", "\"날짜가 언제였지?\""], size=28, weight=700, stroke=BLUE, sw=3.5)
    s.box(1340, 240, 340, 120, ["어제 결정을", "근거로 답한다"], size=30, weight=800, fill=BLUE_SOFT, stroke=BLUE, sw=3)
    s.arrow([(1280, 300), (1334, 300)], color="blue")
    s.arrow([(800, 165), (870, 165), (870, 300), (914, 300)], color="blue")
    s.text(886, 228, "읽기", size=24, weight=800, fill=BLUE)
    theme, body = term_top(3, 15, "메모리",
                           "세션이나 실행이 끝난 뒤에도 다시 불러올 수 있게 파일이나 저장소에 남긴 정보. 모델의 가중치는 바꾸지 않는다.",
                           "어제 정한 회의 날짜를 인계 파일에 적었다.", "오늘 새 대화를 열면 그 결정이 따라올까?",
                           s.render(), "세션이 이어진다고 메모리가 생기지는 않는다. 재학습도 아니다. 입력에 무엇이 들어가는지만 달라진다.")
    return dict(kind="term", term="메모리", term_index=15, chapter=3, v10=[20], label="용어 15 메모리",
                theme=theme, body=body, layout="sequence")


# ---------------------------------------------------------------- 25 case AI교양 (S21)

def s25():
    s = Svg("s25", 120, 360, 1680, 580, "AI교양 네 단계 흐름과 그 주변의 규칙, 컨텍스트, 도구, 상태, 검증")
    cells_top = [("규칙", "원문 보존과 버전, 확정 문장 불변"), ("컨텍스트", "해당 글, 수정 이력, 관련 근거"),
                 ("도구", "파일 저장, 이미지 생성, 초안 작성")]
    for i, (t, d) in enumerate(cells_top):
        x = i * 570
        s.rect(x, 0, 540, 120, fill=PAPER2)
        s.text(x + 28, 38, t, size=28, weight=800, fill=BLUE)
        s.text(x + 28, 84, d, size=26, fill=INK2)
    cells_bot = [("상태", "현재 버전, 확정 여부, 단계별 결과, 초안 식별자"), ("검증", "저장본 대조, 초안 재열람")]
    for i, (t, d) in enumerate(cells_bot):
        x = i * 855
        s.rect(x, 440, 825, 120, fill=PAPER2)
        s.text(x + 28, 478, t, size=28, weight=800, fill=BLUE)
        s.text(x + 28, 524, d, size=26, fill=INK2)
    s.box(0, 220, 290, 130, ["원문 보존", ("v01과 인덱스", {"size": 24, "weight": 400, "fill": INK2})], size=30, weight=800)
    s.box(350, 220, 290, 130, ["수정과 확인", ("새 버전, 이전 본 보존", {"size": 24, "weight": 400, "fill": INK2})],
          size=30, weight=800)
    s.add('<polygon points="830,170 950,285 830,400 710,285" fill="#FBECDB" stroke="#B45309" stroke-width="3.5"/>')
    s.lines(830, 285, ["사용자", "최종 확정"], size=28, weight=800, fill=AMBER, anchor="middle")
    s.box(1020, 220, 380, 130, ["삽화, 보관,", "비공개 초안, 재열람"], size=30, weight=800, stroke=BLUE, sw=3.5)
    s.box(1460, 220, 220, 130, ["공개 발행", "범위 밖"], size=28, weight=800, fill="none", stroke=AMBER, sw=2.5,
          dash="9 7", color=AMBER)
    s.arrow([(290, 285), (344, 285)])
    s.arrow([(640, 285), (704, 285)])
    s.arrow([(950, 285), (1014, 285)], color="amber")
    s.text(984, 254, "예", size=24, weight=800, fill=AMBER, anchor="middle")
    s.arrow([(830, 400), (830, 422), (495, 422), (495, 356)], color="amber", dash="9 7")
    s.text(690, 396, "아니오: 다시 수정", size=24, weight=800, fill=AMBER, anchor="end")
    s.text(830, 150, "사람이 정한다", size=24, weight=800, fill=AMBER, anchor="middle")
    body = "\n  ".join([
        case_head(4, "AI교양"),
        p("qline case-q", "<b>질문</b>최종본이 확정되기 전에 삽화부터 만들자는 요청이 왔다. 만들어도 될까?"),
        p("case-title", "흐름을 받치는 장치까지 보면 업무용 하네스다", "h2"),
        s.render(),
        p("foot", "완료 기록의 설명용 인용이며, 이번 작업으로 제작하지 않았다. 별도 상태 머신이 전환을 강제한다는 뜻은 아니다.",
          style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    return dict(kind="case", case="AI교양", case_index=4, chapter=3, v10=[21], label="사례 4 AI교양",
                theme="t-paper", body=body, layout="case")


# ---------------------------------------------------------------- 26 break (S22)

def s26():
    body = "\n  ".join([
        p("brk-word", "쉬는 시간", "h2"),
        p("brk-min", "10분"),
        '<div class="abs cover-rule" style="top:690px"></div>',
        p("brk-next", "돌아오면 4장<br><b>누가 이어서 일할까?</b>"),
        p("brk-done", "지금까지: 모델과 실행, 일하는 방법을 담는 곳, 모델이 아는 것"),
    ])
    notes = '''<p>쉬는 시간 10분. 시작 후 약 67분 지점이다.</p>
<p>돌아오면 4장에서 세션, 워커, 서브에이전트를 보고 CEO Agent 사례로 넘어간다.</p>'''
    return dict(kind="break", label="쉬는 시간", theme="t-night", body=body, notes=notes, v10=[22])


# ---------------------------------------------------------------- 27 chapter 4

def s27():
    theme, body = chapter(27, 4, ["누가 이어서", "일할까?"],
                          "대화를 묶는 단위, 실제로 일하는 주체, 맡겨진 하위 실행을 나눈다. 그다음 한 흐름 안에서 상황별 페르소나를 고르는 사례를 본다.",
                          13, [("세션", "term", "작업 맥락"), ("워커", "term", "실행 담당"),
                               ("서브에이전트", "term", "맡겨진 하위 실행"), ("CEO Agent", "case", "상황별 선택")])
    notes = '''<p>질문: 누가 이어서 일할까?</p>
<p>순서: 세션(3분), 워커(3분), 서브에이전트(3분), 사례 CEO Agent(3분). 전환 1분을 더해 약 13분이다.</p>
<p>핵심 구분: 세션은 작업 맥락이고, 워커는 실행 담당이다. 역할을 나눠도 독립 검증이 되지는 않는다.</p>'''
    return dict(kind="chapter", label="4장 누가 이어서 일할까?", theme=theme, body=body, notes=notes)


# ---------------------------------------------------------------- 28 session (S23): two screens, one session

def s28():
    s = Svg("s28", 120, 440, 1680, 460, "노트북과 휴대폰 두 화면이 같은 세션 하나를 보고, 파일은 워커가 고친다")
    s.rect(30, 20, 320, 190, fill=WHITE, stroke=INK, sw=3)
    s.lines(190, 115, ["노트북", ("메시지를 보낸다", {"size": 24, "weight": 400, "fill": INK2})], size=30, weight=800,
            anchor="middle", lh=1.5)
    s.add(f'<polygon points="0,214 380,214 360,238 20,238" fill="{INK}"/>')
    s.rect(90, 280, 200, 170, fill=WHITE, stroke=INK, sw=3)
    s.lines(190, 365, ["휴대폰", ("같은 답이", {"size": 24, "weight": 400, "fill": INK2}),
                       ("보인다", {"size": 24, "weight": 400, "fill": INK2})], size=30, weight=800, anchor="middle", lh=1.35)
    s.rect(540, 10, 560, 440, fill=BLUE_SOFT, stroke=BLUE, sw=4)
    s.text(570, 52, "세션 하나", size=32, weight=800, fill=BLUE)
    for i, t in enumerate(["대화 이력", "도구 기록", "상태 파일 링크"]):
        s.box(570, 100 + i * 110, 500, 86, t, size=30, weight=700)
    s.arrow([(380, 115), (534, 115)])
    s.arrow([(290, 365), (534, 365)])
    s.text(460, 90, "보기", size=24, weight=800, fill=MUTED, anchor="middle")
    s.text(420, 340, "보기", size=24, weight=800, fill=MUTED, anchor="middle")
    s.arrow([(1100, 230), (1294, 230)], color="blue")
    s.text(1196, 202, "실행은", size=24, weight=800, fill=BLUE, anchor="middle")
    s.box(1300, 150, 380, 160, ["워커 하나", ("파일을 고치는 주체", {"size": 26, "weight": 400, "fill": WHITE})],
          size=32, weight=800, fill=BLUE, stroke=BLUE, color=WHITE)
    s.text(1300, 370, "화면 두 개, 세션 하나", size=32, weight=800)
    s.text(1300, 416, "쓰기 주체는 하나여야 한다", size=26, fill=MUTED)
    theme, body = term_top(4, 16, "세션",
                           "하나의 작업 흐름을 묶어 두는 대화와 상태의 단위. 입력, 출력, 도구 기록, 진행 상태가 여기에 연결된다.",
                           "같은 회의 준비 대화를 노트북과 휴대폰에서 연다.", "같은 대화를 두 화면에서 보면 작업자도 두 명일까?",
                           s.render(), "세션은 실행 주체가 아니다. 세션에 저장된 이력 중 이번 호출에 들어간 부분만 컨텍스트다.")
    return dict(kind="term", term="세션", term_index=16, chapter=4, v10=[23], label="용어 16 세션",
                theme=theme, body=body, layout="boundary")


# ---------------------------------------------------------------- 29 worker (S24): permission boundary

def s29():
    s = Svg("s29", 770, 120, 1040, 760, "워커의 쓰기 허용 경계와 경계 밖의 쓰기 금지 파일")
    s.rect(300, 40, 720, 500, fill="none", stroke=BLUE, sw=3, dash="12 9")
    s.text(328, 80, "작업 지시상 범위: 문서 한 곳", size=28, weight=800, fill=BLUE)
    s.text(328, 120, "기술적 샌드박스가 아니다", size=24, weight=700, fill=MUTED)
    s.box(0, 220, 250, 170, ["작업 지시", ("고칠 부분 목록", {"size": 26, "weight": 400, "fill": INK2})],
          size=32, weight=800)
    s.box(360, 210, 300, 190, ["워커", ("고치기 담당", {"size": 26, "weight": 400, "fill": WHITE})], size=40,
          weight=800, fill=BLUE, stroke=BLUE, color=WHITE, lh=1.5)
    s.box(760, 230, 220, 150, ["고친", "문서"], size=32, weight=800)
    s.arrow([(250, 305), (354, 305)])
    s.arrow([(660, 305), (754, 305)], color="blue")
    s.text(328, 462, "실제 권한은 도구와 런타임 설정이 정한다.", size=26, weight=800, fill=AMBER)
    s.text(328, 504, "보고는 자기 보고다. 결과는 검증 단계가 판단한다.", size=24, fill=MUTED)
    s.box(0, 600, 330, 130, ["메모 담당", ("읽기만 한다", {"size": 26, "weight": 400, "fill": INK2})],
          size=30, weight=800, stroke=MUTED, dash="9 7")
    s.rect(560, 600, 460, 130, fill=AMBER_SOFT, stroke=AMBER, sw=3)
    s.check(590, 641, False, 48)
    s.text(664, 646, "tickets.csv", size=30, weight=700, mono=True)
    s.text(664, 690, "지시상 쓰기 금지", size=26, weight=800, fill=AMBER)
    theme, body = term_split(4, 17, "워커",
                             "배정받은 작업을 실제로 수행하는 실행 주체. 읽기 전용 조사인지 파일 수정인지에 따라 권한과 작업 범위가 달라진다.",
                             "한 사람은 고치기만, 다른 사람은 메모만 쓰기로 나뉘었다.", "문서를 실제로 고칠 담당은 누구로 정할까?",
                             s.render(), "워커는 맡은 일을 하는 역할이고, 서브에이전트는 상위와 하위의 위임 관계다. 하위 에이전트가 워커일 수 있다.")
    return dict(kind="term", term="워커", term_index=17, chapter=4, v10=[24], label="용어 17 워커",
                theme=theme, body=body, layout="split")


# ---------------------------------------------------------------- 30 subagent (S25): delegate and return, mirrored

def s30():
    s = Svg("s30", 120, 120, 1020, 780, "상위 작업이 하위 실행에 맡기고 결과를 돌려받는 흐름")
    s.box(40, 40, 440, 200, ["상위 작업", ("보고서를 쓴다", {"size": 26, "weight": 400, "fill": INK2})], size=36,
          weight=800, lh=1.5)
    s.rect(540, 320, 460, 280, fill=BLUE_SOFT, stroke=BLUE, sw=3.5)
    s.lines(770, 410, ["하위 실행", ("별도의 입력 맥락", {"size": 26, "weight": 400, "fill": INK2}),
                       ("용어 정의만 뽑는다", {"size": 26, "weight": 400, "fill": INK2})], size=36, weight=800,
            anchor="middle", lh=1.4)
    s.rect(560, 520, 420, 52, fill=AMBER_SOFT)
    s.text(770, 546, "읽기 전용 작업 지시 (이번 예시)", size=26, weight=800, fill=AMBER, anchor="middle")
    s.arrow([(480, 120), (770, 120), (770, 314)], color="blue")
    s.text(620, 92, "지시와 문서", size=26, weight=800, fill=BLUE, anchor="middle")
    s.arrow([(540, 440), (260, 440), (260, 246)])
    s.text(400, 412, "용어 목록", size=26, weight=800, anchor="middle")
    s.box(40, 560, 440, 120, ["원문", ("그대로 둔다", {"size": 26, "weight": 400, "fill": INK2})], size=32,
          weight=800, stroke=MUTED, dash="9 7")
    s.arrow([(540, 620), (486, 620)], color="muted", dash="8 6")
    s.text(40, 712, "지시만으로 실제 쓰기 권한이 사라지지는 않는다", size=26, weight=800, fill=INK2)
    s.text(40, 752, "같은 모델과 비슷한 맥락이면 오류가 겹칠 수 있다", size=26, weight=800, fill=AMBER)
    theme, body = term_split(4, 18, "서브에이전트",
                             "상위 작업이 맡긴 하위 작업을 별도의 입력 맥락에서 수행하고 결과를 돌려주는 하위 실행. 읽기 전용일 수도, 쓰기 권한이 있을 수도 있다.",
                             "긴 문서에서 용어 정의만 뽑는 일을 나눠 준다.", "그 작업자가 원문을 고쳐도 될까?",
                             s.render(), "오케스트레이션은 배정 방식이고, 서브에이전트는 실행 단위다. 서브에이전트가 있다고 독립 검토가 되지는 않는다.",
                             mirror=True)
    return dict(kind="term", term="서브에이전트", term_index=18, chapter=4, v10=[25], label="용어 18 서브에이전트",
                theme=theme, body=body, layout="split-mirror")


# ---------------------------------------------------------------- 31 case CEO Agent (S26)

def s31():
    body = '''<p class="abs kicker case-head"><span class="tag-case">사례 5 / 5</span>CEO Agent</p>
  <p class="abs qline case-q"><b>질문</b>같은 사실이라면 사내 보고와 외부 발언의 강조도 같아야 할까?</p>
  <h2 class="abs ceo-title">조사한 근거로 만든 페르소나를, 상황에 맞게 골라 쓴다</h2>
  <svg class="svg" style="left:120px;top:352px" width="1680" height="600" viewBox="0 0 1680 600" role="img" aria-label="조사에서 페르소나 명세로, 상황에서 선택과 결과로 이어지는 두 줄 흐름">
    <defs>
      <marker id="s31-ink" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0.5 L10,5 L0,9.5 z" fill="#14171C"/></marker>
      <marker id="s31-blue" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0.5 L10,5 L0,9.5 z" fill="#2457A6"/></marker>
      <marker id="s31-amber" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0.5 L10,5 L0,9.5 z" fill="#B45309"/></marker>
    </defs>
    <line x1="0" y1="282" x2="1680" y2="282" stroke="#CFCBC2" stroke-width="2"/>
    <g>
      <text x="0" y="60" font-size="34" font-weight="800" fill="#2457A6">조사</text>
      <text x="0" y="100" font-size="24" fill="#5E6570">근거에서 명세로</text>
      <text x="0" y="360" font-size="34" font-weight="800" fill="#2457A6">적용</text>
      <text x="0" y="400" font-size="24" fill="#5E6570">상황에서 결과로</text>
    </g>
    <g font-size="27" fill="#14171C">
      <path d="M200 16 H520 L540 36 V80 H200 Z" fill="#FFFFFF" stroke="#14171C" stroke-width="2"/><path d="M520 16 V36 H540" fill="none" stroke="#14171C" stroke-width="2"/>
      <text x="222" y="58">본인이 쓴 글과 서신</text>
      <path d="M200 96 H520 L540 116 V160 H200 Z" fill="#FFFFFF" stroke="#14171C" stroke-width="2"/><path d="M520 96 V116 H540" fill="none" stroke="#14171C" stroke-width="2"/>
      <text x="222" y="138">본인이 고친 초안의 변경</text>
      <path d="M200 176 H520 L540 196 V240 H200 Z" fill="#FFFFFF" stroke="#14171C" stroke-width="2"/><path d="M520 176 V196 H540" fill="none" stroke="#14171C" stroke-width="2"/>
      <text x="222" y="218">실제 피드백과 코멘트</text>
    </g>
    <polyline points="548,128 620,128" fill="none" stroke="#14171C" stroke-width="3" marker-end="url(#s31-ink)"/>
    <rect x="626" y="70" width="270" height="116" fill="#FFFFFF" stroke="#14171C" stroke-width="2.5"/>
    <text x="761" y="118" font-size="30" font-weight="700" text-anchor="middle">관찰된</text>
    <text x="761" y="158" font-size="30" font-weight="700" text-anchor="middle">상황별 특성</text>
    <text x="761" y="228" font-size="24" fill="#5E6570" text-anchor="middle">관찰과 가설을 구분</text>
    <polyline points="902,128 974,128" fill="none" stroke="#14171C" stroke-width="3" marker-end="url(#s31-ink)"/>
    <path d="M980 56 H1220 L1250 86 V200 H980 Z" fill="#E1E9F6" stroke="#2457A6" stroke-width="3.5"/><path d="M1220 56 V86 H1250" fill="none" stroke="#2457A6" stroke-width="3"/>
    <text x="1115" y="120" font-size="32" font-weight="800" text-anchor="middle" fill="#14171C">페르소나</text>
    <text x="1115" y="162" font-size="32" font-weight="800" text-anchor="middle" fill="#14171C">명세</text>
    <g font-size="30" font-weight="700" text-anchor="middle" dominant-baseline="central">
      <rect x="200" y="318" width="200" height="60" fill="#ECE9E1"/><text x="300" y="348">과업</text>
      <rect x="200" y="398" width="200" height="60" fill="#ECE9E1"/><text x="300" y="428">독자</text>
      <rect x="200" y="478" width="200" height="60" fill="#ECE9E1"/><text x="300" y="508">자리</text>
    </g>
    <g fill="none" stroke="#14171C" stroke-width="3">
      <polyline points="400,348 690,348 690,428"/>
      <polyline points="400,428 974,428" marker-end="url(#s31-ink)"/>
      <polyline points="400,508 690,508 690,428"/>
    </g>
    <polyline points="1115,206 1115,358" fill="none" stroke="#2457A6" stroke-width="4" marker-end="url(#s31-blue)"/>
    <rect x="980" y="364" width="270" height="128" fill="#2457A6"/>
    <text x="1115" y="414" font-size="30" font-weight="800" text-anchor="middle" fill="#FFFFFF">등록과 판단</text>
    <text x="1115" y="454" font-size="30" font-weight="800" text-anchor="middle" fill="#FFFFFF">기준 선택</text>
    <text x="1115" y="540" font-size="24" fill="#3A4049" text-anchor="middle">관련 맥락만 넣는다</text>
    <polyline points="1256,410 1300,410 1300,352 1330,352" fill="none" stroke="#14171C" stroke-width="3" marker-end="url(#s31-ink)"/>
    <polyline points="1256,446 1300,446 1300,500 1330,500" fill="none" stroke="#14171C" stroke-width="3" marker-end="url(#s31-ink)"/>
    <g>
      <rect x="1336" y="304" width="344" height="100" fill="#FFFFFF" stroke="#14171C" stroke-width="2.5"/>
      <text x="1356" y="344" font-size="28" font-weight="800">사내 보고 검수</text>
      <text x="1356" y="384" font-size="25" fill="#3A4049">원인과 조치 기한을 묻는다</text>
      <rect x="1336" y="452" width="344" height="100" fill="#FFFFFF" stroke="#14171C" stroke-width="2.5"/>
      <text x="1356" y="492" font-size="28" font-weight="800">외부 발언</text>
      <text x="1356" y="532" font-size="25" fill="#3A4049">같은 사실을 배경과 함께</text>
    </g>
    <polyline points="1508,298 1508,128 1262,128" fill="none" stroke="#B45309" stroke-width="3" stroke-dasharray="10 8" marker-end="url(#s31-amber)"/>
    <text x="1528" y="200" font-size="28" font-weight="800" fill="#B45309">사람의</text>
    <text x="1528" y="238" font-size="28" font-weight="800" fill="#B45309">피드백</text>
  </svg>
  <p class="abs foot ceo-foot">같은 사실(가상): 분기 일정 지연 두 건. 원자료와 인물 정보는 공개하지 않는다. 모델을 학습시키지 않으며, 단계들은 독립된 작업자가 아니다.</p>'''
    return dict(kind="case", case="CEO Agent", case_index=5, chapter=4, v10=[26], label="사례 5 CEO Agent",
                theme="t-paper", body=body, layout="case")


# ---------------------------------------------------------------- 32 chapter 5

def s32():
    theme, body = chapter(32, 5, ["끝났다는 말을", "어떻게 믿을까?"],
                          "흐름과 시작 장치, 주장과 확인을 나눈다. 일이 어디서 돌고 누가 개입하는지까지 적은 뒤, 다섯 사례를 한 틀로 되짚는다.",
                          24, [("워크플로우", "term"), ("자동화", "term"), ("완료 보고", "term"), ("검증", "term"),
                               ("로컬 실행", "term"), ("클라우드 실행", "term"), ("리모트 컨트롤", "term"), ("종합", "synth")])
    notes = '''<p>질문: 끝났다는 말을 어떻게 믿을까?</p>
<p>순서: 워크플로우(3분), 자동화(3분), 완료 보고(3분), 검증(3분), 로컬 실행(2분), 클라우드 실행(2분), 리모트 컨트롤(3분), 종합(4분). 전환 1분을 더해 약 24분이다.</p>
<p>왜 실행 위치가 이 장에 있나: "끝났다"는 말을 믿으려면 무엇이 어디서 돌았고 누가 개입했는지까지 적어야 한다. 로컬과 클라우드는 실행 위치, 리모트 컨트롤은 개입 방식이라는 다른 축이다.</p>'''
    return dict(kind="chapter", label="5장 끝났다는 말을 어떻게 믿을까?", theme=theme, body=body, notes=notes)


# ---------------------------------------------------------------- 33 workflow (S27): numbered steps, one human gate

def s33():
    s = Svg("s33", 120, 440, 1680, 460, "원문 보존, 수정과 확인, 사용자 최종 확정, 제작과 재열람 검증의 네 단계")
    steps = [(0, "원문 보존 v01", "v01, 정리 노트, 인덱스"), (420, "수정과 확인", "새 버전, 이전 본 보존")]
    for x, t, out in steps:
        s.text(x, 40, f"0{1 if x == 0 else 2}", size=64, weight=800, fill=BLUE)
        s.box(x, 100, 340, 130, t, size=32, weight=800)
        s.text(x, 270, "산출물", size=24, weight=800, fill=MUTED)
        s.text(x, 306, out, size=26, fill=INK2)
    s.text(840, 40, "03", size=64, weight=800, fill=AMBER)
    s.add('<polygon points="960,90 1090,165 960,240 830,165" fill="#FBECDB" stroke="#B45309" stroke-width="3.5"/>')
    s.lines(960, 165, ["사용자", "최종 확정"], size=28, weight=800, fill=AMBER, anchor="middle")
    s.text(990, 270, "사람이 결정", size=24, weight=800, fill=AMBER)
    s.text(990, 306, "확정 메시지", size=26, fill=INK2)
    s.text(1180, 40, "04", size=64, weight=800, fill=BLUE)
    s.box(1180, 100, 500, 130, ["삽화, 보존, 비공개 초안,", "재열람 검증"], size=30, weight=800, stroke=BLUE, sw=3.5)
    s.text(1180, 270, "산출물", size=24, weight=800, fill=MUTED)
    s.text(1180, 306, "초안과 재열람 기록", size=26, fill=INK2)
    s.arrow([(340, 165), (414, 165)])
    s.arrow([(760, 165), (824, 165)])
    s.arrow([(1090, 165), (1174, 165)], color="amber")
    s.arrow([(960, 240), (960, 380), (730, 380), (730, 236)], color="amber", dash="10 8")
    s.text(990, 380, "확정 전에는 다음 단계가 열리지 않는다", size=26, weight=800, fill=AMBER)
    s.text(1180, 420, "공개 발행은 이 흐름에 없다", size=26, fill=MUTED)
    theme, body = term_top(5, 19, "워크플로우",
                           "입력, 단계, 단계별 산출물, 다음 단계로 넘어가는 조건을 정해 둔 작업 흐름. 사람이 단계를 따라도 워크플로우다.",
                           "AI교양 원문을 받았다. 최종본은 아직 확정 전이다.", "삽화부터 만들어도 될까?",
                           s.render(), "자동화는 그중 일부를 조건이 맞으면 시작하는 장치다. 하네스는 이 단계를 돌리고 검증하는 틀이다.")
    return dict(kind="term", term="워크플로우", term_index=19, chapter=5, v10=[27], label="용어 19 워크플로우",
                theme=theme, body=body, layout="sequence")


# ---------------------------------------------------------------- 34 automation (S28): trigger, bundle, log

def s34():
    s = Svg("s34", 120, 440, 1680, 460, "사람의 확정 뒤 트리거가 작업 묶음을 시작하고 기록을 남긴다")
    s.box(0, 40, 300, 160, ["최종 확정", ("사람이 한다", {"size": 26, "weight": 400, "fill": INK2})], size=32,
          weight=800, fill="none", stroke=AMBER, dash="10 8", color=AMBER)
    s.text(0, 240, "자동화 바깥", size=24, weight=800, fill=AMBER)
    s.arrow([(300, 120), (364, 120)], color="amber")
    s.box(370, 40, 290, 160, ["트리거", ("확정 메시지 도착", {"size": 26, "weight": 400, "fill": WHITE})], size=32,
          weight=800, fill=BLUE, stroke=BLUE, color=WHITE)
    s.arrow([(660, 120), (734, 120)], color="blue")
    s.rect(740, 0, 560, 380, fill=WHITE, stroke=INK, sw=4)
    s.text(770, 38, "이어서 실행되는 작업", size=28, weight=800)
    for i, t in enumerate(["삽화 생성", "확정 문장과 이미지 보존", "비공개 초안 작성", "초안 재열람"]):
        y = 74 + i * 74
        s.rect(770, y, 500, 60, fill=PAPER2)
        s.text(796, y + 30, t, size=28, weight=700)
    s.arrow([(1300, 120), (1374, 120)])
    s.box(1380, 40, 300, 160, ["기록", ("실행 로그, 실패 기록", {"size": 26, "weight": 400, "fill": INK2})], size=32,
          weight=800)
    s.lines(1380, 280, ["성공 기록은 실행이", "끝났다는 뜻일 뿐이다"], size=26, weight=800, fill=AMBER, lh=1.4)
    s.check(740, 404, False, 40)
    s.text(796, 424, "공개 발행은 조건에 넣지 않는다", size=28, weight=700, fill=AMBER)
    theme, body = term_top(5, 20, "자동화",
                           "시간, 이벤트, 앞 단계 결과 같은 조건이 충족되면 사람이 다시 시작하지 않아도 정해진 작업을 실행하게 만든 장치.",
                           "최종 확정 메시지가 도착했다. 저장과 초안 작성을 이어 가고 싶다.", "확정 메시지 하나로 뒤의 제작 전체를 시작해도 될까?",
                           s.render(), "자동 기억은 저장과 불러오기의 문제, 자동화는 실행 시작의 문제다. 이 장면은 설명용이며 실행하지 않았다.")
    return dict(kind="term", term="자동화", term_index=20, chapter=5, v10=[28], label="용어 20 자동화",
                theme=theme, body=body, layout="sequence")


# ---------------------------------------------------------------- 35 completion report (S29): claim vs check

def s35():
    s = Svg("s35", 120, 440, 1680, 460, "완료 보고 카드의 주장과 대조 결과")
    s.rect(0, 0, 760, 360, fill=WHITE, stroke=INK, sw=2.5)
    s.rect(0, 0, 760, 72, fill=INK)
    s.text(30, 36, "완료 보고", size=30, weight=800, fill=WHITE)
    s.text(730, 36, "주장", size=26, weight=800, fill="#BFD3FF", anchor="end")
    for i, (k, v) in enumerate([("상태", "완료"), ("산출물", "report.md"), ("확인 항목", "건수 검증 완료"), ("미확인", "없음")]):
        y = 116 + i * 62
        s.text(30, y, k, size=26, weight=800, fill=MUTED)
        s.text(220, y, v, size=30, weight=700, mono=(k == "산출물"))
    s.rect(900, 0, 780, 360, fill=WHITE, stroke=BLUE, sw=3)
    s.rect(900, 0, 780, 72, fill=BLUE_SOFT)
    s.text(930, 36, "대조 결과", size=30, weight=800, fill=BLUE)
    s.text(1650, 36, "확인", size=26, weight=800, fill=BLUE, anchor="end")
    s.check(930, 104, True, 48)
    s.text(1000, 128, "파일 존재", size=30, weight=800)
    s.text(1650, 128, "예", size=30, weight=800, fill=BLUE, anchor="end")
    s.check(930, 194, False, 48)
    s.text(1000, 218, "건수 일치", size=30, weight=800)
    s.text(1650, 218, "아니오", size=30, weight=800, fill=AMBER, anchor="end")
    s.text(1000, 270, "보고서 42, 원본 행 40, 고유 티켓 38", size=26, fill=INK2)
    s.arrow([(764, 180), (894, 180)], color="blue")
    s.text(0, 420, "보고는 완료, 검증은 실패. 둘을 나란히 적는다.", size=34, weight=800, fill=AMBER)
    theme, body = term_top(5, 21, "완료 보고",
                           '작업자가 "끝났다"고 말한 기록. 무엇을 했고 무엇을 확인했다고 주장하는지 담지만, 그 자체가 검증 증거는 아니다.',
                           '작업자가 "검토 완료" 한 줄로 보고했다.', "그 한 줄이면 검토가 끝났다고 말할 수 있을까?",
                           s.render(), "실행 도구의 done은 실행이 끝났다는 증거일 수 있지만, 요구 조건을 만족한다는 증거는 아니다.")
    return dict(kind="term", term="완료 보고", term_index=21, chapter=5, v10=[29], label="용어 21 완료 보고",
                theme=theme, body=body, layout="compare")


# ---------------------------------------------------------------- 36 verification (S30): ledger of checks

def s36():
    s = Svg("s36", 120, 440, 1680, 460, "검증 항목, 확인 방법, 결과 기록")
    for x, t in ((0, "항목"), (460, "확인 방법"), (1180, "결과 기록")):
        s.text(x, 16, t, size=26, weight=800, fill=MUTED)
    s.line(0, 44, 1680, 44, color=INK, sw=3)
    rows = [("건수 일치", "결정적 확인", BLUE, ["원본 행 수와 고유 ticket_id 수를", "명령으로 세어 요약과 대조한다"],
             ["원본 40, 고유 38, 보고서 42", ("실패", {"fill": AMBER, "weight": 800})]),
            ("모호 행 목록", "결정적 확인", BLUE, ["빈 칸이나 형식이 다른 날짜가 있는", "행 번호를 뽑아 보고서와 대조한다"],
             ["빠진 행이 있으면 실패로 적는다"]),
            ("근거 인용", "사람의 확인", AMBER, ["주요 주장마다 행 식별자가", "인용됐는지 읽고 확인한다"],
             [("아직 확인 전", {"fill": MUTED})])]
    for i, (item, kind, col, how, res) in enumerate(rows):
        y = 56 + i * 124
        if i % 2 == 0:
            s.rect(0, y, 1680, 116, fill=PAPER2)
        s.text(24, y + 40, item, size=32, weight=800)
        s.text(24, y + 84, kind, size=24, weight=800, fill=col)
        s.lines(460, y + 58, how, size=28, lh=1.35)
        s.lines(1180, y + 58, res, size=28, weight=700, lh=1.35)
    s.text(0, 440, "기준은 작업 전에 정한다. 한 항목 통과가 전체 통과는 아니다.", size=30, weight=800, fill=BLUE)
    theme, body = term_top(5, 22, "검증",
                           "미리 정한 기준으로 산출물, 숫자, 인용, 파일 상태, 실행 결과를 작업자의 말과 독립된 방법으로 확인해 판단하는 과정.",
                           '주간 요약에 "이번 주 문의 42건"이라고 적혀 있다.', "누가 어떻게 확인할까? 한 번 보면 충분할까?",
                           s.render(), "같은 작업자가 다시 읽는 것은 약한 점검이다. 리뷰는 판단이고, 검증은 기준에 따른 확인이다.")
    return dict(kind="term", term="검증", term_index=22, chapter=5, v10=[30], label="용어 22 검증",
                theme=theme, body=body, layout="compare")


# ---------------------------------------------------------------- 37 local execution (S31): device boundary

def s37():
    s = Svg("s37", 120, 440, 1680, 460, "노트북 안에서 도는 도구와 파일, 기기 밖일 수 있는 모델 추론")
    s.rect(0, 0, 1040, 400, fill="none", stroke=INK, sw=4)
    s.add(f'<polygon points="-20,404 1060,404 1040,430 0,430" fill="{INK}"/>')
    s.text(30, 40, "내 노트북", size=30, weight=800)
    s.box(40, 120, 280, 200, ["메모 폴더", ("파일 여러 개", {"size": 26, "weight": 400, "fill": INK2})], size=30, weight=800)
    s.box(380, 120, 280, 200, ["파일 읽기 도구", ("여기서 실행된다", {"size": 26, "weight": 400, "fill": INK2})],
          size=30, weight=800, stroke=BLUE, sw=3.5)
    s.box(720, 120, 280, 200, ["작업 폴더", ("요약을 저장한다", {"size": 26, "weight": 400, "fill": INK2})], size=30,
          weight=800)
    s.arrow([(320, 220), (374, 220)])
    s.box(1260, 120, 420, 200, ["모델 추론 서비스", ("위치는 따로 확인", {"size": 26, "weight": 400, "fill": INK2})],
          size=30, weight=800, stroke=MUTED, dash="10 8")
    s.arrow([(660, 160), (690, 160), (690, 80), (1150, 80), (1150, 170), (1254, 170)], color="muted", dash="9 7")
    s.text(1120, 56, "요청", size=26, weight=800, fill=MUTED, anchor="end")
    s.arrow([(1260, 270), (1150, 270), (1150, 360), (860, 360), (860, 326)], color="muted", dash="9 7")
    s.text(1170, 384, "응답", size=26, weight=800, fill=MUTED)
    s.lines(1260, 400, ["로컬 실행이어도 인터넷과", "계정이 필요할 수 있다"], size=24, fill=MUTED, lh=1.35)
    theme, body = term_top(5, 23, "로컬 실행",
                           "도구와 프로세스가 사용자의 컴퓨터에서 돌고, 파일 접근과 명령이 그 기기 안에서 일어나는 방식. 모델 추론 위치와는 따로 말한다.",
                           "노트북의 메모 폴더를 AI 도구가 읽고 요약한다.", "요약 답변도 노트북에서 만들어질까?",
                           s.render(), '"로컬에서 돌렸다"가 모델도 기기 안에서 돌았다는 뜻은 아니다. 로컬이 곧 안전하다는 뜻도 아니다.')
    return dict(kind="term", term="로컬 실행", term_index=23, chapter=5, v10=[31], label="용어 23 로컬 실행",
                theme=theme, body=body, layout="boundary")


# ---------------------------------------------------------------- 38 cloud execution (S32): per-component ledger

def s38():
    s = Svg("s38", 120, 440, 1680, 460, "구성 요소마다 내 기기인지 외부 서버인지 따로 적은 목록")
    s.text(0, 20, "구성 요소", size=26, weight=800, fill=MUTED)
    s.text(860, 20, "내 기기", size=28, weight=800, anchor="middle")
    s.text(1380, 20, "외부 서버", size=28, weight=800, anchor="middle")
    s.line(0, 50, 1680, 50, color=INK, sw=3)
    rows = [("모델 추론", "초안 텍스트를 만든다", "server"), ("초안 파일 저장", "노트북에 쓴다", "device"),
            ("파일 도구", "읽고 쓰는 기능", "device"), ("메일 발송", "이 장면에서는 하지 않는다", "none")]
    for i, (t, d, where) in enumerate(rows):
        y = 64 + i * 84
        if i % 2 == 0:
            s.rect(0, y, 1680, 76, fill=PAPER2)
        s.text(24, y + 38, t, size=30, weight=800)
        s.text(300, y + 38, d, size=26, fill=INK2)
        if where == "device":
            s.box(740, y + 12, 240, 52, "여기", size=26, weight=800, fill=INK, stroke=INK, color=WHITE)
        elif where == "server":
            s.box(1260, y + 12, 240, 52, "여기", size=26, weight=800, fill=BLUE, stroke=BLUE, color=WHITE)
        else:
            s.box(740, y + 12, 760, 52, "실행하지 않음", size=26, weight=800, fill="none", stroke=AMBER, dash="9 7",
                  color=AMBER)
    s.text(0, 430, '"클라우드 작업"이라는 한 단어로는 어느 부분인지 알 수 없다.', size=32, weight=800, fill=BLUE)
    theme, body = term_top(5, 24, "클라우드 실행",
                           "도구, 워커, 모델 추론 중 일부나 전부가 사용자 기기가 아닌 외부 서버에서 도는 방식. 어느 구성 요소인지 함께 말해야 한다.",
                           "모델은 외부 서버에서 초안을 쓰고, 파일은 노트북에 저장한다.", '"클라우드 작업"이라고 한 단어로 불러도 될까?',
                           s.render(), "클라우드 실행과 리모트 컨트롤은 다른 축이다. 공유 범위는 제품 설정에 따르며 전역 공유를 가정하지 않는다.")
    return dict(kind="term", term="클라우드 실행", term_index=24, chapter=5, v10=[32], label="용어 24 클라우드 실행",
                theme=theme, body=body, layout="compare")


# ---------------------------------------------------------------- 39 remote control (S33): run here, watch there

def s39():
    s = Svg("s39", 120, 440, 1680, 460, "노트북에서 계속 도는 워커와, 같은 세션을 보고 멈추는 휴대폰 앱")
    s.rect(0, 0, 900, 380, fill="none", stroke=INK, sw=4)
    s.add(f'<polygon points="-20,384 920,384 900,410 0,410" fill="{INK}"/>')
    s.text(30, 40, "노트북: 실행 위치", size=30, weight=800)
    s.box(40, 100, 380, 220, ["워커", ("작업이 계속 돈다", {"size": 26, "weight": 400, "fill": WHITE})], size=40,
          weight=800, fill=BLUE, stroke=BLUE, color=WHITE, lh=1.5)
    s.box(480, 100, 380, 220, ["파일", ("여기에만 있다", {"size": 26, "weight": 400, "fill": INK2})], size=36, weight=800)
    s.rect(1320, 0, 360, 440, fill=WHITE, stroke=INK, sw=4)
    s.text(1500, 40, "휴대폰 앱", size=30, weight=800, anchor="middle")
    s.rect(1350, 76, 300, 200, fill=PAPER2)
    s.lines(1500, 176, ["같은 세션", "화면"], size=30, weight=700, anchor="middle")
    s.box(1390, 310, 220, 80, "중단", size=32, weight=800, fill=AMBER, stroke=AMBER, color=WHITE)
    s.arrow([(904, 150), (1314, 150)], color="blue", tail=True)
    s.text(1110, 122, "보기와 지시", size=28, weight=800, fill=BLUE, anchor="middle")
    s.arrow([(1384, 350), (950, 350), (950, 260), (906, 260)], color="amber")
    s.text(1170, 322, "중단 신호", size=28, weight=800, fill=AMBER, anchor="middle")
    s.text(0, 448, "앱은 두 번째 쓰기 주체가 아니다. 실행 위치는 그대로 노트북이다.", size=28, weight=800, fill=INK2)
    theme, body = term_top(5, 25, "리모트 컨트롤",
                           "실제 실행은 원래 환경에서 계속하고, 다른 화면이나 기기에서 그 세션을 보고 지시하거나 중단 신호를 보내는 개입 방식.",
                           "노트북에서 도는 작업을 휴대폰에서 보고 멈추고 싶다.", "멈춤을 누르면 작업 장소가 휴대폰으로 옮겨질까?",
                           s.render(), "실행 위치와 개입 방식은 다른 축이다. 한 경로로 연결됐다고 다른 경로의 앱 가시성이 보장되지는 않는다.")
    return dict(kind="term", term="리모트 컨트롤", term_index=25, chapter=5, v10=[33], label="용어 25 리모트 컨트롤",
                theme=theme, body=body, layout="boundary")


# ---------------------------------------------------------------- 40 synthesis (S34)

def s40():
    rows = [("AI교양", "흐름과 전환 조건, 사람의 확정 게이트", "재열람으로 검증"),
            ("OpenClaw", "실행 위치와 개입 방식", "워커와 원격 앱"),
            ("OMH", "제약에 맞춘 도구와 권한, 증거와 한계", "사내 모델 품질 미검증"),
            ("Grokbot", "책임과 실행 위치의 패턴", "사용자 설명, 첨부 미확인"),
            ("CEO Agent", "조사한 페르소나를 상황에 맞게 고르는 흐름", "단계는 독립 작업자가 아님")]
    lis = "".join(f'<li><span class="c">{e(a)}</span><span class="w">{e(b)}</span><span class="n">{e(c)}</span></li>'
                  for a, b, c in rows)
    chips = "".join(f"<span>{e(t)}</span>" for t in ["규칙", "컨텍스트", "도구와 실행 위치", "상태", "검증과 사람의 최종 책임"])
    body = "\n  ".join([
        p("kicker op-kicker", "종합"),
        p("op-title", "다섯 사례, 같은 요소, 다른 무게", "h2"),
        f'<div class="abs syn-chips">{chips}</div>',
        f'<ol class="abs syn-list">{lis}</ol>',
        p("foot", "측정된 성과 비교가 아니다. 설계와 기록 구조만 비교했다.",
          style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    return dict(kind="synthesis", label="종합: 다섯 사례", theme="t-paper", body=body, v10=[34], chapter=5, layout="synthesis")


# ---------------------------------------------------------------- 41 closing

def s41():
    body = '''<p class="abs close-kicker">마치며</p>
  <h2 class="abs close-thesis">AI에게 일을 맡길 때는<br>모델 바깥의 구조까지 설계한다</h2>
  <ol class="abs close-list">
    <li><span class="n">01</span><span class="s">모델은 요청하고, 실행은 런타임이 한다</span><span class="q">AI는 무엇을 하고 누가 실행할까?</span></li>
    <li><span class="n">02</span><span class="s">일하는 방법은 절차와 도구로 담는다</span><span class="q">일하는 방법을 어디에 담을까?</span></li>
    <li><span class="n">03</span><span class="s">이번 호출에 실제로 들어간 정보가 컨텍스트다</span><span class="q">AI는 무엇을 알고 있을까?</span></li>
    <li><span class="n">04</span><span class="s">세션은 작업 맥락이고, 워커는 실행 담당이다</span><span class="q">누가 이어서 일할까?</span></li>
    <li><span class="n">05</span><span class="s">완료 보고는 주장이고, 검증은 확인이다</span><span class="q">끝났다는 말을 어떻게 믿을까?</span></li>
  </ol>
  <p class="abs close-end">이어서 질문을 받겠습니다.</p>'''
    notes = '''<p>다섯 장의 질문을 한 문장씩으로 되짚는다. 각 문장은 해당 장의 핵심 구분이다.</p>
<ul>
<li>1장: 모델은 출력과 도구 호출 요청을 만들고, 실제 실행은 런타임이 한다.</li>
<li>2장: 절차는 스킬, 기능은 도구, 배포는 플러그인, 연결은 커넥터, 규약은 MCP로 나눠 담는다. 순서와 역할 배정은 오케스트레이션이다.</li>
<li>3장: 컨텍스트는 이번 호출에 실제로 들어간 정보 전체다. 지시와 요청, 읽힌 파일 내용, 도구 결과, 포함된 이전 대화가 모두 들어간다. 디스크에만 있는 파일은 들어가지 않는다.</li>
<li>4장: 세션은 작업 맥락을 묶는 단위이고, 워커는 실제로 일을 수행하는 주체다. 역할을 나누거나 서브에이전트를 써도 그것만으로 독립 검증이 되지는 않는다.</li>
<li>5장: 완료 보고는 주장이고, 검증은 미리 정한 기준으로 확인하는 일이다. 사람의 확정은 자동화 바깥에 둔다. 실행 위치와 개입 방식은 다른 축이다.</li>
</ul>
<p>주의: 구조를 설계하면 점검 가능성과 재현성이 높아질 수 있지만, 결과가 반드시 좋아진다고 말하지 않는다.</p>'''
    return dict(kind="closing", label="마치며", theme="t-night", body=body, notes=notes, layout="closing")


# ---------------------------------------------------------------- 42 Q&A (S35)

QA_INDEX = [
    ("1장", [("5", "모델"), ("6", "에이전트"), ("7", "런타임"), ("8", "하네스"), ("9", "OpenClaw")]),
    ("2장", [("11", "오케스트레이션"), ("12", "도구"), ("13", "스킬"), ("14", "OMH"), ("15", "플러그인"), ("16", "커넥터"),
             ("17", "MCP"), ("18", "Grokbot")]),
    ("3장", [("20", "프롬프트"), ("21", "컨텍스트"), ("22", "토큰"), ("23", "컨텍스트 창"), ("24", "메모리"), ("25", "AI교양")]),
    ("4장", [("28", "세션"), ("29", "워커"), ("30", "서브에이전트"), ("31", "CEO Agent")]),
    ("5장", [("33", "워크플로우"), ("34", "자동화"), ("35", "완료 보고"), ("36", "검증"), ("37", "로컬 실행"),
             ("38", "클라우드 실행"), ("39", "리모트 컨트롤")]),
]
CASES = {"OpenClaw", "OMH", "Grokbot", "AI교양", "CEO Agent"}


def s42():
    cols = []
    for i, (ch, items) in enumerate(QA_INDEX):
        lis = "".join(f'<li{" class=" + chr(34) + "case" + chr(34) if t in CASES else ""}><b>{n}</b>{e(t)}</li>'
                      for n, t in items)
        cols.append(f'<div class="abs qa-col" style="left:{120 + i * 344}px"><p class="qa-ch">{ch}</p><ul>{lis}</ul></div>')
    body = "\n  ".join([
        p("kicker op-kicker", "질의응답"),
        p("op-title", "질문을 받겠습니다", "h2"),
        p("qline", "질문이 없다면: 가장 헷갈렸던 용어 하나와 그 이유는?", style="left:120px;top:262px;width:1680px;margin:0"),
        *cols,
        p("foot", "숫자는 슬라이드 번호다. 사각형 표시는 사례다. 확인되지 않은 답은 확인이 필요하다고 답한다.",
          style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    return dict(kind="qa", label="질의응답", theme="t-paper", body=body, v10=[35], layout="qa")


SLIDES_B = [s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38, s39, s40, s41, s42]
