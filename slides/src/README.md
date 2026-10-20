# Deck source

## v04 (current), v03 and v02

The current deck is v04: 42 slides, built from `v02/` (the folder name is historical; one builder makes all three versions).

v04 keeps v03's slides, diagrams, page numbers and author-first slide 2, and changes two things:
- no lecture timing anywhere: not on screen, in aria labels, in the page head, in presenter notes, in the manifest or in `data-` attributes. The v04 build does not enforce 120 minutes. Tool and task times inside examples (dates, a trigger "time" condition) are content and stay.
- edited presentation copy: `v02/copy_v04.py` holds curated exact-text edits per slide (headings, definitions as noun phrases, scenes, captions, SVG labels, footers), v04 notes for the chapter, opening and closing slides, and the v10 excerpt editor. Every edit must match its slide or the build stops. Each v10 block in the v04 notes is labelled "v10 발췌 SN (v04 편집)", drops only lecture-time lines, and points to the untouched source plan.

v02 and v03 (below) carry the 120-minute schedule and still rebuild byte for byte.

v03 is built the same way: Visual rules are in `DESIGN.md` at the project root. Content comes from `docs/plans/slide-content-plan-v10.md` and `docs/production/slide-production-brief-v02.md`; the brief's three "v02 정정" items and the v03 correction on slide 2 override ambiguous v10 wording. Each correction appears in the notes before the untouched v10 block.

v03 differs from v02 in two places only:
- a physical page number, "n / 42", inside every canvas at the bottom right, so screen, print and PDF all carry it (theme-aware colour, clear of the footers);
- slide 2: the author finds and selects the topic and writes the first draft v01 personally; AI joins for review and revision; the author confirms; then illustration and archive, Naver private draft, reopen verification. v01 is the author's original, not AI-generated.

Outputs for VER = v04 (current), v03 or v02 (kept as exported):
- `slides/harness-engineering-workshop-VER.html`: canonical single-file export, CSS and JS inlined.
- `slides/index.html`: current entry, the same file as the v04 export.
- `slides/harness-engineering-workshop-VER.pdf`: browser print, 42 pages, 16:9.
- `slides/speaker-notes-VER.md`: presenter notes as Markdown.
- `slides/harness-engineering-workshop-VER.manifest.json`: physical number, kind, layout, chapter, minutes, term, case and v10 source for every slide. The same data is on each `<section>` as `data-` attributes and in the page as `#deck-manifest`.
- `slides/VER-check-evidence.json`: the browser check result.
- `slides/render/VER/`: one PNG per slide, interaction and viewport screenshots, contact sheets. Git-ignored and regenerated.

Layout of `v02/`:
- `kit.py`: SVG drawing kit on canvas pixels (boxes, lines, arrows, ticks), plus small HTML helpers. `kit.VERSION` tells slide functions which version is being built.
- `deck_a.py`, `deck_b.py`: one function per physical slide, 1 to 21 and 22 to 42. Each returns the slide's kind, chapter, term or case, v10 source, layout family and body. Slide 2 has a v02 and a v03 variant.
- `deck.src.html`, `v02.css`, `v02.js`: page shell, styles and navigation, inlined by the build. The page-number styles live in `build_v02.py` and are added only from v03, so v02 output stays byte-identical.
- `copy_v04.py`: v04 copy edits, v04 notes, v10 excerpt editor and the lecture-time pattern.
- `build_v02.py`: assembles v07 by default (44 slides including two optional reference slides); `--version v02` through `v06` reproduces the preserved 42-slide versions. `--out-dir` writes elsewhere without changing the current index. Original source and correction IDs stay stable as physical page numbers move. Lecture timing exists only in historical v02/v03; current exports omit it. Standard library only.
- `check_v02.mjs`: headless Chrome check through an existing Playwright install; `DECK_VERSION` selects the version (default v07).
- `contact_sheet_deck.py`: tiles the renders into four contact sheets (Pillow and fontconfig); takes the version as an argument.
- `proof.src.html`, `build_proof.py`, `check_proof.mjs`, `contact_sheet.py`: the six-screen redesign proof in `slides/previews/`, kept as a record.

Rebuild and check the current deck, from the project root:

```sh
python3 slides/src/v02/build_v02.py
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.js node slides/src/v02/check_v02.mjs
python3 slides/src/v02/contact_sheet_deck.py v04
```

Confirm v02 and v03 still reproduce without touching the delivered files:

```sh
python3 slides/src/v02/build_v02.py --version v02 --out-dir /tmp/v02-rebuild
cmp slides/harness-engineering-workshop-v02.html /tmp/v02-rebuild/harness-engineering-workshop-v02.html
python3 slides/src/v02/build_v02.py --version v03 --out-dir /tmp/v03-rebuild
cmp slides/harness-engineering-workshop-v03.html /tmp/v03-rebuild/harness-engineering-workshop-v03.html
```

Do not run `check_v02.mjs` with `DECK_VERSION=v02` or `v03` unless you mean to replace that version's delivered PDF and evidence.

`check_v02.mjs` covers:
- manifest and `data-` attributes: 42 slides, the 25 v10 terms in order, five cases, one CEO Agent slide, one break, at least three term layout families; for v02 and v03 also 120 minutes, a three-minute CEO Agent slide and a ten-minute break; for v04 no schedule field at all;
- lecture time (v04): none on screen, in aria labels, in the page head or in the notes;
- notes: in v02 and v03 every term and case slide carries its full v10 block; in v04 it carries the labelled edited excerpt with every teaching line (scene, definition, re-application, backup example, distinction, check question) intact; slides 9, 23, 29 and 30, and from v03 slide 2, show their correction before the v10 text;
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

### v07 reference slides

v07 keeps the 42 v06 slides and inserts two optional reference slides after original slide 14 (OMH), so the deck has 44 pages. `copy_v07.py` holds the layer:
- `ref_a()` and `ref_b()`: 참고 A (pstack and Superpowers on the same feature request) and 참고 B (what to take: ways of working, applied to OMH). Kind `reference`, not counted among the 25 terms or five cases. Each has a "본문으로, 17쪽" skip link and notes with links pinned to cursor/plugins 111cf6a (pstack 0.15.29) and obra/superpowers b739a8a (7.0.0). The sources are reference data, not workflows this deck runs.
- `apply()`: moves physical page pointers in the originals (Q&A index, the 27번 and 35번 pointers in the slide 2 notes). v10 source ids and correction ids stay keyed to the original (v06) numbers; the builder looks corrections up by `sl["orig"]`.
- `insert()`: places the two slides after the OMH case.

The v07 manifest and `data-` attributes carry `original` (v06 number) or `reference` (A, B). The builder and browser check default to v07; the check also verifies 44 pages, original numbering, reference placement and content, pinned sources in the notes, the skip link landing on 17, and the CEO deep link at its new page. `--version v06` (or v02 to v05) reproduces the preserved exports byte for byte. Sources and the claim-level summary: `docs/references/pstack-superpowers-comparison-v01.md`.

### v06 wording and role clarity

v06 keeps the v05 presentation and design and changes wording only where an expression named the wrong actor or read like implementation jargon. `copy_v06.py` holds the layer, applied after `copy_v04.py` and `copy_v05.py`:
- slide 9 is redrawn: the coordinator either handles the request directly (`직접 처리`, the user's wording) or delegates it to a worker (`워커에게 위임`); the same coordinator, in the same colour and linked by a "같은 코디네이터" line, checks the returned result (`결과 검증 / 코디네이터가 확인`). The viewing screen sits on the worker's task and is not wired to the gateway. The runtime still executes the tools the coordinator picks.
- slide 14 is redrawn as a before and after of one task ("CSV 빈 값 처리 후, 무엇이 바뀌었는지 확인"): both lanes start from OpenCode + OMO with the same model; the after lane adds `data_inspect` and `data_compare`; the modification step is the same in both. Detail and evidence limits are in the notes (`OMH_NOTES`).
- `EDITS`: per-slide before, after and reason for every other screen change.
- `CORRECTIONS`: notes shown before the v10 excerpt on slides 9, 18 and 31.
- `EXCERPT_EDITS`: ordered phrase swaps applied to the v10 excerpts in the notes, published in the manifest as `excerpt_edits` so the check follows the same wording. The source plan is untouched.

`audit_v06.py` writes the per-slide audit (all 42 slides, changed or not) to `docs/production/wording-audit-v06.md` from these tables. The builder and browser check default to v06; `--version v05` (or v02 to v04) reproduces the preserved exports byte for byte. For v06 the check also requires slide 9 to show the coordinator, both routes, the result check and the viewing screen, and fails if "부모" or "도구로 처리" appears on any screen.

### v05 roadmap adjustment

v05 keeps the v04 presentation and removes only the slide 3 break marker, with five evenly spaced roadmap columns. `copy_v05.py` contains this edit. The separate break slide remains. The builder and browser check default to v05; use `--version v04` to reproduce the preserved v04 export.
