"""Tile rendered PNG pages into one contact sheet for quick review.

Usage (from the project root, after render.sh):
    python3 slides/src/contact_sheet.py slides/previews/representative-v01
"""

import sys
from pathlib import Path

from PIL import Image

COLS, THUMB_W, GAP = 3, 720, 24


def main(folder):
    folder = Path(folder)
    pages = sorted(folder.glob("page-*.png"))
    thumbs = []
    for p in pages:
        im = Image.open(p).convert("RGB")
        thumbs.append(im.resize((THUMB_W, round(im.height * THUMB_W / im.width))))
    th = thumbs[0].height
    rows = (len(thumbs) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * THUMB_W + (COLS + 1) * GAP, rows * th + (rows + 1) * GAP),
                      (205, 209, 214))
    for i, im in enumerate(thumbs):
        r, c = divmod(i, COLS)
        sheet.paste(im, (GAP + c * (THUMB_W + GAP), GAP + r * (th + GAP)))
    out = folder / "contact-sheet.png"
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
