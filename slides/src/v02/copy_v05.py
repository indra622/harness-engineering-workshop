"""v05: remove only the roadmap break marker; keep the separate break slide."""
import re


def apply(n, slide):
    if n != 3:
        return
    marker = '<div class="abs road-break" style="left:1144px"><span>쉬는 시간</span></div>'
    if slide["body"].count(marker) != 1:
        raise SystemExit("v05 roadmap break marker missing or duplicated")
    body = slide["body"].replace(marker, "")
    positions = iter(120 + 341 * i for i in range(5))
    body, count = re.subn(r'<div class="abs road-col" style="left:\d+px">',
                         lambda _: f'<div class="abs road-col" style="left:{next(positions)}px">', body)
    if count != 5:
        raise SystemExit("v05 roadmap must have five columns")
    slide["body"] = body
    slide["notes"] = slide["notes"].replace("<p>3장과 4장 사이에 쉬는 시간이 있습니다.</p>", "")
