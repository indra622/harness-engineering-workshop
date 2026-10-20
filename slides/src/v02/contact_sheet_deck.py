"""Tile the 42 v02 slide renders into contact sheets of twelve.

Usage (from the project root, after check_v02.mjs):
    python3 slides/src/v02/contact_sheet_deck.py

Writes slides/render/v02/contact-1.png to contact-4.png (git-ignored). Needs
Pillow and fontconfig (fc-match) to find Nanum Gothic for the labels.
"""

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "slides" / "render" / "v02"
MANIFEST = ROOT / "slides" / "harness-engineering-workshop-v02.manifest.json"
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
            draw.text((x, y + 6), f"{n}. {it['label']}  ({it['minutes']}분, {it.get('layout', it['kind'])})",
                      fill="#14171C", font=font)
            sheet.paste(im, (x, y + LAB))
        out = DIR / f"contact-{sheet_no}.png"
        sheet.save(out)
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
