# 하네스 엔지니어링 워크샵

하네스 엔지니어링 워크숍의 용어 설명과 사례를 준비하는 작업 디렉토리다.

![하네스 엔지니어링 v04 표지](assets/workshop-v04-cover.png)

## 현재 기준

- 발표 자료는 v04다. 42장. [slides/index.html](slides/index.html)을 연다. v04는 v03의 구성과 도식을 그대로 두고, 강의 시간 배분을 화면과 발표자 노트와 목록 파일에서 모두 뺐으며, 화면 문구를 발표용 문장으로 다시 다듬었다. 쪽 번호와 2번 슬라이드의 작가 중심 순서(작가가 주제를 고르고 초고 v01을 직접 쓴 뒤 AI와 함께 다듬음)는 그대로다.
- [슬라이드별 내용 정의 v10](docs/plans/slide-content-plan-v10.md): 용어와 사례의 뜻, 장면, 사실 제약의 기준. 발표자 노트에 표시한 정정(2, 9, 23, 29, 30번)만 v10보다 우선한다. v04 노트의 v10 발췌는 강의 시간 표기만 뺀 편집본이며, 원문은 이 파일에 그대로 있다.
- [슬라이드 제작 브리프 v02](docs/production/slide-production-brief-v02.md): 다섯 장 구성, 42장 화면 지도, 배치 계열, v02 정정. 이 브리프의 시간 배분은 v02와 v03 기준의 기록이며 v04에는 적용하지 않는다.
- [DESIGN.md](DESIGN.md): v02 디자인 기준(표준 절 순서). v01 디자인은 [docs/design/DESIGN-v01.md](docs/design/DESIGN-v01.md)에 보존했다.
- 용어 25개를 각각 독립 슬라이드에서 설명하고, 사례 다섯 개(OpenClaw, OMH, Grokbot, AI교양, CEO Agent)를 관련 용어 바로 뒤에 둔다. CEO Agent는 한 장이다. 3장과 4장 사이에 쉬는 시간이 있고, 참가자 실습은 없다.

## 폴더

- `docs/plans/`: 슬라이드 내용 정의 v01부터 v10. 내용 기준은 v10이다.
- `docs/production/`: 슬라이드 제작 브리프 v01(이전 판)과 v02(현재).
- `docs/design/`: v01 디자인 사본과 v02 시안 단계의 제안.
- `docs/notes/`: 초기 강사용 워크샵 노트와 개정본.
- `slides/`: 발표 자료, PDF, 발표자 노트와 빌드 소스(`slides/src/`).
- `assets/`: 현재 발표 자료의 표지 미리보기와 시각자료.

## 발표 자료 v04 (현재)

HTML이 기준 산출물이다. 도식은 모두 편집 가능한 인라인 SVG와 실제 텍스트이며, 화면 전체를 이미지로 넣지 않았다. 네트워크 없이 열리고 외부 글꼴이나 CDN을 쓰지 않는다.

- [slides/index.html](slides/index.html): 현재 입구. 단일 파일이라 파일 하나만 보내도 열린다.
- [slides/harness-engineering-workshop-v04.html](slides/harness-engineering-workshop-v04.html): 기준 단일 파일 내보내기. `index.html`과 같은 내용이다.
- [slides/harness-engineering-workshop-v04.pdf](slides/harness-engineering-workshop-v04.pdf): 브라우저 인쇄로 만든 42쪽, 16:9 PDF. 쪽마다 번호가 찍힌다.
- [slides/speaker-notes-v04.md](slides/speaker-notes-v04.md): 발표자 노트 전문. 용어와 사례 슬라이드에는 v10 해당 블록의 편집 발췌(강의 시간 표기만 뺌)가 들어 있고, 정정이 필요한 곳은 정정이 발췌보다 먼저 나온다.
- [slides/harness-engineering-workshop-v04.manifest.json](slides/harness-engineering-workshop-v04.manifest.json): 화면 번호, 종류, 배치, 장, 용어, 사례, v10 출처 목록. 같은 정보가 각 슬라이드의 `data-` 속성에도 있다.
- [slides/v04-check-evidence.json](slides/v04-check-evidence.json): 최근 브라우저 검사 결과.

조작: 오른쪽, 아래, PageDown, 스페이스는 다음, 왼쪽, 위, PageUp은 이전, Home과 End는 처음과 끝, N은 발표자 노트, F는 전체 화면이다. `index.html#s31`이나 `#31`처럼 슬라이드 번호로 바로 연다. `?notes=1`을 붙이면 노트가 열린 채로 시작한다. 인쇄하면 슬라이드마다 한 쪽씩 나온다. 쪽 번호는 화면 오른쪽 아래에 "n / 42"로 보인다.

글꼴은 Nanum Gothic을 기본으로 쓰고, 없으면 Apple SD Gothic Neo, Malgun Gothic, Noto Sans KR 순으로 대체된다. 렌더와 검사는 Nanum Gothic으로 했다.

다시 만들기와 점검은 [slides/src/README.md](slides/src/README.md)에 있다.

## 이전 판 (보존)

- v03 발표 자료: [slides/harness-engineering-workshop-v03.html](slides/harness-engineering-workshop-v03.html), [slides/harness-engineering-workshop-v03.pdf](slides/harness-engineering-workshop-v03.pdf), [slides/speaker-notes-v03.md](slides/speaker-notes-v03.md), `slides/harness-engineering-workshop-v03.manifest.json`, `slides/v03-check-evidence.json`. 120분 일정 기준. 쪽 번호와 2번 슬라이드 정정을 처음 넣은 판이며, `--version v03`으로 다시 빌드하면 같은 바이트가 나온다.
- v02 발표 자료(120분 일정 기준): [slides/harness-engineering-workshop-v02.html](slides/harness-engineering-workshop-v02.html), [slides/harness-engineering-workshop-v02.pdf](slides/harness-engineering-workshop-v02.pdf), [slides/speaker-notes-v02.md](slides/speaker-notes-v02.md), `slides/harness-engineering-workshop-v02.manifest.json`, `slides/v02-check-evidence.json`. 내보낸 그대로 보존했고, `--version v02`로 다시 빌드하면 같은 바이트가 나온다.
- v01 발표 자료: [slides/harness-engineering-workshop-v01.html](slides/harness-engineering-workshop-v01.html)(단일 파일), [slides/harness-engineering-workshop-v01.pdf](slides/harness-engineering-workshop-v01.pdf)(35쪽), [slides/speaker-notes.md](slides/speaker-notes.md)(v01 노트). v01 입구 파일은 `slides/index-v01.html`로 옮겼고 `slides/assets/`의 CSS와 JS를 쓴다.
- v02 시안 여섯 장: `slides/previews/redesign-v02.html`, `.pdf`, `slides/previews/redesign-v02/`.
- `slides/previews/`의 PPTX 여섯 장은 더 이전 단계의 선택형 실험 결과이며 기준 산출물이 아니다.

## 작업 원칙

이 디렉토리를 이후 작업의 기준으로 사용한다. 개정은 새 버전 파일로 저장하고 이전 버전은 보존한다. 발표자료 주요 작성과 수정은 공식 Claude Remote Control 경로를 따른다. 기존 원격 세션의 작업 트리는 자동으로 이 경로로 옮겨진 것이 아니다. 후속 작성 전에 새 경로를 작업자에게 명시한다.

## 버전과 공개 범위

현재 발표 자료는 v04, 내용 정의는 v10이다. 과거 버전과 초기 노트는 개정 이력으로 보존하며 현재 진행안과 다를 수 있다.

공개본은 로컬 절대 경로를 논리 경로로 바꿨다. `ceo-agent/`와 `workspace/`로 적힌 근거 자료는 이 저장소에 포함되지 않은 로컬 참고 자료다. CEO Agent의 실제 페르소나, 회사 내부 자료, 보고서, 인증정보와 실행 로그는 포함하지 않는다. Grokbot 첨부 원자료도 포함하지 않는다. 로컬 원본과 복사 검증 파일은 별도로 보존한다.
