---
version: alpha
name: Harness Workshop Editorial
description: 하네스 엔지니어링 120분 워크숍 발표 자료 v02의 디자인 시스템. 1920 x 1080 캔버스, 편집 디자인 위계, 두 강조색.
colors:
  primary: "#14171C"
  on-primary: "#FFFFFF"
  secondary: "#3A4049"
  muted: "#5E6570"
  rule: "#CFCBC2"
  neutral: "#F5F3EE"
  neutral-2: "#ECE9E1"
  tertiary: "#2457A6"
  tertiary-soft: "#E1E9F6"
  caution: "#B45309"
  caution-soft: "#FBECDB"
  night: "#11151B"
  night-2: "#1B2129"
  night-line: "#3B4552"
  on-night: "#ECEEF1"
  on-night-muted: "#A2AAB5"
  sky: "#8DB4FF"
  chapter: "#1D4486"
  on-chapter-muted: "#BFD3FF"
typography:
  display-cover:
    fontFamily: Nanum Gothic
    fontSize: 176px
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: -0.02em
  display-chapter:
    fontFamily: Nanum Gothic
    fontSize: 112px
    fontWeight: 800
    lineHeight: 1.16
  term-split:
    fontFamily: Nanum Gothic
    fontSize: 140px
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: -0.02em
  term-top:
    fontFamily: Nanum Gothic
    fontSize: 112px
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: -0.02em
  headline-case:
    fontFamily: Nanum Gothic
    fontSize: 68px
    fontWeight: 800
    lineHeight: 1.2
  headline-closing:
    fontFamily: Nanum Gothic
    fontSize: 80px
    fontWeight: 800
    lineHeight: 1.2
  body-definition:
    fontFamily: Nanum Gothic
    fontSize: 34px
    fontWeight: 700
    lineHeight: 1.45
  body-scene:
    fontFamily: Nanum Gothic
    fontSize: 30px
    fontWeight: 400
    lineHeight: 1.45
  label-diagram:
    fontFamily: Nanum Gothic
    fontSize: 30px
    fontWeight: 800
    lineHeight: 1.32
  label-sm:
    fontFamily: Nanum Gothic
    fontSize: 24px
    fontWeight: 400
    lineHeight: 1.4
  label-kicker:
    fontFamily: Nanum Gothic
    fontSize: 26px
    fontWeight: 700
    letterSpacing: 0.04em
  code:
    fontFamily: SF Mono
    fontSize: 26px
    fontWeight: 400
rounded:
  none: 0px
spacing:
  canvas-width: 1920px
  canvas-height: 1080px
  safe: 40px
  margin: 120px
  gutter: 28px
  diagram-gap: 60px
  min-text: 24px
components:
  slide-cover:
    backgroundColor: "{colors.night}"
    textColor: "{colors.on-night}"
    typography: "{typography.display-cover}"
  slide-chapter:
    backgroundColor: "{colors.chapter}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-chapter}"
  slide-content:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
  case-tag:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-kicker}"
    padding: 6px
  diagram-box:
    backgroundColor: "#FFFFFF"
    textColor: "{colors.primary}"
    typography: "{typography.label-diagram}"
    rounded: "{rounded.none}"
  diagram-box-key:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.none}"
  human-gate:
    backgroundColor: "{colors.caution-soft}"
    textColor: "{colors.caution}"
  distinction-line:
    textColor: "{colors.secondary}"
    typography: "{typography.body-scene}"
---

# 하네스 엔지니어링 워크숍 디자인 v02

v02 발표 자료(`slides/harness-engineering-workshop-v02.html`)의 기준이다. v01 디자인 문서는 `docs/design/DESIGN-v01.md`에 원문 그대로 보존했다. 토큰의 실제 값은 `slides/src/v02/v02.css`의 `:root`에 있다.

## Overview

v01은 "도식이 붙은 강의 노트"였다. 서른다섯 장이 같은 질문 띠, 같은 정의 띠, 같은 둥근 상자로 채워져 어느 화면도 앞으로 나오지 않았다. v02는 편집 디자인처럼 화면마다 주인공 하나를 크게 둔다. 표지는 제목, 장 전환은 장의 질문, 용어는 단어와 그 개념이 움직이는 그림, 사례는 한 줄 결론, 마무리는 명제가 주인공이다.

청중은 AI 도구를 업무에 쓰려는 비개발 직군을 포함한 사내 참가자다. 화면은 차분하고 단단해야 하고, 개념의 경계가 또렷해야 한다. 장식 그래픽, 스톡 일러스트, 그라디언트, 그림자는 쓰지 않는다.

리듬은 배경 세 가지로 만든다. 표지, 휴식, 마무리는 밤, 다섯 장 전환은 파랑, 본문은 종이다. 42장 안에서 밤 3장, 파랑 5장, 종이 34장이 번갈아 나온다.

## Colors

강조색은 둘뿐이다. 나머지는 잉크와 종이의 단계다.

- **Primary, 잉크 (#14171C):** 제목, 본문, 상자 테두리, 사례 꼬리표.
- **Secondary (#3A4049), Muted (#5E6570):** 보조 문장, 각주, 열 제목.
- **Neutral, 종이 (#F5F3EE)와 Neutral-2 (#ECE9E1):** 본문 배경과 레인, 보조 면.
- **Tertiary, 구조의 파랑 (#2457A6)과 옅은 파랑 (#E1E9F6):** 흐름, 실행 계층, 핵심 상자, 확인된 것.
- **Caution, 호박색 (#B45309)과 옅은 호박색 (#FBECDB):** 사람의 확인과 결정, 한계, 미검증, 지시와 실제 권한의 차이, 헷갈리기 쉬운 점.
- **Night (#11151B), Chapter (#1D4486):** 표지와 마무리, 장 전환 배경.

파랑은 "구조와 확인", 호박색은 "사람과 한계"라는 뜻으로만 쓴다. 같은 화면에서 두 색이 다른 뜻으로 쓰이지 않게 한다.

## Typography

기본 글꼴은 Nanum Gothic (Regular, Bold, ExtraBold)이다. 대체 순서는 Apple SD Gothic Neo, Malgun Gothic, Noto Sans KR, sans-serif다. 렌더와 검사는 Nanum Gothic으로 했고, 다른 글꼴로 바뀌면 줄바꿈이 달라질 수 있다. 코드 이름(`read_file`, `tickets.csv` 등)만 고정폭 글꼴을 쓴다.

- **표시용:** 표지 176px, 장 질문 112px, 용어 단어 140px(나란히 배치)와 112px(위쪽 배치). 단어가 길면 줄인다(5자 120px, 6자 100px, 7자 88px).
- **제목:** 사례 결론 60~68px, 마무리 명제 80px, 여는 화면 제목 76px.
- **본문:** 정의 34px Bold, 장면 30px, 도식 라벨 26~32px.
- **최소 크기:** 캔버스 기준 24px. 넘치면 글자를 줄이지 않고 문장이나 배치를 고친다.

## Layout

모든 화면은 1920 x 1080 고정 캔버스이며 화면 폭에 맞춰 비율 그대로 축소한다. 안전 여백 40px, 본문 왼쪽 정렬선 120px.

용어 화면은 개념에 맞춘 세 계열로 나눈다. 같은 틀을 25번 반복하지 않는다.

- **나란히 배치 (split, split-mirror):** 설명 열과 레인, 루프, 경계 그림. 에이전트, 런타임, 워커는 설명이 왼쪽, 스킬과 서브에이전트는 설명이 오른쪽이다.
- **위쪽 머리말과 전폭 비교 (compare, lane):** 모델, 도구, 프롬프트, 완료 보고, 검증, 클라우드 실행은 A와 B 또는 주장과 확인을 나란히 놓는다. 오케스트레이션은 전폭 레인이다.
- **위쪽 머리말과 전폭 시각 (boundary, sequence, typographic):** 하네스, 컨텍스트, 플러그인, 세션, 로컬 실행, 리모트 컨트롤은 경계, 커넥터, MCP, 메모리, 워크플로우, 자동화는 순서, 토큰과 컨텍스트 창은 글자와 막대 자체가 그림이다.

용어 화면에는 정의, 장면과 질문, 개념 그림, 헷갈리기 쉬운 점이 반드시 있다. 사례 화면은 꼬리표, 질문 줄, 한 줄 결론, 사례 고유 도식, 출처와 한계 각주를 갖는다.

## Elevation & Depth

평면 디자인이다. 그림자와 입체 효과는 쓰지 않는다. 위계는 크기, 굵기, 배경 면(종이와 옅은 면), 테두리 두께(일반 2.5px, 핵심 3.5~4px)로 만든다. 확인되지 않은 것, 설명상의 것, 지시상의 범위는 점선으로 그린다.

## Shapes

모든 상자는 각지다(모서리 0px). 원은 장 경로의 용어 정거장과 단계 번호에만, 마름모는 사람이 정하는 전환 조건에만 쓴다. 사각형 정거장은 사례와 종합이다. 접힌 모서리 문서 모양은 자료와 명세에만 쓴다.

## Components

- **장 전환:** 큰 장 번호(반투명), 장 질문, 장 목표 한 문장, 이번 장의 경로(용어는 원, 사례는 사각형), "약 N분" 표시 하나.
- **용어 머리말:** 장과 용어 번호 표식, 용어 단어, 정의, 장면 상자(왼쪽 파란 선, "장면" 라벨, 대사, 질문).
- **헷갈리기 쉬운 점:** 화면 맨 아래 가는 선 위 한 줄. 호박색 라벨.
- **도식 상자:** 흰 바탕과 잉크 테두리. 핵심은 파랑 채움 또는 굵은 파랑 테두리. 화살표는 끝에 삼각형 머리, 사람의 되돌림은 호박색 점선.
- **상태 표시:** 파란 체크(확인됨), 호박색 X(실패, 금지), 호박색 물음표(따로 확인할 단계).
- **사례 꼬리표:** 잉크 바탕 흰 글자 "사례 N / 5".
- **발표자 노트:** N 키로 여는 오른쪽 패널. v02 정정은 호박색 띠로 v10 원문보다 먼저 보인다.

## Do's and Don'ts

- Do 화면마다 주인공 하나를 정하고 나머지는 물러나게 한다.
- Do 그림이 그 개념의 동작을 보여 주게 한다. 개념에 맞지 않는 범용 그림을 재사용하지 않는다.
- Do 지시상 범위와 실제로 강제되는 권한을 구분해 적는다. 지시만으로 권한이 사라진다고 그리지 않는다.
- Do 확인되지 않은 내용은 점선과 "미확인" 표시로 구분한다.
- Don't 둥근 상자, 그림자, 그라디언트, 스톡 일러스트, 화면 전체 이미지를 쓰지 않는다.
- Don't 모든 화면에 같은 질문 띠와 정의 띠를 반복하지 않는다.
- Don't 24px보다 작은 글자를 쓰거나, 넘친 글자를 줄여서 맞추지 않는다.
- Don't 공개 화면에 가운뎃점(U+00B7), 호스트 절대 경로, 세션 링크, 개인 자료를 넣지 않는다.
