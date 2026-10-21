"""v08: automatic difficulty judgment and the audience-facing case name 클식이."""


def apply(original, slide):
    slide["body"] = slide["body"].replace("OpenClaw", "클식이")
    slide["label"] = slide["label"].replace("OpenClaw", "클식이")
    if slide.get("case") == "OpenClaw":
        slide["case"] = "클식이"
    if original != 9:
        return
    old = "직접 할까, 맡길까"
    assert slide["body"].count(old) == 1
    slide["body"] = slide["body"].replace(old, "업무 난이도 자동 판단")
    slide["notes"] = slide.get("notes", "") + (
        "<p>클식이는 이 사례의 OpenClaw 기반 개인 에이전트를 부르는 이름입니다.</p>"
        "<p><strong>업무 난이도 자동 판단:</strong> 코디네이터가 요청의 복잡성과 작업 범위, "
        "필요한 도구를 보고 직접 처리할지 워커에게 위임할지 판단합니다. "
        "사용자의 명시적인 지시와 작업별 위임 기준을 우선합니다.</p>"
    )
