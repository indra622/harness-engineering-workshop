"""v16: the Grokbot case (original 18) redrawn with the author-confirmed bots, and a third reference slide.

- Original 18 (physical 20): four bots the author confirmed on 2026-10-21
  (록식이, 에식이, 소식이, 최저가봇) share one cloud environment with connected
  apps and routines. No duties are drawn for the bots; the names are the
  author's configuration, not product names. The message is that a harness can
  run as a cloud service without always-on hardware of one's own, next to the
  self-run 클식이. The stale "unverified attachment" captions are gone from the
  screen, the aria label and the current notes; the v10 excerpt keeps its
  teaching lines and drops only the two stale lines about the attachment.
- 참고 C (physical 21, new): three cloud personal agents, dots (OpenAI),
  Grok Bot (xAI) and Muse (Meta), adapted from one slide of the AILC Lv3 course
  (chapter 2, '직접 써 보기: 누구나 쓰는 개인 에이전트 셋'). Dates, pricing,
  regions and app counts are left out. Claims follow the official pages checked
  on 2026-10-21; see docs/references/cloud-personal-agents-v01.md.
- Physical pointers move: originals 19 to 42 become physical 22 to 45. The Q&A
  index, the slide 2 note pointers and the slide 28 correction follow.
"""

import re

from kit import AMBER, BLUE, BLUE_SOFT, INK, INK2, MUTED, PAPER2, WHITE, Svg, case_head, e, p

import copy_v07

INSERT_AFTER = 18  # original slide number of the Grokbot case
SKIP_TO = 22  # physical number of the first main slide after 참고 C
NAMES = ["록식이", "에식이", "소식이", "최저가봇"]

SOURCES = [
    ("OpenAI, Getting started with your dot", "https://help.openai.com/en/articles/20001530-getting-started-with-your-dot"),
    ("xAI, Introducing Grok Bot", "https://x.ai/news/introducing-grok-bot"),
    ("Meta, Introducing Muse, a personal AI agent",
     "https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/"),
]


def physical(orig):
    """Physical slide number in v16 for an original (v06) slide number."""
    return orig if orig <= copy_v07.INSERT_AFTER else orig + 2 if orig <= INSERT_AFTER else orig + 3


def _sources_html(items):
    li = "".join(f'<li><a href="{u}">{e(t)}</a><br><span class="src">{e(u)}</span></li>' for t, u in items)
    return f"<h3>출처 (2026-10-21 확인)</h3><ul>{li}</ul>"


# ---------------------------------------------------------------- physical 20: four bots in one cloud


def grok_left():
    s = Svg("s18", 120, 380, 960, 570, "작성자가 확인한 구성: 록식이, 에식이, 소식이, 최저가봇 네 봇이 Grok Bot 서비스의 클라우드 "
            "컴퓨터 하나를 함께 쓰고, 연결한 앱과 루틴을 공유한다. 사람은 일을 맡기고, 필요할 때 승인한다")
    s.rect(0, 0, 960, 470, fill=BLUE_SOFT, stroke=BLUE, sw=3, extra=' data-box="cloud"')
    s.text(28, 36, "클라우드", size=28, weight=800, fill=BLUE)
    s.text(932, 36, "Grok Bot 서비스가 제공하는 컴퓨터", size=24, weight=800, fill=BLUE, anchor="end")
    for k, name in enumerate(NAMES):
        x, y = 40 + (k % 2) * 450, 70 + (k // 2) * 124
        s.rect(x, y, 430, 104, fill=WHITE, stroke=INK, sw=2.5, extra=f' data-bot="{name}"')
        s.text(x + 215, y + 52, name, size=34, weight=800, anchor="middle")
    s.text(40, 352, "네 봇이 함께 쓰는 것", size=24, weight=800, fill=INK2)
    for k, chip in enumerate(["공유 컴퓨터", "연결한 앱", "루틴"]):
        x = 40 + k * 300
        s.rect(x, 378, 280, 64, fill=WHITE, stroke=BLUE, sw=2, extra=' data-box="shared"')
        s.text(x + 140, 410, chip, size=28, weight=800, fill=BLUE, anchor="middle")
    s.rect(240, 506, 480, 60, fill=PAPER2, extra=' data-box="person"')
    s.text(480, 536, "사람: 일을 맡기고, 필요하면 승인", size=26, weight=800, anchor="middle")
    s.arrow([(480, 504), (480, 476)], color="blue")
    return s.render()


def grok_right():
    s = Svg("s18b", 1120, 380, 680, 570, "어디서 돌아가나. 직접 운영하는 클식이는 장비와 실행 환경을 우리가 관리한다. Grok Bot은 "
            "서비스가 늘 켜진 컴퓨터를 클라우드에 제공한다. 늘 켜 둔 내 장비 없이도 하네스를 쓸 수 있고, 서비스마다 권한과 이용 조건은 다르다")
    s.text(0, 14, "어디서 돌아가나", size=26, weight=800, fill=MUTED)
    s.rect(0, 44, 680, 150, fill=WHITE, stroke=MUTED, sw=2.5, dash="9 7", extra=' data-box="self"')
    s.text(28, 80, "직접 운영", size=24, weight=800, fill=MUTED)
    s.text(28, 120, "클식이", size=32, weight=800)
    s.text(28, 162, "장비와 실행 환경을 우리가 관리", size=26, fill=INK2)
    s.rect(0, 214, 680, 150, fill=BLUE, stroke=BLUE, sw=3, extra=' data-box="service"')
    s.text(28, 250, "클라우드 서비스", size=24, weight=800, fill=WHITE)
    s.text(28, 290, "Grok Bot", size=32, weight=800, fill=WHITE)
    s.text(28, 332, "서비스가 늘 켜진 컴퓨터를 제공", size=26, fill=WHITE)
    s.text(0, 418, "늘 켜 둔 내 장비 없이도", size=36, weight=800)
    s.text(0, 466, "하네스를 쓸 수 있음", size=36, weight=800, fill=BLUE)
    s.text(0, 520, "서비스마다 권한과 이용 조건은 다름", size=24, fill=INK2)
    s.text(0, 554, "다른 서비스는 다음 쪽, 참고 C", size=24, weight=800, fill=BLUE)
    return s.render()


def grok_body():
    return "\n  ".join([
        case_head(3, "Grokbot"),
        p("qline case-q", "<b>질문</b>하네스를 쓰려면 늘 켜 둔 내 컴퓨터가 꼭 있어야 할까?"),
        p("case-title", "내 맥미니 없이도, 클라우드에서 도는 봇 넷", "h2"),
        grok_left(), grok_right(),
    ])


GROK_NOTES = f"""<p><strong>화면 읽기:</strong> 왼쪽은 작성자가 2026-10-21에 확인한 Grok Bot 구성입니다. 록식이, 에식이, 소식이, 최저가봇 네 봇이 서비스가 제공하는 클라우드 컴퓨터 하나를 함께 쓰고, 연결한 앱과 루틴을 공유합니다. 네 이름은 작성자가 붙인 구성이며 공식 제품 이름이 아닙니다. 이름만으로 각 봇의 일을 짐작해 그리지 않았고, 어느 봇이 다른 봇을 지휘한다거나 특별한 전달 경로가 있다고 말하지 않습니다.</p>
<p><strong>이 사례를 보는 이유:</strong> 클식이는 우리가 장비와 실행 환경을 직접 운영하는 하네스입니다. Grok Bot 같은 클라우드 서비스는 늘 켜 둔 컴퓨터를 서비스가 제공하므로, 맥미니처럼 직접 관리하는 상시 장비가 없어도 비슷한 하네스를 쓸 수 있습니다. 하네스를 두는 곳이 우리 손으로 운영하는 장비에만 있지 않다는 것이 이 화면의 메시지입니다. 이런 서비스는 여럿이고 Grok Bot은 그중 하나입니다. 다음 쪽(참고 C)에서 다른 예를 봅니다.</p>
<p><strong>공식 제품 설명 (xAI, 2026-10-21 확인):</strong> Grok Bot은 클라우드에 자기 컴퓨터와 도구, 앱을 두고 계속 일하며, 여러 봇이 그 컴퓨터를 함께 씁니다. 봇마다 따로 부를 수 있고, 대화 맥락과 그룹 대화, 봇 사이 넘김이 있습니다. 선호와 루틴을 기억하고, 필요할 때 사람에게 승인을 구합니다. 출처: <a href="{SOURCES[1][1]}">{e(SOURCES[1][0])}</a></p>
<p><strong>말하지 않는 것:</strong> 모든 클라우드 서비스가 같은 권한, 가격, 제공 범위를 갖는다고 말하지 않습니다. 성능이나 생산성 수치, 추가 모델 학습도 주장하지 않습니다.</p>"""

CORRECTIONS = {
    18: ("v16부터 이 화면은 작성자가 2026-10-21에 확인한 구성(록식이, 에식이, 소식이, 최저가봇 네 봇과 공유 클라우드 컴퓨터, "
         "연결한 앱, 루틴)을 그린다. 아래 v10 발췌의 '사용자가 설명한 패턴'은 이 확인으로 대신하고, 네 비교 축 목록은 "
         "'늘 켜 둔 내 장비 없이도 클라우드에서 하네스를 쓸 수 있다'는 메시지로 바꿨다. 발췌에서 자료 상태에 관한 옛 메모 두 줄은 뺐다. "
         "발췌의 '클라우드가 항상 동작한다고 말하지 않는다'는 이전 화면의 패턴 설명에 대한 주의였고, v16 화면의 '늘 켜진 컴퓨터'는 "
         "xAI 공식 설명을 따른다. 위의 OpenClaw 줄 정정은 발췌의 구체 예시에만 해당한다."),
    40: ("v16부터 Grokbot 줄은 작성자가 확인한 구성(네 봇과 공유 클라우드 컴퓨터)을 따른다. 화면의 Grokbot 줄을 "
         "'클라우드 서비스에서 도는 봇 넷, 작성자가 확인한 구성'으로 바꿨고, 아래 발췌의 자료 상태에 관한 옛 문구는 뺐다."),
}

# the two stale lines about the attachment, dropped from the S15 excerpt in v16; teaching lines stay
EXCERPT_CUTS = {
    15: ["- 이번 수정에서도 첨부 자료를 열 수 없었다. 이 슬라이드는 이전에 받은 설명 요약만 쓰고, 그 요약도 독립 검증하지 않았다.\n"],
}
EXCERPT_SWAPS = {
    15: [("맨 아래에 \"사용자 설명, 첨부 미확인, 패턴 비교만\"이라고 적는다.", "")],
    34: [("Grokbot 설명: 책임과 실행 위치의 패턴. 첨부 미확인, 독립 검증 없음.", "Grokbot 설명: 책임과 실행 위치의 패턴.")],
}
SYNTH_EDITS = [
    ('<span class="w">책임과 실행 위치의 패턴</span><span class="n">사용자 설명, 첨부 미확인</span>',
     '<span class="w">클라우드 서비스에서 도는 봇 넷</span><span class="n">작성자가 확인한 구성</span>'),
]


def excerpt(sid, body):
    for old in EXCERPT_CUTS.get(sid, []):
        if body.count(old) != 1:
            raise SystemExit(f"v16 excerpt S{sid}: line not found: {old[:50]}")
        body = body.replace(old, "")
    for old, new in EXCERPT_SWAPS.get(sid, []):
        if body.count(old) != 1:
            raise SystemExit(f"v16 excerpt S{sid}: text not found: {old[:50]}")
        body = body.replace(old, new)
    return re.sub(r" +\n", "\n", body)


# corrections from earlier layers that name a physical page
FIX_PAGES = [("v12부터 27쪽 가운데 흐름은", "v12부터 이 화면(v16부터 28쪽) 가운데 흐름은")]


def fix_text(text):
    for old, new in FIX_PAGES:
        text = text.replace(old, new)
    return text


# ---------------------------------------------------------------- 참고 C: three cloud personal agents

AGENTS = [
    ("dots", "OpenAI", ["ChatGPT에서 시작", "연결한 앱으로 이어서 일하기", "결과 검토와 판단"]),
    ("Grok Bot", "xAI", ["봇별 대화, 그룹 대화", "늘 켜진 컴퓨터로 앱 작업", "필요할 때 승인 요청"]),
    ("Muse", "Meta", ["앱이나 WhatsApp", "메일, 여행, 양식 처리", "메일 발송, 구매 전 확인"]),
]
ROWS = ["들어가는 곳", "맡기는 일", "사람이 보는 곳"]
SHARED = ["클라우드의 자기 컴퓨터", "연결한 앱", "이어지는 기억", "사람의 확인"]


def ref_c():
    s = Svg("s21", 120, 340, 1680, 600, "클라우드에서 쓰는 개인 에이전트 셋. dots(OpenAI): ChatGPT에서 시작해 연결한 앱으로 이어서 "
            "일하고, 결과 검토와 판단은 사람. Grok Bot(xAI): 봇별 대화와 그룹 대화, 늘 켜진 컴퓨터로 앱 작업, 필요할 때 승인 요청. "
            "Muse(Meta): 앱이나 WhatsApp에서 메일, 여행, 양식 처리, 메일 발송과 구매 전 확인. 공통으로 클라우드의 자기 컴퓨터, "
            "연결한 앱, 이어지는 기억, 사람의 확인을 갖는다")
    w, gap = 540, 30
    for k, (name, maker, vals) in enumerate(AGENTS):
        x = k * (w + gap)
        s.rect(x, 0, w, 370, fill=WHITE, stroke=INK, sw=2.5, extra=f' data-agent="{name}"')
        s.text(x + 28, 44, name, size=36, weight=800)
        s.text(x + w - 28, 44, maker, size=26, weight=800, fill=MUTED, anchor="end")
        s.line(x + 28, 82, x + w - 28, 82, color=PAPER2, sw=2)
        for r, (lab, val) in enumerate(zip(ROWS, vals)):
            y = 118 + r * 86
            s.text(x + 28, y, lab, size=24, weight=800, fill=AMBER if r == 2 else BLUE)
            s.text(x + 28, y + 36, val, size=28, weight=700)
    s.rect(0, 400, 1680, 150, fill=BLUE_SOFT, stroke=BLUE, sw=3, extra=' data-box="shared"')
    s.text(28, 440, "셋의 공통점", size=26, weight=800, fill=BLUE)
    cw = 380
    for k, chip in enumerate(SHARED):
        x = 28 + k * (cw + 24)
        s.rect(x, 466, cw, 62, fill=WHITE, stroke=BLUE, sw=2)
        s.text(x + cw / 2, 497, chip, size=28, weight=800, anchor="middle")
    body = "\n  ".join([
        p("kicker case-head", f'<span class="tag-case">참고 C</span>{e("클라우드 개인 에이전트")}'),
        f'<a class="abs ref-skip" href="#s{SKIP_TO}">본문으로, {SKIP_TO}쪽</a>',
        p("qline case-q", "<b>질문</b>직접 만든 봇이 없어도, 비슷한 걸 써 볼 수 있을까?"),
        p("case-title", "맥미니 없이도, 클라우드에서 쓰는 개인 에이전트", "h2"),
        s.render(),
        p("foot", "출처: 각 회사 공식 발표와 도움말 (2026-10-21 확인). 이용 조건과 제공 지역은 서비스마다 다름",
          style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    notes = f"""<p><strong>이 화면의 위치:</strong> 본문(25개 용어와 다섯 사례)에 들지 않는 참고 화면입니다. 필요하면 오른쪽 위 '본문으로'를 눌러 {SKIP_TO}쪽으로 건너뜁니다.</p>
<p><strong>읽는 법:</strong> 앞 쪽의 Grok Bot처럼, 클라우드에 자기 컴퓨터를 두고 일하는 개인 에이전트 서비스는 여럿입니다. 셋은 들어가는 곳과 주로 맡기는 일이 다르지만, 클라우드의 자기 컴퓨터, 연결한 앱, 이어지는 기억, 사람이 확인하는 자리를 함께 갖습니다. 오늘 본 도구, 메모리, 검증과 사람의 개입이 서비스 안에 들어간 모습입니다. 순위나 성능 비교가 아닙니다.</p>
<p><strong>dots (OpenAI):</strong> ChatGPT에서 설정해 시작합니다. 자기 클라우드 컴퓨터에서 연결한 앱으로 일하고, 맥락을 이어 가며 대화와 대화 사이에도 계속 일합니다. 사용자가 목표와 맡길 범위를 정하고 결과를 검토하며, 판단은 사람에게 남깁니다. 내 컴퓨터와의 연결은 선택 사항이며 기본으로 꺼져 있어, 클라우드에서 쓰는 데 필요하지 않습니다. 화면의 'dots'는 원래 강의의 표기이고, 도움말에서는 한 개를 'dot'이라고 부릅니다.</p>
<p><strong>Grok Bot (xAI):</strong> 자기 컴퓨터와 도구, 앱을 클라우드에 두고 계속 일하며, 여러 봇이 그 컴퓨터를 함께 씁니다. 봇마다 따로 부를 수 있고, 그룹 대화와 봇 사이 넘김이 있습니다. 선호와 루틴을 기억하고, 필요할 때 승인을 구합니다. 앞 쪽의 네 봇 이름은 작성자의 구성이지 공식 이름이 아닙니다.</p>
<p><strong>Muse (Meta):</strong> 클라우드의 전용 보안 가상 컴퓨터와 브라우저로 메일, 여행, 양식, 목표 관리 같은 일을 합니다. 앱이나 WhatsApp에서 부르고, 앱을 닫아도 일을 이어 가며, 배우고 기억합니다. 메일을 보내거나 구매하기 전에 확인을 받고, 권한과 앱 연결은 사용자가 정합니다.</p>
<p><strong>출처와 뺀 것:</strong> AILC Lv3 강의 2장의 '직접 써 보기: 누구나 쓰는 개인 에이전트 셋' 한 장을 이 발표에 맞게 고쳐 실었습니다. 출시일, 가격, 제공 지역, 연결 앱 수는 금방 바뀌고 이 발표의 메시지에 필요하지 않아 뺐습니다. 모든 서비스를 어디서나 쓸 수 있다거나 권한과 가격이 같다고 말하지 않습니다. 정리 문서는 docs/references/cloud-personal-agents-v01.md입니다.</p>
{_sources_html(SOURCES)}"""
    return dict(kind="reference", reference="C", label="참고 C: 맥미니 없이도, 클라우드에서 쓰는 개인 에이전트",
                theme="t-paper", body=body, notes=notes, chapter=2, layout="reference")


# ---------------------------------------------------------------- per-slide changes and insertion


def apply(orig, sl):
    if orig == 2:
        for a, b in ((f"AI교양 사례({copy_v07.physical(25)}번)", f"AI교양 사례({physical(25)}번)"),
                     (f"워크플로우({copy_v07.physical(33)}번)", f"워크플로우({physical(33)}번)")):
            if sl["notes"].count(a) != 1:
                raise SystemExit(f"v16: slide 2 note pointer not found: {a}")
            sl["notes"] = sl["notes"].replace(a, b)
    elif orig == 18:
        sl["body"] = grok_body()
        sl["notes"] = GROK_NOTES
    elif orig == 40:
        for old, new in SYNTH_EDITS:
            if sl["body"].count(old) != 1:
                raise SystemExit("v16: synthesis Grokbot row not found")
            sl["body"] = sl["body"].replace(old, new)
    elif orig == 42:
        body, k = re.subn(r"<b>(\d+)</b>",
                          lambda m: f"<b>{int(m.group(1)) + 1 if int(m.group(1)) > 20 else m.group(1)}</b>", sl["body"])
        if k != 30:
            raise SystemExit(f"v16: Q&A index expected 30 numbers, found {k}")
        sl["body"] = body


def insert(slides):
    """참고 C goes right after the Grokbot case."""
    k = next(i for i, sl in enumerate(slides) if sl.get("orig") == INSERT_AFTER)
    return slides[:k + 1] + [ref_c()] + slides[k + 1:]
