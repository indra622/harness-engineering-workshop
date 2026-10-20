"""Text measurement with the real Nanum Gothic metrics.

Depends only on Pillow and fontconfig's `fc-match`, so the HTML build does
not need python-pptx or lxml.
"""

import subprocess
from functools import lru_cache

from PIL import ImageFont

from . import theme as T


@lru_cache(maxsize=None)
def _font_file():
    out = subprocess.run(["fc-match", T.FONT, "--format=%{file}"],
                         capture_output=True, text=True, check=True).stdout
    return out.strip()


@lru_cache(maxsize=None)
def _pil(size_pt, bold):
    # Nanum Gothic TTC: index 0 Regular, 1 Bold
    return ImageFont.truetype(_font_file(), size_pt * 10, index=1 if bold else 0)


def text_width_in(s, size_pt, bold=False):
    """Rendered width of one line in inches (font measured at 10x for precision)."""
    if not s:
        return 0.0
    return _pil(size_pt, bold).getlength(s) / 10 / 72
