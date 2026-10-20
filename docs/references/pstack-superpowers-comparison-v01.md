# pstack과 Superpowers 비교 자료 v01

기준일: 2026-10-21. 발표 자료 v07의 참고 화면 두 장(15쪽 참고 A, 16쪽 참고 B)의 근거 문서다.

이 문서는 두 공개 스킬 묶음을 같은 기준일의 고정된 커밋으로 읽고 한국어로 요약한 것이다. 원문을 옮겨 싣지 않았고, 두 묶음을 실제로 실행하거나 성능을 잰 결과도 아니다. 어느 쪽이 낫다는 순위, 점수, 벤치마크, 모든 환경에서 똑같이 동작한다는 호환성 주장은 하지 않는다. 이 워크숍이 두 묶음을 설치하라고 안내하지도 않는다.

## 1. 비교 대상과 고정된 판

- **pstack**: Cursor의 공식 플러그인 저장소 `cursor/plugins` 안의 pstack.
  - 버전 0.15.29
  - 커밋 `111cf6a16b11cc822782c1585859af4a580a2490`
  - 같은 이름의 다른 저장소 사본이나 개인 설치본(예: 이전에 설치된 0.15.25)은 이 문서의 비교 대상이 아니다.
- **Superpowers**: `obra/superpowers`.
  - 버전 7.0.0
  - 커밋 `b739a8af570e10a95898f2bdf6cec97467fa6c12`

링크는 모두 위 커밋에 고정된 주소다.

- pstack
  - [README](https://github.com/cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490/pstack/README.md)
  - [plugin.json](https://github.com/cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490/pstack/plugin.json)
  - [기능(feature) 플레이북](https://github.com/cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490/pstack/skills/poteto-mode/playbooks/feature.md)
  - [Claude Code 어댑터](https://github.com/cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490/pstack/docs/harness/claude-code.md)
- Superpowers
  - [README](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/README.md)
  - [.claude-plugin/plugin.json](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/.claude-plugin/plugin.json)
  - [brainstorming](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/skills/brainstorming/SKILL.md)
  - [subagent-driven-development](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/skills/subagent-driven-development/SKILL.md)
  - [test-driven-development](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/skills/test-driven-development/SKILL.md)

## 2. 출처에서 확인한 사실

각 줄 끝의 링크가 근거다. 표현은 요약이며 원문 인용이 아니다.

### pstack

- poteto-mode가 요청을 보고 플레이북 하나를 고른 뒤, 그 단계를 할 일 목록으로 열고 필요한 다른 스킬을 부른다. README는 플레이북 23개를 소개한다(조사, 버그 수정, 기능, 리팩터링 등). [README, usage](https://github.com/cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490/pstack/README.md#usage)
- 기능 플레이북은 다음 순서로 진행한다.
  - 영향 범위를 파악하고 설계를 탐색한다.
  - 먼저 끝내야 할 단계, 서로 독립인 작업, 공유 상태, 가장 작은 안전한 분할을 할 일로 적어 점검한다.
  - 파일 범위, 데이터 구조, 성공 기준을 정해 코드 작성을 하위 에이전트에 맡긴다.
  - 맞는 대상에서 검증하고, 작은 단위로 커밋한다.
  - 한 기능처럼 코드가 엮인 일은 한 담당자에게 두고, 상위에서 여럿에 나누는 것은 서로 독립인 결과물에 쓴다.
  - [feature 플레이북](https://github.com/cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490/pstack/skills/poteto-mode/playbooks/feature.md)
- 스킬은 Cursor 이름으로 쓰여 있고, Claude Code에서는 어댑터 문서가 도구, 하위 에이전트 설정, 모델, 경로 이름을 바꿔 대응한다. Cursor 전용 기능이 필요한 단계는 한 줄로 알리고 건너뛴다. [Claude Code 어댑터](https://github.com/cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490/pstack/docs/harness/claude-code.md)
- 계획 전용 스킬은 기본으로 두지 않으며, 필요하면 poteto-mode가 계획을 다룬다고 README가 밝힌다. [README, why are there no planning skills?](https://github.com/cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490/pstack/README.md#why-are-there-no-planning-skills)

### Superpowers

- 기본 흐름(README)은 다음 순서다.
  - brainstorming으로 의도를 끌어내 합의한다.
  - 작업 공간을 분리한다.
  - writing-plans로 작은 작업 단위의 계획을 쓴다.
  - subagent-driven-development 또는 executing-plans로 실행한다. 실행 중에는 test-driven-development를 따르고, 작업 사이에 검토한다.
  - 브랜치를 마무리한다.
  - [README, The Basic Workflow](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/README.md#the-basic-workflow)
- brainstorming은 먼저 요청에서 무엇이 불분명한지 확인한다. 명확하고 단순한 변경은 바로 처리할 수 있고, 사용자가 질문을 건너뛰고 시작하라고 할 수도 있다. 설계가 필요한 작업은 이해를 맞추고, 프로젝트 규모에 따라 문서로 정리해 합의한다. [brainstorming](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/skills/brainstorming/SKILL.md)
- subagent-driven-development는 작업마다 새 구현 담당 하위 에이전트를 두고, 작업이 끝날 때마다 검토 한 번이 명세 충족과 코드 품질을 함께 보며, 마지막에 브랜치 전체를 검토한다. 하위 에이전트 없이 한 세션에서 실행하고 마지막에 한 번 검토하는 executing-plans도 고를 수 있다. [subagent-driven-development](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/skills/subagent-driven-development/SKILL.md)
- test-driven-development는 실패하는 테스트를 먼저 쓰고(RED), 통과할 만큼만 구현하고(GREEN), 정리하는(REFACTOR) 순환을 따른다. [test-driven-development](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/skills/test-driven-development/SKILL.md)
- README는 Claude Code 외에도 여러 코딩 에이전트의 설치 경로를 안내한다. [README, Installation](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/README.md#installation)

### 표기 차이 하나

- Superpowers README의 스킬 목록은 subagent-driven-development를 '두 단계 검토(명세, 그다음 품질)'로 소개한다.
- 같은 커밋의 스킬 본문은 작업별 검토 한 번이 명세와 품질을 함께 본다고 설명한다.
- 발표 자료는 스킬 본문을 따랐다.

## 3. 편집 요약 (발표 자료의 해석)

아래는 위 사실을 교육용으로 정리한 해석이다. 출처가 직접 이렇게 말한다는 뜻은 아니다.

- 같은 기능 추가 요청을 두고, pstack은 작업에 맞는 플레이북, 범위와 성공 기준을 정한 위임, 실제 동작으로 하는 검증을 앞에 둔다. Superpowers는 작업 크기에 맞춘 설계 합의, 작은 단위 계획, 테스트 먼저, 단계마다 검토를 앞에 둔다.
- 둘 다 다시 쓰는 스킬 묶음이고, 둘 다 하위 에이전트에 맡기고 검토할 수 있다. 차이는 무엇을 먼저 챙기는지에 있고, 할 수 있는 일의 유무나 성능 차이가 아니다.
- '한쪽은 빠르고 한쪽은 꼼꼼하다', '병렬 대 직렬' 같은 이분법으로 정리하지 않는다. 에이전트 수도 고정돼 있지 않다.
- 참고 A의 pstack 줄에서 1단계(플레이북 고르기) 다음 단계들은 기능 플레이북을 고른 경우의 예다. 다른 플레이북은 단계가 다르다.
- '실제 동작으로 검증'은 코드, 테스트, 실행 결과처럼 실제로 쓰이는 대상에서 근거와 대조한다는 뜻으로 쓴 표현이다. 화면 캡처만 보는 것이 아니다.

## 4. OMH와의 관계

- 이 저장소의 내용 기획 v10(S11)은 OMH의 선택형 엄격 절차(omh-rigorous)가 pstack에서 버그 수정, 기능 구현, 근거 기반 조사 절차를 골라 적응시킨 것이라고 기록한다.
- 어느 pstack 버전에서 가져왔는지는 기록이 없다. 그래서 위 0.15.29와 같다고 말하지 않는다.
- Superpowers는 이 자료에서 비교용 참고이며, OMH 구현의 근거로 제시하지 않는다.
- 참고 B에서 가운데 상자(내 환경에서 쓸 절차와 도구 선택)가 'OMH'로 이어지는 선은 설계 선택을 OMH에 적용한 예다. OMH가 실제로 어디서 무엇을 가져왔는지 보여 주는 계보가 아니다.
- OMH는 설정된 모델 하나와 OpenCode, OMO의 기존 역할을 그대로 두고, 업무 도구(data_inspect, data_compare)와 필요할 때 골라 쓰는 omh-rigorous를 더했다(14쪽).

## 5. 다시 볼 때

- 두 묶음은 자주 바뀐다. 다시 볼 때는 새 커밋과 버전을 고정하고, 이 문서를 v02로 새로 만든다. v01은 남겨 둔다.
- 특히 다음 세 가지가 바뀌면 참고 화면을 다시 확인한다.
  - pstack 기능 플레이북의 단계와 위임 방식
  - Superpowers의 검토 구조와 실행 방식 선택지
  - 두 묶음의 호스트 지원 범위
