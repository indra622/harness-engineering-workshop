# Deck source

## v03 (current) and v02

The current deck is v03: 42 slides, 120 minutes, built from `v02/` (the folder name is historical; one builder makes both versions). Visual rules are in `DESIGN.md` at the project root. Content comes from `docs/plans/slide-content-plan-v10.md` and `docs/production/slide-production-brief-v02.md`; the brief's three "v02 정정" items and the v03 correction on slide 2 override ambiguous v10 wording. Each correction appears in the notes before the untouched v10 block.

v03 differs from v02 in two places only:
- a physical page number, "n / 42", inside every canvas at the bottom right, so screen, print and PDF all carry it (theme-aware colour, clear of the footers);
- slide 2: the author finds and selects the topic and writes the first draft v01 personally; AI joins for review and revision; the author confirms; then illustration and archive, Naver private draft, reopen verification. v01 is the author's original, not AI-generated.

Outputs for VER = v03 (current) or v02 (kept as exported):
- `slides/harness-engineering-workshop-VER.html`: canonical single-file export, CSS and JS inlined.
- `slides/index.html`: current entry, the same file as the v03 export.
- `slides/harness-engineering-workshop-VER.pdf`: browser print, 42 pages, 16:9.
- `slides/speaker-notes-VER.md`: presenter notes as Markdown.
- `slides/harness-engineering-workshop-VER.manifest.json`: physical number, kind, layout, chapter, minutes, term, case and v10 source for every slide. The same data is on each `<section>` as `data-` attributes and in the page as `#deck-manifest`.
- `slides/VER-check-evidence.json`: the browser check result.
- `slides/render/VER/`: one PNG per slide, interaction and viewport screenshots, contact sheets. Git-ignored and regenerated.

Layout of `v02/`:
- `kit.py`: SVG drawing kit on canvas pixels (boxes, lines, arrows, ticks), plus small HTML helpers. `kit.VERSION` tells slide functions which version is being built.
- `deck_a.py`, `deck_b.py`: one function per physical slide, 1 to 21 and 22 to 42. Each returns the slide's kind, chapter, term or case, v10 source, layout family and body. Slide 2 has a v02 and a v03 variant.
- `deck.src.html`, `v02.css`, `v02.js`: page shell, styles and navigation, inlined by the build. The page-number styles live in `build_v02.py` and are added only from v03, so v02 output stays byte-identical.
- `build_v02.py`: assembles the deck and the notes for `--version v03` (default) or `--version v02`; `--out-dir` writes elsewhere and never touches `slides/index.html`. Term and case notes start with the scene, then any correction, then the full v10 block under a source heading. Stops before writing if the deck no longer adds up (42 slides, 120 minutes, the 25 v10 terms in order, five cases, one three-minute CEO Agent slide, a ten-minute break) or if the output contains a middle dot, a host path or a session link. Standard library only.
- `check_v02.mjs`: headless Chrome check through an existing Playwright install; `DECK_VERSION` selects the version (default v03).
- `contact_sheet_deck.py`: tiles the renders into four contact sheets (Pillow and fontconfig); takes the version as an argument.
- `proof.src.html`, `build_proof.py`, `check_proof.mjs`, `contact_sheet.py`: the six-screen redesign proof in `slides/previews/`, kept as a record.

Rebuild and check the current deck, from the project root:

```sh
python3 slides/src/v02/build_v02.py
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.js node slides/src/v02/check_v02.mjs
python3 slides/src/v02/contact_sheet_deck.py v03
```

Confirm v02 still reproduces without touching the delivered files:

```sh
python3 slides/src/v02/build_v02.py --version v02 --out-dir /tmp/v02-rebuild
cmp slides/harness-engineering-workshop-v02.html /tmp/v02-rebuild/harness-engineering-workshop-v02.html
```

Do not run `check_v02.mjs` with `DECK_VERSION=v02` unless you mean to replace the delivered v02 PDF and evidence.

`check_v02.mjs` covers:
- manifest and `data-` attributes: 42 slides, 120 minutes, the 25 v10 terms in order, five cases, one three-minute CEO Agent slide, a ten-minute break, at least three term layout families;
- notes: every term and case slide carries its full v10 block; slides 9, 23, 29 and 30 show their v02 correction before it, and from v03 slide 2 shows its v03 correction;
- page numbers (v03): every slide shows "n / 42" in the bottom-right safe corner, and every PDF page's own text contains its number (poppler `pdftotext`);
- every visible text run: inside the 40 px safe margin, at least 24 px on the canvas, no overlap, no clipped box;
- diagram labels: each SVG label stays inside the box it sits in, and no visible connector runs through a label;
- keyboard, buttons, notes, deep links (`#s31` with notes, `#7`), the F full-screen toggle;
- 1280 x 720, 1920 x 1080 with notes, 390 x 844 with and without notes;
- the no-JavaScript fallback;
- the single file copied into an empty temporary folder;
- print from slide 20 to a 42-page 16:9 PDF;
- console errors and network requests.

Passing checks are not a presentation review. Look at the renders and the contact sheets.

## v01 (historical)

The v01 sections below describe the earlier 35-slide deck. Its entry is now `slides/index-v01.html`, so rebuilding v01 does not overwrite the current entry. The v01 single-file export, PDF and `slides/speaker-notes.md` are kept unchanged.

The v01 HTML presentation was built by a Python generator that writes `slides/index-v01.html` with one inline SVG diagram per slide, plus a single-file export and the presenter notes. Its visual rules are in `docs/design/DESIGN-v01.md`. Its content came from `docs/plans/slide-content-plan-v10.md` and `docs/production/slide-production-brief-v01.md`.

## Outputs

- `slides/index-v01.html`: the v01 presentation. Uses `slides/assets/deck.css` and `slides/assets/deck.js`.
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
