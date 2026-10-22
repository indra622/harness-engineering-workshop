"""v21: a quiet OKF knowledge-reuse update on physical page 15 only."""

from kit import p

COPY = "이후 OKF도 적용: 작업 지식을 정리해 다음 작업에서 재사용"
SPEC = "https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md"


def apply(slides):
    targets = [s for s in slides if s.get("orig") == "omh-evolution"]
    if len(targets) != 1:
        raise SystemExit("v21: expected one OMH evolution slide")
    slide = targets[0]
    slide["body"] += "\n  " + p(
        "foot okf-update", COPY,
        style="left:120px;top:946px;width:1560px;margin:0;",
    )
    slide["notes"] += (
        '<p><strong>이후의 작은 추가 (2026-10-22 작성자 진술):</strong> '
        'OMP로 옮겨 직접 덧붙일 부분을 줄인 뒤, OKF(Open Knowledge Format) 기반의 '
        '폴더형 지식 정리도 적용했습니다. 작업에서 확인한 지식을 노트로 정리하고 '
        '다음 작업에 필요한 내용을 찾아 재사용하려는 용도입니다. '
        '작성자는 동작한다고 보고했지만 이 발표 자료에서는 내부 구현이나 '
        '다음 세션의 검색 정확도, 성능 향상을 독립 검증하지 않았습니다. '
        'OKF 자체가 기억을 검색하거나 자동 갱신하는 실행기라는 뜻은 아니며, '
        'OMP 기본 기능 상자에도 포함시키지 않았습니다. '
        f'형식 출처: <a href="{SPEC}">OKF v0.2 명세 (고정 커밋 ad30107)</a>.</p>'
    )
    return slides
