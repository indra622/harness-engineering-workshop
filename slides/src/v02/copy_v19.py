"""v19: a quiet reflective epilogue after the Q&A. Everything else as in v18.

v18 removed the old closing (original 41). v19 appends a new closing page after
the Q&A, reusing original id 41 so no reference, term or case id is invented;
the original order becomes 1 to 40, 42, 41. The page has no diagram, list or
icon: a title and seven lines in three groups on the night theme, with the
approved wording kept as is. Its CSS is appended only from v19 so earlier exports
stay byte-identical.
"""

from kit import p

TITLE = "만들어 보고도, 남아 있는 질문"
GROUPS = [
    ["공부할수록, 오히려 확신이 줄었어요.", "에이전트가 더 똑똑해지면 해결될 일은 아닐까.", "우리가 더해야 할 구조는 어디까지일까."],
    ["누군가는 필요성을 느끼고,", "누군가는 저처럼 질문이 더 생겼을지도 모르겠어요."],
    ["그래도 직접 시도하고 알아간 시간은 남겠죠.", "오늘은 답 하나보다, 각자의 질문 하나가 남았으면 해요."],
]

V19_CSS = """
/* v19: reflective epilogue after the Q&A */
.ep-rule { left: 128px; top: 196px; width: 72px; height: 4px; background: var(--sky); }
.ep-title { left: 122px; top: 232px; margin: 0; font-size: 68px; font-weight: 800; line-height: 1.2; letter-spacing: -0.01em;
  color: var(--night-text); }
.ep-body { left: 128px; top: 440px; width: 1500px; margin: 0; }
.ep-body p { margin: 0 0 46px; font-size: 34px; line-height: 1.62; color: var(--night-muted); }
.ep-body p:last-child { margin-bottom: 0; color: var(--night-text); }
"""

NOTES = """<p><strong>이 화면의 자리:</strong> 질의응답 뒤에 두는 짧은 맺음말입니다. 앞에서 정리한 결론을 다시 요약하는 화면이 아니라, 발표를 준비하며 남은 생각을 솔직하게 나누는 자리입니다. 천천히 읽고 길게 덧붙이지 않습니다.</p>
<p><strong>작성자의 생각:</strong> 직접 만들어 보고 공부할수록 오히려 확신이 줄었습니다. 모델이 더 똑똑해지면 지금 우리가 더하는 구조 중 일부는 필요 없어질 수도 있고, 어디까지 구조를 더해야 하는지는 아직 잘 모르겠습니다. 고정된 절차와 다시 쓰는 도구는 반복되는 일에서 분명 쓸모가 있지만, 모든 일에 꼭 필요한 것은 아니라고 생각합니다.</p>
<p><strong>듣는 분들께:</strong> 오늘 이야기를 듣고 누군가는 이런 구조가 필요하다고 느끼고, 누군가는 저처럼 질문이 더 생겼을 수 있습니다. 둘 다 괜찮습니다. 꼭 무언가를 만들어 가지 않아도, 직접 시도해 보고 알아 간 경험과 각자의 질문이 남는다면 그것으로 충분하다고 생각합니다.</p>
<p><strong>말하지 않는 것:</strong> 더 똑똑한 모델이 모든 문제를 해결한다고 말하지 않습니다. 화면의 '에이전트가 더 똑똑해지면 해결될 일은 아닐까'는 답이 아니라 질문입니다. 앞의 사례들에 대해 새로 측정한 성과도 덧붙이지 않습니다.</p>"""


def closing():
    groups = "".join("<p>" + "<br>".join(lines) + "</p>" for lines in GROUPS)
    body = "\n  ".join([
        '<div class="abs ep-rule" aria-hidden="true"></div>',
        p("ep-title", TITLE, "h2"),
        f'<div class="abs ep-body">{groups}</div>',
    ])
    return dict(kind="closing", label="맺음말: 남아 있는 질문", theme="t-night", body=body, notes=NOTES,
                layout="closing", orig=41)


def append(slides):
    """The epilogue goes after the Q&A, as the last page."""
    if slides[-1]["kind"] != "qa" or any(s.get("orig") == 41 for s in slides):
        raise SystemExit("v19: expected the Q&A last and no original 41")
    return slides + [closing()]
