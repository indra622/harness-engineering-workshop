"""Tile the six v02 proof renders into one contact sheet.

Usage (from the project root, after check_proof.mjs):
    python3 slides/src/v02/contact_sheet.py

Writes slides/previews/redesign-v02/contact-sheet.png. Needs Pillow and
fontconfig (fc-match) to find Nanum Gothic for the labels.
"""

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "slides" / "previews" / "redesign-v02"
NAMES = ["P1-cover", "P2-chapter-1", "P3-term-runtime", "P4-case-omh", "P5-case-ceo", "P6-closing"]
W, H, PAD, LAB = 640, 360, 32, 44


def main():
    fontfile = subprocess.run(["fc-match", "-f", "%{file}", "Nanum Gothic"],
                              capture_output=True, text=True, check=True).stdout
    font = ImageFont.truetype(fontfile, 24, index=1)
    sheet = Image.new("RGB", (3 * W + 4 * PAD, 2 * (H + LAB) + 3 * PAD), "#D9D6CF")
    draw = ImageDraw.Draw(sheet)
    for i, name in enumerate(NAMES):
        im = Image.open(DIR / f"{name}.png").convert("RGB").resize((W, H), Image.LANCZOS)
        x = PAD + (i % 3) * (W + PAD)
        y = PAD + (i // 3) * (H + LAB + PAD)
        draw.text((x, y + 6), name, fill="#14171C", font=font)
        sheet.paste(im, (x, y + LAB))
    out = DIR / "contact-sheet.png"
    sheet.save(out)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
