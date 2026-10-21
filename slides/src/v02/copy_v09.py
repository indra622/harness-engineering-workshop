"""v09: include the scheduler in the gateway caption on slide9."""


def apply(original, slide):
    if original != 9:
        return
    old = "채널과 세션"
    assert slide["body"].count(old) == 1
    slide["body"] = slide["body"].replace(old, "채널, 세션, 스케줄러")
