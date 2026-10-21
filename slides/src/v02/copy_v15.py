"""v15: two lines in slide 14's summary; layout and other screens stay as v14."""

SUMMARY = "반복할수록, 복잡할수록 커지는 하네스의 효용"
DETAIL = "분업, 비교, 재검토 절차를 재사용해 복잡한 반복 작업의 준비와 확인 부담을 줄이기"

EDITS = [
    ("역할을 나눠 맡기고, 준비된 비교로 요청 밖 변경을 보고 전에 확인", SUMMARY),
    ("OpenCode 순정도 네 단계를 할 수 있지만, 비교 도구와 검토 연결은 직접 준비해야 함", DETAIL),
]

NOTE = """<p><strong>반복성과 복잡성에 따른 효용:</strong> 이 화면의 선택 이유는 한 번의 단순한 일을 무조건 더 많은 역할로 처리하자는 것이 아닙니다. 비슷한 작업을 반복하면 역할 배정, 비교 방식 준비, 검토 기준 확인과 재수정 연결도 반복됩니다. 그 작업이 복잡해 챙길 관계와 검증 지점이 많을수록, 미리 갖춘 분업과 검증 절차를 재사용하는 가치가 커진다는 것이 이 발표의 메시지입니다. 실제 속도나 비용을 측정한 결과나 복잡도에 비례한 성능 보장은 아닙니다. 단발성이고 단순한 작업에서는 순정이 더 가벼울 수 있고, 하네스 자체의 준비와 유지, 조율 비용도 있습니다. 순정에서도 절차와 도구를 잘 갖춰 재사용하면 자기 업무에 맞는 하네스를 만든 셈입니다.</p>"""


def apply(orig, sl):
    if orig != 14:
        return
    for old, new in EDITS:
        if sl["body"].count(old) != 1:
            raise SystemExit(f"v15 slide 14: expected one summary match for {old}")
        sl["body"] = sl["body"].replace(old, new, 1)
    sl["notes"] = NOTE + sl["notes"]
