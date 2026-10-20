# Deck source

The HTML presentation is the canonical output. A Python generator writes `slides/index.html` with one inline SVG diagram per slide, plus a single-file export and the presenter notes. A browser check then verifies the result in real headless Chrome. Visual rules are in `DESIGN.md` at the project root. Content comes from `docs/plans/slide-content-plan-v10.md` and `docs/production/slide-production-brief-v01.md`.

## Outputs

- `slides/index.html`: the presentation. Uses `slides/assets/deck.css` and `slides/assets/deck.js`.
- `slides/harness-engineering-workshop-v01.html`: the same deck in one file, with CSS and JS inlined.
- `slides/harness-engineering-workshop-v01.pdf`: browser print, 35 pages, 16:9.
- `slides/speaker-notes.md`: the presenter notes as Markdown.
- `slides/html-check-evidence.json`: the latest browser check result.
- `slides/render/`: slide and interaction screenshots from the check. Git-ignored and regenerated each run.

## Layout

- `web/kit.py`: SVG drawing kit (text, nodes, containers, lanes, arrows) on a 13.333 x 7.5 inch viewBox.
- `web/frame.py`: the shared slide frame (meta row, title, question strip, key sentence, footnote).
- `web/slides.py`: one function per source slide ID, S1 to S35. `SCREEN_TITLES` holds on-screen titles that differ from the canonical v10 title, which stays in the notes.
- `deck/theme.py`, `deck/notes.py`, `deck/metrics.py`: shared design tokens, notes extraction and Nanum Gothic text measurement. These three use only the Python standard library and Pillow; they are shared with the PPTX experiment.
- `build_html.py`: builds the HTML, the single-file export and the notes, after layout checks.
- `check_html.mjs`: headless Chrome check through an existing Playwright install.
- `../assets/deck.css`, `../assets/deck.js`: hand-written page styles and navigation.

## Requirements

HTML build (`build_html.py`):
- Python 3 with Pillow. python-pptx and lxml are not needed; the HTML build does not import them.
- fontconfig (`fc-match`) and the Nanum Gothic font.

Browser check (`check_html.mjs`):
- Node.js, an existing Playwright install, and Google Chrome. Nothing is downloaded. Point `PLAYWRIGHT_MODULE` at that install's `playwright/index.js`.

Legacy PPTX experiment (`build_deck.py`, `audit_deck.py`, `render.sh`):
- Python 3 with python-pptx 1.0.2, lxml and Pillow.
- LibreOffice (`soffice`) and poppler (`pdftoppm`, `pdftotext`, `pdfinfo`, `pdffonts`).

## Rebuild and check

From the project root:

```sh
python3 slides/src/build_html.py
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.js node slides/src/check_html.mjs
```

`build_html.py` stops without writing anything if a slide fails a layout check:
- a shape inside the 0.4 in edge margin;
- text wider or taller than its box, measured with Nanum Gothic;
- a font below 20 pt in diagrams or 16 pt elsewhere;
- unintended overlap;
- a connector crossing a box.

`check_html.mjs` covers the rendered page:
- 35 slides in v10 order, and the minutes total 120;
- notes on every slide, including the canonical title;
- no raster images;
- each slide's rendered text measured against its box in the live DOM;
- keyboard, buttons, notes and deep links;
- four viewport sizes, from desktop to phone;
- the no-JavaScript fallback;
- print to a 35-page 16:9 PDF;
- the single-file export loaded from a folder with no assets next to it;
- console errors and network requests.

It also writes a screenshot of every slide.

## Legacy PPTX experiment

`build_deck.py`, `render.sh`, `audit_deck.py`, `contact_sheet.py` and `deck/kit.py`, `deck/frame.py`, `deck/slides.py` built the six editable PowerPoint proof slides in `slides/previews/`. They are kept for reference and are not the canonical output. Rebuild them with:

```sh
python3 slides/src/build_deck.py --set representative --out slides/previews/representative-v01.pptx
sh slides/src/render.sh slides/previews/representative-v01.pptx
python3 slides/src/audit_deck.py slides/previews/representative-v01.pptx
```
