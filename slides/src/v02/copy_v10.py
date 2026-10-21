"""v10: new comparison axes on slides 14 and 15, with slide 16 kept in step. Everything else as in v09.

- Slide 14 (OMH): the comparison is now bare OpenCode against the OMH integrated
  package, which bundles OMO's role collaboration and workflow together with
  OMH's own data tools and optional procedure. OMO is drawn inside the OMH
  boundary. This supersedes the v06 to v09 comparison (OpenCode + OMO on both
  sides, only the OMH additions differing). Evidence for the package
  relationship: the OMH integrated v04 reference (configuration and
  conditions, roles, tools), a local archive that is not part of this repository.
- Slide 15 (참고 A): a directional view chosen for this presentation, AS-IS
  Superpowers to TO-BE pstack. It is not a ranking, a maturity ladder or a record
  of a finished migration. Source facts stay those of the pinned commits in
  docs/references/pstack-superpowers-comparison-v01.md.
- Slide 16 (참고 B): labels and notes follow the two changes above.
"""

from kit import BLUE, BLUE_SOFT, INK, INK2, MUTED, PAPER2, WHITE, Svg, case_head, e, p

import copy_v07

# ---------------------------------------------------------------- slide 14: OpenCode 순정 vs OMH 통합 구성


def omh_svg():
    s = Svg("s14", 120, 340, 1680, 600,
            "같은 일, CSV 빈 값 처리 후 무엇이 바뀌었는지 확인하기. 왼쪽 OpenCode 순정은 범용 코딩 에이전트가 파일 읽기, 쓰기, "
            "명령 실행으로 필요한 점검과 비교를 그때그때 준비한다. 오른쪽 OMH 통합 구성은 OMO의 역할 협업과 작업 흐름, "
            "업무 도구 data_inspect와 data_compare, 필요할 때 쓰는 작업 절차 omh-rigorous를 한 묶음 안에 담는다")
    sm = {"size": 24, "weight": 400, "fill": INK2}
    s.rect(0, 0, 1680, 54, fill=PAPER2)
    s.text(24, 27, "같은 일", size=26, weight=800, fill=MUTED)
    s.text(150, 27, "CSV 빈 값 처리 후, 무엇이 바뀌었는지 확인", size=28, weight=800)
    s.text(1656, 27, "같은 모델 사용, 추가 학습 없음", size=26, fill=INK2, anchor="end")

    # left: bare OpenCode, a general coding agent environment
    s.rect(0, 80, 620, 390, fill=WHITE, stroke=INK, sw=2.5, extra=' data-box="opencode"')
    s.text(28, 118, "OpenCode 순정", size=32, weight=800)
    s.text(28, 156, "범용 코딩 에이전트 환경", size=24, fill=INK2)
    s.box(28, 184, 564, 96, ["코딩 에이전트", ("파일 읽기, 쓰기, 명령 실행, 계획과 확인", sm)], size=28, weight=800,
          fill=PAPER2, stroke=None, lh=1.4)
    left_steps = ["파일을 열거나 점검 스크립트 작성", "고른 빈 값 규칙 적용", "비교 코드를 그때그때 준비"]
    for k, t in enumerate(left_steps):
        y = 318 + k * 48
        s.text(28, y, str(k + 1), size=26, weight=800, fill=MUTED)
        s.text(64, y, t, size=26)

    # right: the OMH integrated package, which contains OMO
    s.rect(680, 80, 1000, 390, fill="none", stroke=BLUE, sw=4, extra=' data-box="omh"')
    s.text(708, 118, "OMH 통합 구성", size=32, weight=800, fill=BLUE)
    s.text(1652, 118, "OMO + 업무 도구 + 작업 절차", size=26, weight=800, fill=BLUE, anchor="end")
    s.text(708, 156, "OMO의 역할 구성까지 묶은 OMH", size=24, fill=INK2)
    s.rect(708, 184, 280, 112, fill=BLUE_SOFT, stroke=BLUE, sw=2.5, extra=' data-box="omo"')
    s.lines(848, 240, ["OMO", ("역할 협업과 작업 흐름", sm)], size=30, weight=800, anchor="middle", lh=1.5)
    s.rect(1006, 184, 418, 112, fill=WHITE, stroke=BLUE, sw=2.5, extra=' data-box="tools"')
    s.lines(1215, 240, ["업무 도구", ("data_inspect, data_compare", {"size": 24, "weight": 400, "fill": BLUE,
                                                                   "mono": True})], size=30, weight=800,
            anchor="middle", lh=1.5)
    s.rect(1442, 184, 210, 112, fill=WHITE, stroke=BLUE, sw=2.5, extra=' data-box="procedure"')
    s.lines(1547, 240, ["작업 절차", ("omh-rigorous", {"size": 24, "weight": 400, "fill": BLUE, "mono": True})],
            size=30, weight=800, anchor="middle", lh=1.5)
    right_steps = [("data_inspect", "열, 타입, 빈 값 수 요약 (행 값 없이)"), ("", "같은 빈 값 규칙 적용"),
                   ("data_compare", "id 기준 추가, 삭제, 변경 요약 (자동 병합 없음)")]
    for k, (tool, t) in enumerate(right_steps):
        y = 318 + k * 48
        s.text(708, y, str(k + 1), size=26, weight=800, fill=MUTED)
        if tool:
            s.text(744, y, tool, size=24, fill=BLUE, mono=True)
            s.text(944, y, t, size=26)
        else:
            s.text(744, y, t, size=26)

    s.rect(0, 496, 1680, 104, fill=WHITE, stroke=BLUE, sw=3)
    s.text(28, 532, "달라진 것", size=26, weight=800, fill=BLUE)
    s.text(190, 532, "그때그때 꾸리던 역할 분담, 점검, 비교를 한 묶음으로", size=28, weight=800)
    s.text(190, 574, "빈 값 규칙과 결과를 받아들일지는 여전히 사람이 결정", size=24, fill=INK2)
    return s.render()


def omh_body():
    return "\n  ".join([
        case_head(2, "OMH"),
        p("qline case-q", "<b>질문</b>OpenCode만 쓸 때와, OMO까지 묶은 OMH로 같은 일을 할 때 무엇이 달라질까?"),
        p("case-title", "같은 일, OpenCode 순정과 OMH 통합 구성", "h2"),
        omh_svg(),
        p("foot", "설명용 예시. 모의, 오프라인 기능 점검만 했고 실제 사내 모델의 품질 비교는 하지 않음",
          style="left:120px;top:968px;width:1680px;margin:0;color:#B45309;font-weight:700"),
    ])


OMH_NOTES = """<p><strong>비교의 두 쪽:</strong> 왼쪽은 OpenCode 순정, 곧 추가 묶음 없이 쓰는 범용 코딩 에이전트 환경입니다. 오른쪽은 OMH 통합 구성입니다. 이 발표에서 'OMH 통합 구성'은 OMO의 역할 협업과 작업 흐름, OMO의 원래 플러그인과 실행기, 의존성까지 한 패키지에 담고, 그 위에 OMH가 더한 업무 도구(data_inspect, data_compare)와 필요할 때 골라 쓰는 작업 절차(omh-rigorous)를 함께 묶은 것을 말합니다. 그래서 그림에서 OMO는 OMH 경계 안에 있습니다. 두 쪽은 서로 경쟁하는 대안이 아니라, 같은 일을 범용 환경으로 할 때와 묶음으로 할 때입니다.</p>
<p><strong>이름 구분:</strong> 이전 판(v06부터 v09)에서 'OMH'는 OpenCode와 OMO 위에 더한 업무 도구와 절차만을 가리켰습니다. v10부터 14쪽의 'OMH'는 OMO까지 포함한 통합 구성 전체입니다. 업무 도구와 절차만 말할 때는 'OMH가 더한 도구와 절차'라고 부릅니다.</p>
<p><strong>전제 조건:</strong> OpenCode와 Python은 미리 설치돼 있어야 하는 조건이고, 통합 패키지에 들어 있지 않습니다. OMO의 모든 역할은 고른 같은 모델을 함께 씁니다. 역할마다 다른 모델을 쓰거나, 별도의 상주 프로그램이 돌거나, 품질이 자동으로 보장되는 것은 아닙니다. 모델은 그대로이고 학습하지 않았습니다.</p>
<p><strong>왼쪽도 할 수 있는 일:</strong> OpenCode 순정에서도 에이전트가 파일을 읽고 쓰고, 명령을 실행하고, 계획하고 확인할 수 있습니다. 같은 일을 할 수 있으며, 필요한 점검 스크립트와 비교 코드, 절차를 그때그때 준비합니다. 왼쪽 흐름은 설명용 예시이지 측정한 실패 사례가 아닙니다.</p>
<p><strong>달라진 것:</strong> 역할 분담과 작업 흐름(OMO), 구조 점검과 비교 도구(data_inspect는 행 값 없이 열, 타입, 빈 값 수, 점검 범위를 요약하고, data_compare는 정한 키 기준으로 추가, 삭제, 변경 행을 요약하며 자동 병합하지 않음), 필요할 때 쓰는 절차(omh-rigorous)가 한 묶음으로 준비돼 있어 매번 새로 꾸리지 않아도 됩니다. 결과도 같은 형식으로 남습니다.</p>
<p><strong>여전히 사람과 모델이 정하는 것:</strong> 어떤 키로 비교할지, 빈 값을 어떤 규칙으로 처리할지, 비교 결과를 받아들일지는 도구가 정하지 않습니다. 속도나 정확도를 수치로 비교하지 않았습니다.</p>
<p><strong>근거:</strong> 패키지 관계는 OMH 통합 v04 참고 문서(구성과 조건, 역할, 도구)를 따랐습니다. 로컬 보관 자료이며 이 저장소에는 들어 있지 않습니다. 근거의 한계: 설치와 점검 기록, 모의 환경 테스트는 기능이 연결됐다는 증거일 뿐이고, 실제 사내 모델의 품질 비교는 하지 않았습니다.</p>"""

CORRECTIONS = {
    14: ("v10부터 14쪽은 사용자 요청에 따라 'OpenCode 순정'과 'OMO까지 묶은 OMH 통합 구성'을 비교한다. 아래 v10 기획 발췌(S11)와 "
         "v06부터 v09까지의 14쪽은 OpenCode와 OMO를 양쪽 공통 기반으로 두고 OMH가 더한 부분만 비교했는데, 그 비교 축은 이전 판의 "
         "기록이다. 발췌 속 'OMH'는 OMH가 더한 도구와 절차를 가리키며, 이 화면의 'OMH 통합 구성'과 범위가 다르다."),
}

# ---------------------------------------------------------------- slide 15: AS-IS Superpowers to TO-BE pstack


def ref_a():
    s = Svg("s15", 120, 330, 1680, 620, "이 발표가 고른 전환 방향. AS-IS Superpowers: 의도와 설계 합의, 작은 단위로 계획, "
            "테스트 먼저 구현과 작업별 검토, 브랜치 전체 검토. 큰 화살표로 TO-BE pstack: 작업별 플레이북 고르기, "
            "구조 파악과 설계, 범위를 정해 위임, 실제 동작으로 검증. 둘 다 계획, 위임, 검토, 테스트를 할 수 있다")
    sm = {"size": 24, "weight": 400, "fill": INK2}
    xs = [340, 680, 1020, 1360]
    # AS-IS: Superpowers
    s.box(0, 10, 300, 150, [("AS-IS", {"size": 24, "weight": 800, "fill": MUTED}), "Superpowers",
                            ("설계 합의와 단계 검토", sm)], size=32, weight=800, fill=PAPER2, stroke=INK, lh=1.35)
    asis = [["의도와 설계 합의", ("작업 크기에 맞게", sm)], ["작은 단위로 계획", ("파일, 확인 방법까지", sm)],
            ["테스트 먼저 구현", ("명세, 품질 함께 검토", sm)], ["브랜치 전체 검토", ("마무리 방식 선택", sm)]]
    for k, (x, lines) in enumerate(zip(xs, asis)):
        s.box(x, 10, 300, 150, lines, size=28, weight=800, fill=WHITE, stroke=INK, sw=2.5)
        if k < 3:
            s.arrow([(x + 302, 85), (xs[k + 1] - 6, 85)])
    s.arrow([(300, 85), (334, 85)])
    # transition arrow
    s.add('<polygon points="900,178 1100,178 1100,210 1170,210 1000,262 830,210 900,210" fill="#2457A6"/>')
    s.text(1196, 222, "작업별 절차 선택으로", size=28, weight=800, fill=BLUE)
    # TO-BE: pstack
    s.box(0, 280, 300, 150, [("TO-BE", {"size": 24, "weight": 800, "fill": WHITE}), "pstack",
                             ("작업별 플레이북, 위임, 검증", {"size": 24, "weight": 400, "fill": WHITE})],
          size=32, weight=800, fill=BLUE, stroke=BLUE, color=WHITE, lh=1.35)
    tobe = [["작업별 플레이북", ("이번엔 기능 플레이북", sm)], ["구조 파악, 설계", ("영향 범위, 데이터 구조", sm)],
            ["범위 정해 위임", ("성공 기준, 안전한 분할", sm)], ["실제 동작으로 검증", ("결과와 근거 대조", sm)]]
    for k, (x, lines) in enumerate(zip(xs, tobe)):
        s.box(x, 280, 300, 150, lines, size=28, weight=800, fill=BLUE_SOFT, stroke=BLUE, sw=3)
        if k < 3:
            s.arrow([(x + 302, 355), (xs[k + 1] - 6, 355)], color="blue")
    s.arrow([(300, 355), (334, 355)], color="blue")
    s.rect(0, 470, 1680, 130, fill=PAPER2)
    s.text(28, 512, "바뀌는 초점", size=26, weight=800, fill=BLUE)
    s.text(200, 512, "설계 합의와 단계별 검토 중심에서, 작업별 플레이북과 범위 정한 위임, 실제 동작 검증 중심으로", size=28,
           weight=800)
    s.text(200, 558, "공통 기반: 계획, 위임, 검토와 테스트", size=24,
           fill=INK2)
    body = "\n  ".join([
        copy_v07._head("참고 A", "Superpowers에서 pstack으로"),
        p("qline case-q", "<b>질문</b>같은 기능 추가 요청(가상): CSV 내보내기. 무엇을 먼저 챙기는 방식으로 바꿔 볼까?"),
        p("case-title", "AS-IS Superpowers, TO-BE pstack", "h2"),
        s.render(),
        p("foot", e(copy_v07.PROVENANCE), style="left:120px;top:968px;width:1680px;margin:0"),
    ])
    notes = f"""<p><strong>이 화면의 위치:</strong> 본문(25개 용어와 다섯 사례)에 들지 않는 참고 화면입니다. 필요하면 오른쪽 위 '본문으로'를 눌러 {copy_v07.SKIP_TO}쪽으로 건너뜁니다.</p>
<p><strong>전환 관점:</strong> 이 발표는 Superpowers식 흐름을 지금의 방식(AS-IS)으로, pstack식 흐름을 바꿔 가려는 방향(TO-BE)으로 놓고 봅니다. 이 발표가 고른 관점이며, 어느 쪽이 더 성숙하다는 단계표나 제품 순위가 아닙니다. 실제 조직이 이미 이 전환을 마쳤다는 기록도 아닙니다.</p>
<p><strong>AS-IS, Superpowers:</strong> brainstorming이 먼저 의도를 끌어내고 이해한 내용을 되짚습니다. 작은 변경은 대화로, 큰 작업은 설계 문서로 합의합니다. 이어서 작은 단위의 계획을 쓰고, 실행할 때는 작업마다 새 하위 에이전트가 테스트 먼저(RED, GREEN, REFACTOR) 구현하고 작업별 검토 한 번이 명세 충족과 코드 품질을 함께 봅니다. 마지막에 브랜치 전체를 검토하고 마무리 방식을 고릅니다. 하위 에이전트 대신 한 세션에서 실행하고 마지막에 한 번 검토하는 방식(executing-plans)도 있습니다.</p>
<p><strong>TO-BE, pstack:</strong> poteto-mode가 요청을 보고 작업에 맞는 플레이북(README 기준 23개)을 고릅니다. 2단계부터는 기능 플레이북을 고른 경우의 예이며, 플레이북마다 단계는 다릅니다. 기능 플레이북은 영향 범위를 파악하고 설계를 탐색한 뒤, 먼저 끝낼 단계, 독립 작업, 공유 상태, 가장 작은 안전한 분할을 점검하고, 파일 범위와 데이터 구조, 성공 기준을 정해 구현을 맡깁니다. 그다음 실제 동작으로 검증합니다. 코드, 테스트, 실행 결과를 근거와 대조하는 것이며, 화면 캡처만 보는 것이 아닙니다. 한 기능처럼 코드가 엮인 일은 한 담당자에게 둡니다.</p>
<p><strong>바뀌는 것과 바뀌지 않는 것:</strong> 바뀌는 것은 무엇을 먼저 챙기는지입니다. 설계 합의와 단계별 검토 중심에서, 작업에 맞는 플레이북과 범위를 정한 위임, 실제 동작으로 하는 검증 중심으로 옮겨 갑니다. pstack에도 계획과 테스트가 있고 Superpowers에도 위임과 검토가 있습니다. 전환한다고 정확도나 속도가 저절로 오른다고 말하지 않으며, 잰 수치도 없습니다.</p>
<p><strong>실행 환경:</strong> pstack은 Cursor 이름으로 쓰여 있고 Claude Code용 어댑터가 이름을 바꿔 대응하며, Cursor 전용 기능은 건너뜁니다. 호스트마다 똑같이 동작한다고 말하지 않습니다. Superpowers도 여러 코딩 에이전트에 설치 경로를 안내합니다.</p>
<p><strong>표기 주의:</strong> Superpowers README의 스킬 목록에는 '두 단계 검토'라는 표현이 남아 있지만, 같은 커밋의 subagent-driven-development 본문은 작업별 검토 한 번이 명세와 품질을 함께 본다고 설명합니다. 이 화면은 스킬 본문을 따랐습니다.</p>
{copy_v07._sources_html()}"""
    return dict(kind="reference", reference="A", label="참고 A: AS-IS Superpowers, TO-BE pstack",
                theme="t-paper", body=body, notes=notes, chapter=2, layout="reference")


# ---------------------------------------------------------------- slide 16: keep in step with 14 and 15

REF_B_EDITS = [
    ('>pstack에서 눈여겨볼 것<', '>TO-BE pstack에서 가져올 것<'),
    ('>Superpowers (비교 참고)<', '>AS-IS Superpowers (비교 참고)<'),
    # Superpowers is a reference for the current way, not OMH lineage: its line becomes dashed
    ('<polyline points="520,282 570,282 570,270 614,270" fill="none" stroke="#14171C" stroke-width="3" marker-end="url(#s16-ink)"/>',
     '<polyline points="520,282 570,282 570,270 614,270" fill="none" stroke="#5E6570" stroke-width="3" stroke-dasharray="9 7" marker-end="url(#s16-muted)"/>'),
    # OMH panel: the model stays the same, OMO is included in OMH rather than a shared base
    ('>그대로</text>', '>같음</text>'),
    ('<text x="1310" y="150" font-size="26" font-weight="700" fill="#14171C" dominant-baseline="central">OpenCode와 OMO 역할</text>',
     '<text x="1190" y="150" font-size="24" font-weight="800" fill="#5E6570" dominant-baseline="central">포함</text>'
     '<text x="1310" y="150" font-size="26" font-weight="700" fill="#14171C" dominant-baseline="central">OMO 역할 구성</text>'),
    ('설정된 모델과 OpenCode, OMO 역할을 그대로 두고 업무 도구와 omh-rigorous를 더한다',
     'OMO의 역할 구성까지 묶고 설정된 모델은 같게 두며 업무 도구와 omh-rigorous를 더한다'),
]

REF_B_NOTES = [
    ("<p><strong>OMH와의 연결:</strong> 적용 예로 든 OMH는 설정된 모델 하나와 OpenCode, OMO의 기존 역할을 그대로 두고, 업무 도구(data_inspect, data_compare)와 필요할 때 골라 쓰는 절차(omh-rigorous)를 더했습니다(14쪽).",
     "<p><strong>OMH와의 연결:</strong> 적용 예로 든 OMH는 14쪽의 OMH 통합 구성입니다. OMO의 역할 구성까지 한 묶음에 담고, 설정된 모델 하나를 그대로 쓰며, 업무 도구(data_inspect, data_compare)와 필요할 때 골라 쓰는 절차(omh-rigorous)를 더했습니다. 오른쪽 상자의 '포함'은 OMO가 OMH 안에 들어 있다는 뜻입니다."),
    ("<p><strong>Superpowers의 자리:</strong> Superpowers는 여기서 비교용 참고이며, OMH 구현의 근거로 제시하지 않습니다.",
     "<p><strong>Superpowers의 자리:</strong> 15쪽에서 Superpowers는 AS-IS, pstack은 TO-BE입니다. 이 화면에서도 pstack은 가져올 방향, Superpowers는 지금 방식의 비교 참고이며, OMH 구현의 근거로 제시하지 않습니다. 그래서 Superpowers에서 가운데로 가는 선은 점선입니다."),
]


def _ref_b(sl):
    body, notes = sl["body"], sl["notes"]
    for old, new in REF_B_EDITS:
        if body.count(old) != 1:
            raise SystemExit(f"v10 slide 16: expected one match for {old[:60]}")
        body = body.replace(old, new)
    for old, new in REF_B_NOTES:
        if notes.count(old) != 1:
            raise SystemExit(f"v10 slide 16 notes: expected one match for {old[:60]}")
        notes = notes.replace(old, new)
    sl["body"], sl["notes"] = body, notes


def apply(orig, sl):
    if orig == 14:
        sl["body"] = omh_body()
        sl["notes"] = OMH_NOTES


def apply_refs(slides):
    out = []
    for sl in slides:
        if sl.get("reference") == "A":
            out.append(ref_a())
        else:
            if sl.get("reference") == "B":
                _ref_b(sl)
            out.append(sl)
    return out
