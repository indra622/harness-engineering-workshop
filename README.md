# 하네스 엔지니어링 워크샵

120분 교육의 용어 설명과 하네스 사례를 준비하는 작업 디렉토리다.

## 현재 기준

- [슬라이드별 내용 정의 v10](docs/plans/slide-content-plan-v10.md)
- 35장, 120분. 용어 25개를 각각 독립 슬라이드에서 설명하고, 사례 다섯 개를 관련 용어 사이에 끼워 넣었다. 용어 슬라이드는 각 3분이며 장면과 질문으로 시작한다. 장면 예시는 가상 초안이다.
- 도입 5분, 용어 75분, 휴식 10분, 사례 25분(OpenClaw 5, OMH 5, Grokbot 3, AI교양 5, CEO Agent 3, 종합 4), 질문 5분.
- 참가자 실습은 0분이다. OpenClaw, OMH, AI교양 제작 흐름, CEO Agent 한 장, 그록봇을 사례로 다룬다. CEO Agent 장은 조사한 페르소나를 상황에 맞게 적용하는 흐름을 다룬다.
- [슬라이드 제작 브리프 v01](docs/production/slide-production-brief-v01.md): 35장 제작 맵, 자산 목록, 넘김 기준.
- 발표 자료는 HTML이 기준이다. 아래 "발표 자료" 절을 본다. 시연 녹화 자료는 아직 만들지 않았다.

## 폴더

- `docs/plans/`: 슬라이드 내용 정의 v01부터 v10. 현재 기준은 v10이다.
- `docs/production/`: 슬라이드 제작 기획서와 시각자료 준비 계획.
- `docs/notes/`: 초기 강사용 워크샵 노트와 개정본.
- `slides/`: HTML 발표 자료, 단일 파일 내보내기, 인쇄용 PDF, 발표자 노트와 빌드 소스(`slides/src/`).
- `assets/`: 앞으로 사용할 그림과 도식. 현재 비어 있다.

## 발표 자료

HTML이 기준 산출물이다. 35장, 120분이며 도식은 모두 편집 가능한 네이티브 SVG다. 네트워크 없이 열리고 외부 글꼴이나 CDN을 쓰지 않는다.

- [slides/index.html](slides/index.html): 기준 발표 화면. `slides/assets/`의 CSS와 JS를 함께 쓴다. 폴더째로 연다.
- [slides/harness-engineering-workshop-v01.html](slides/harness-engineering-workshop-v01.html): 같은 내용의 단일 파일 내보내기. CSS와 JS가 안에 들어 있어 파일 하나만 보내도 열린다.
- [slides/harness-engineering-workshop-v01.pdf](slides/harness-engineering-workshop-v01.pdf): 브라우저 인쇄로 만든 35쪽, 16:9 PDF. 참고용이다.
- [slides/speaker-notes.md](slides/speaker-notes.md): 발표자 노트 전문. 화면에서는 N 키로 같은 노트를 연다.

조작: 오른쪽, 아래, PageDown, 스페이스는 다음, 왼쪽, 위, PageUp은 이전, Home과 End는 처음과 끝, N은 발표자 노트, F는 전체 화면이다. `index.html#s7`처럼 슬라이드 번호로 바로 연다. `?notes=1`을 붙이면 노트가 열린 채로 시작한다. 인쇄하면 슬라이드마다 한 쪽씩 나온다.

화면 글꼴은 시스템에 설치된 Nanum Gothic을 쓴다. 없으면 Apple SD Gothic Neo, Malgun Gothic, Noto Sans KR 순으로 대체된다.

다시 만들기와 점검은 [slides/src/README.md](slides/src/README.md)에 있다. `slides/previews/`의 PPTX 여섯 장은 이전 단계의 선택형 실험 결과이며 기준 산출물이 아니다.

## 작업 원칙

이 디렉토리를 이후 작업의 기준으로 사용한다. 개정은 새 버전 파일로 저장하고 이전 버전은 보존한다. 발표자료 주요 작성과 수정은 공식 Claude Remote Control 경로를 따른다. 기존 원격 세션의 작업 트리는 자동으로 이 경로로 옮겨진 것이 아니다. 후속 작성 전에 새 경로를 작업자에게 명시한다.

## 버전과 공개 범위

현재 교육안은 v10이다. 과거 버전과 초기 노트는 개정 이력으로 보존하며 현재 진행안과 다를 수 있다.

공개본은 로컬 절대 경로를 논리 경로로 바꿨다. `ceo-agent/`와 `workspace/`로 적힌 근거 자료는 이 저장소에 포함되지 않은 로컬 참고 자료다. CEO Agent의 실제 페르소나, 회사 내부 자료, 보고서, 인증정보와 실행 로그는 포함하지 않는다. 로컬 원본과 복사 검증 파일은 별도로 보존한다.
