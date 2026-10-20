"""Write the v06 wording audit: every slide, with before and after for each change and the reason.

Usage (from the project root):
    python3 slides/src/v02/audit_v06.py [OUT.md]

Reads the applied edits from copy_v06.py, so the log always matches the build.
Default output: docs/production/wording-audit-v06.md
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

import copy_v06  # noqa: E402

# slides reviewed with no change, and why the wording stays
UNCHANGED = {
    1: "표지. 행위자나 내부 용어 없음",
    2: "작가 중심 순서(v03, v04) 그대로. '확정 뒤 정해진 절차'는 누가 무엇을 하는지 분명함",
    3: "로드맵(v05). 장 질문과 용어 목록뿐",
    4: "장 전환. 역할 표현 없음",
    5: "모델 정의와 도구 호출 요청 구분 유지",
    6: "에이전트 루프. 행위자 명확",
    7: "런타임: 요청은 모델, 권한 확인과 실행은 런타임. 정확함",
    8: "하네스 다섯 칸. 파일 이름은 예시",
    10: "장 전환",
    12: "도구 카드와 절차 메모 비교. 행위자 명확",
    20: "프롬프트 비교",
    21: "컨텍스트 경계. '저장된 파일과 지금 읽은 파일은 별개' 유지",
    22: "토큰 가상 분할",
    23: "압축과 창 크기 구분(v02 정정) 유지",
    24: "메모리 저장과 읽기",
    26: "쉬는 시간 화면",
    32: "장 전환",
    35: "완료 보고와 대조 결과. '대조'는 화면에서 하는 일 그대로",
    37: "로컬 실행. 도구 위치와 추론 위치 구분 유지",
    41: "마무리 다섯 줄. 화면 문구 변경 없음 (노트의 '주체'만 '작업자'로)",
    42: "질의응답 색인",
}

SLIDE9_DIAGRAM = [
    ("가지 '직접 도구 / 조회, 단순 편집'", "가지 '직접 처리 / 코디네이터가 스스로'",
     "원격 워커에 맡기지 않고 코디네이터가 직접 하는 경로라는 뜻. 도구의 종류가 아니다 (사용자 정정). "
     "그 아래 '런타임이 도구 실행' 표시는 유지: 코디네이터는 도구를 고르고 런타임이 실행한다"),
    ("가지 '원격 워커 / Codex 또는 Claude'", "가지 '워커에게 위임 / Codex 또는 Claude Code'", "다른 경로를 행위로 표현"),
    ("코디네이터 상자 '직접 할까, 맡길까'", "그대로 '직접 할까, 맡길까'", "두 가지와 같은 말로 묻는다"),
    ("'프로젝트 / 파일과 테스트'", "'작업 결과 / 파일과 테스트 출력'", "두 가지가 모두 여기로 모인다"),
    ("'부모의 / 독립 검증' (흰 상자)", "'결과 검증 / 코디네이터가 확인' (코디네이터와 같은 파란 상자)",
     "별도의 부모 에이전트는 없다. 같은 코디네이터가 돌아온 결과를 확인한다. 두 상자를 점선과 '같은 코디네이터' 표시로 잇고, "
     "결과가 돌아오는 화살표에 '결과를 돌려받음'을 붙였다"),
    ("'원격 앱 / 같은 워커를 보고 개입' (점선, 워커로 가는 선)", "'작업 확인 화면 / 진행 확인, 추가 지시' (점선으로 워커 바로 아래에 붙임)",
     "'원격'이 클라우드 추론처럼 읽히지 않게. 워커의 같은 작업을 보는 화면으로만 그리고, 게이트웨이와 연결된 것처럼 그리지 않는다"),
    ("태그 '세션은 4장', '워커는 4장'", "삭제 (게이트웨이 상자에 '채널과 세션' 유지)", "9번의 핵심인 경로와 확인 주체에 집중"),
    ("aria: '…직접 도구 또는 원격 워커, 파일과 테스트, 부모 검증, 답장'",
     "aria: '…코디네이터가 직접 처리하거나 워커에게 위임, 작업 결과, 같은 코디네이터의 결과 검증, 답장. 작업 확인 화면은 워커가 하는 같은 작업을 본다'",
     "화면과 같은 행위자"),
]


SLIDE14_DIAGRAM = [
    ("세 칸 기능 목록 (현장 제약 / 추가한 도구와 절차 칩 / 확인 가능한 증거) + 아래 가상 흐름 한 줄",
     "같은 일('CSV 빈 값 처리 후, 무엇이 바뀌었는지 확인')을 두 줄로 비교: 추가 전(OpenCode + OMO, 기존 도구와 역할) / 추가 후(업무 도구와 절차를 더함). 단계는 구조 파악, 수정, 변경 확인 셋",
     "사용자 요청: 없을 때와 있을 때 무엇이 달라지는지. 기능 목록이 아니라 같은 일의 차이를 보인다"),
    ("(없음)", "추가 전: 파일을 열어 보거나 점검 스크립트를 작성 / 고른 빈 값 규칙 적용 / 비교 기준 키를 정하고 비교 코드를 준비",
     "기존 구성도 이 일을 할 수 있다는 점을 그대로 보인다. 측정한 실패 사례가 아닌 설명용 흐름 (각주에 명시)"),
    ("칩 'data_inspect 구조 점검', 'data_compare 키 기준 비교'",
     "추가 후: data_inspect (열, 타입, 빈 값 수, 점검 범위, 행 값은 빼고 요약) / 같은 수정 단계('수정 단계는 같음') / data_compare (id 기준, 추가, 삭제, 변경 행 요약, 자동 병합 없음)",
     "도구가 실제로 내놓는 근거를 구체적으로. 수치는 지어내지 않음. 수정 단계는 두 줄이 같다고 표시"),
    ("칩 'omh-rigorous 골라 쓰는 절차', 유지 칸 두 개",
     "'달라진 것' 띠: 그때그때 준비하던 점검과 비교를, 만들어 둔 도구로. 결과는 같은 형식으로 / omh-rigorous: 필요할 때 골라 쓰는 계획, 실행, 근거 확인 절차 (모델 성능 향상과는 별개)",
     "핵심 차이를 한 줄로. 모델, 기존 역할, 오프라인 조건이 그대로라는 점은 맨 위 '같은 일' 띠에"),
    ("증거 칸 '사내 모델 품질은 미검증'과 설명 문단", "각주(호박색): 추가 전 흐름은 설명용 예시. 모의, 오프라인 기능 점검만 했고 실제 사내 모델의 품질 비교는 하지 않음",
     "근거의 한계는 화면에 남기고, 자세한 설명은 노트로"),
    ("노트: v10 발췌만", "노트: 달라진 것, 달라지지 않은 것, 사람과 모델이 여전히 정하는 것(의미 있는 키, 빈 값 규칙, 결과 수용), 근거의 한계를 먼저 설명한 뒤 v10 발췌",
     "화면을 가볍게 두고 세부는 노트로"),
]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "production" / "wording-audit-v06.md"
    lines = ["# v06 문구와 역할 점검 기록", "",
             "대상: `slides/harness-engineering-workshop-v06.html` (42장). 기준은 v05 화면과 노트. "
             "변경 내용은 `slides/src/v02/copy_v06.py`에서 그대로 읽어 만든다.", "",
             "원칙: 가르치는 용어(모델, 런타임, 컨텍스트, 하네스, 워커, 서브에이전트, MCP 등)의 이름과 정의는 그대로 둔다. "
             "구현 내부 용어, 번역 투 명사 묶음, 행위자가 흐린 표현만 누가 무엇을 하는지 드러나게 고친다. "
             "사용자의 지시가 앞선 제안보다 우선한다(9번 '직접 처리').", ""]
    for n in range(1, 43):
        edits = copy_v06.EDITS.get(n, [])
        if n == 9:
            lines.append(f"## {n}번: 도식 다시 그림, 문구 수정")
            lines.append("")
            for before, after, why in SLIDE9_DIAGRAM:
                lines += [f"- 전: {before}", f"  후: {after}", f"  이유: {why}"]
        elif n == 14:
            lines.append(f"## {n}번: 추가 전과 추가 후 비교로 다시 그림, 문구 수정")
            lines.append("")
            for before, after, why in SLIDE14_DIAGRAM:
                lines += [f"- 전: {before}", f"  후: {after}", f"  이유: {why}"]
        elif edits:
            lines.append(f"## {n}번: 수정")
            lines.append("")
        else:
            lines.append(f"## {n}번: 변경 없음")
            lines.append("")
            lines.append(f"- 점검: {UNCHANGED.get(n, '점검함')}")
        for old, new, why in edits:
            strip = lambda s: re.sub(r"<[^>]+>", "", s).strip("<> ")  # noqa: E731
            lines += [f"- 전: {strip(old)}", f"  후: {strip(new)}", f"  이유: {why}"]
        if n in copy_v06.CORRECTIONS:
            lines.append(f"- 노트 정정(v10 발췌 앞): {copy_v06.CORRECTIONS[n]}")
        for old, new in copy_v06.NOTE_EDITS.get(n, []):
            lines += [f"- 노트 전: {old}", f"  노트 후: {new}"]
        lines.append("")
    lines += ["## 노트의 v10 발췌 (모든 용어와 사례 슬라이드)", "",
              "v10 원문(`docs/plans/slide-content-plan-v10.md`)은 그대로 두고, v06 노트의 발췌에서만 아래 표현을 순서대로 바꿨다. "
              "같은 목록이 `harness-engineering-workshop-v06.manifest.json`의 `excerpt_edits`에 있어 검사에서도 그대로 따라간다. "
              "'등록된 도구'(등록된 도구 목록이라는 뜻)는 정확하므로 바꾸지 않았다.", ""]
    for old, new in copy_v06.EXCERPT_EDITS:
        lines += [f"- 전: {old}", f"  후: {new}"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")


if __name__ == "__main__":
    main()
