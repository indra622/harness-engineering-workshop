# OMH v12 예시: 행 수는 그대로, 빠진 ID까지 찾아내기

발표 자료 v12 14쪽의 개수를 만든 합성 예시다. 실제 사용자나 회사 데이터는 없다.

## 요청과 파일

요청: CSV의 빈 `amount`만 0으로 바꾸고, 행은 더하지도 지우지도 말 것.

- `data/before.csv`: 원본, ID 0, 1, 2, 빈 `amount` 1개
- `data/after-first.csv`: 첫 결과. 행 3개, 빈 값 0개라 겉보기엔 맞지만, ID 0이 빠지고 없던 ID 3이 생김 (장면을 위해 손으로 만든 데이터)
- `data/after-fixed.csv`: 수정 결과. ID 0, 1, 2 그대로, ID 1의 `amount`만 0

## 다시 돌리기

```sh
python3 examples/omh-v12/run_example.py --engine "/path/to/omh/core/engine.py"
```

경로는 바꿔 넣을 예시다. 엔진은 OMH 통합 v04 묶음의 `components/omh/core` 아래 표준 라이브러리 단일 파일이다. 이 저장소에 들어 있지 않다. 로컬 명령으로 읽기만 하며, 설치, 네트워크, 모델 호출은 없다.

## 결과 (evidence/)

- `tool-results.json`: data_inspect 3회, data_compare 2회의 출력 그대로. `include_values`는 false라 행 값과 ID 값은 없고 개수와 순번만 있다.
- `summary.json`: 화면에 쓴 개수. csv 모듈로 따로 센 값과 같을 때만 기록한다.

| | 행 수 | 빈 amount | left_only | right_only | value_changed | 기준 충족 |
|---|---|---|---|---|---|---|
| 첫 결과 | 3 → 3 | 1 → 0 | 1 | 1 | 1 (amount) | 아니오 |
| 수정 결과 | 3 → 3 | 1 → 0 | 0 | 0 | 1 (amount) | 예 |

- `left_only`: 원본에만 있는 키, `right_only`: 결과에만 있는 키.
- 도구 결과의 `ok`는 호출 성공이라는 뜻이지 업무 기준 통과가 아니다. 기준(추가, 삭제 0건, amount만 변경, 빈 값 0, 전체 범위) 판단은 `run_example.py`가 따로 한다.
- 슬라이드의 역할 분담과 검토, 되돌림 흐름은 설명용이다. 에이전트 실행 기록이 아니다.
