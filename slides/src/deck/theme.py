"""Design tokens for the workshop deck. Mirrors DESIGN.md at the project root.

All font sizes are in points (pt). All positions are in inches on a
13.333 x 7.5 inch (16:9) slide.
"""

SLIDE_W = 13.333
SLIDE_H = 7.5
SAFE = 0.4          # minimum edge clearance for any shape
MARGIN = 0.5        # left and right content margin
RIGHT = SLIDE_W - MARGIN
BOTTOM_LIMIT = 6.52  # diagrams end above the footnote line

FONT = "Nanum Gothic"

COLORS = {
    "canvas": "F7F7F4",      # slide background
    "ink": "1F2328",         # primary text and default lines
    "muted": "5B6470",       # secondary text, retained or out-of-scope outlines
    "primary": "2B5FA8",     # current focus, transitions, things we added
    "warning": "B45309",     # human gate, caution, unverified source
    "band": "E9ECF1",        # question strip and lane bands
    "focus_fill": "E7EEF8",  # fill behind primary-outlined shapes
    "surface": "FFFFFF",     # node fill
    "hairline": "C5CBD3",    # tile outlines
}

SIZE = {
    "title": 36,
    "body": 24,
    "label": 20,      # minimum for diagram labels
    "footnote": 16,
    "meta": 16,
}

LINE = {
    "hair": 1.0,
    "default": 1.25,
    "focus": 2.25,
    "gate": 3.0,
    "connector": 1.5,
}
