"""Tile the slide renders into contact sheets of twelve.

Usage (from the project root, after check_v02.mjs):
    python3 slides/src/v02/contact_sheet_deck.py [v10]

Writes slides/render/VER/contact-1.png to contact-4.png (git-ignored); the
version defaults to v10. Needs Pillow and fontconfig (fc-match) to find
Nanum Gothic for the labels.
"""

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
VER = sys.argv[1] if len(sys.argv) > 1 else "v10"
DIR = ROOT / "slides" / "render" / VER
MANIFEST = ROOT / "slides" / f"harness-engineering-workshop-{VER}.manifest.json"
W, H, PAD, LAB, COLS, PER = 576, 324, 28, 40, 3, 12


def main():
    items = json.loads(MANIFEST.read_text(encoding="utf-8"))["items"]
    fontfile = subprocess.run(["fc-match", "-f", "%{file}", "Nanum Gothic"],
                              capture_output=True, text=True, check=True).stdout
    font = ImageFont.truetype(fontfile, 22, index=1)
    for sheet_no, start in enumerate(range(0, len(items), PER), 1):
        chunk = items[start:start + PER]
        rows = (len(chunk) + COLS - 1) // COLS
        sheet = Image.new("RGB", (COLS * W + (COLS + 1) * PAD, rows * (H + LAB + PAD) + PAD), "#D9D6CF")
        draw = ImageDraw.Draw(sheet)
        for i, it in enumerate(chunk):
            n = it["physical"]
            im = Image.open(DIR / f"s{n:02d}.png").convert("RGB").resize((W, H), Image.LANCZOS)
            x = PAD + (i % COLS) * (W + PAD)
            y = PAD + (i // COLS) * (H + LAB + PAD)
            timing = f"{it['minutes']}분, " if "minutes" in it else ""  # v04 manifests carry no lecture time
            draw.text((x, y + 6), f"{n}. {it['label']}  ({timing}{it.get('layout', it['kind'])})",
                      fill="#14171C", font=font)
            sheet.paste(im, (x, y + LAB))
        out = DIR / f"contact-{sheet_no}.png"
        sheet.save(out)
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
