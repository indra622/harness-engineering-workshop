# DESIGN.md: Harness Engineering Workshop Deck

Proposed visual system for the 35-slide, 120-minute workshop deck. It follows the production brief (`docs/production/slide-production-brief-v01.md`) and is a draft, not an approved brand. Content comes from `docs/plans/slide-content-plan-v10.md`; when this file and v10 disagree on content, v10 wins. Tokens are stated in prose and implemented in `slides/src/deck/theme.py` and `slides/assets/deck.css`.

The canonical medium is an offline HTML presentation (`slides/index.html`). Each slide is one inline SVG on a 13.333 x 7.5 inch viewBox, so coordinates are inches and type sizes are points (pt / 72 in SVG units). The six PowerPoint proof slides in `slides/previews/` are a legacy experiment that used the same tokens.

## Overview

A calm, flat, projection-first deck for working professionals learning a shared vocabulary. Each slide asks one question, gives one definition or key sentence, and shows one native diagram. Heavy explanation lives in presenter notes. Diagrams are native SVG shapes, text and connectors, never full-slide images or mock product screens. The visual grammar varies by idea: request and result, process loop, scope container, swimlane, before and after, evidence panel, architecture map, mini-diagram tiles.

## Colors

- Canvas `#F7F7F4`: slide background, light neutral.
- Ink `#1F2328`: primary text and default outlines.
- Muted `#5B6470`: secondary text, retained or out-of-scope outlines.
- Primary blue `#2B5FA8`: the current focus, transitions, and what was added.
- Warning amber `#B45309`: the human approval gate, caution, unverified sources.
- Band `#E9ECF1`: question strip and lane backgrounds.
- Focus fill `#E7EEF8`: fill behind primary-outlined shapes.
- Surface `#FFFFFF`: node fill. Hairline `#C5CBD3`: tile outlines.

Color never carries meaning alone. Line pattern and weight repeat each role: solid primary 2.25 pt for focus, solid amber 3 pt for the human gate, dashed muted for retained, out of scope or unverified. Contrast ratios have not been computed, so no accessibility conformance is claimed.

## Typography

- Family: Nanum Gothic (open font) for Latin and Korean, taken from the system with fallbacks Apple SD Gothic Neo, Malgun Gothic, Noto Sans KR. No web font download. Bold for titles, tags and emphasis.
- Title 36 pt bold. Body and key sentence 24 pt (key sentence bold). Diagram labels 20 pt minimum. Meta row and footnote 16 pt.
- All sizes are points (pt), not CSS pixels.
- Labels use explicit line breaks; every line is measured with the real font so no label depends on automatic wrap or breaks mid-token.

## Layout

- 16:9, 13.333 x 7.5 in. Content margins 0.5 in left and right; nothing within 0.4 in of any edge.
- Fixed frame on every slide: meta row (section marker left, source slide ID and time right) at 0.42 in, title at 0.78 in, question strip, key sentence, diagram area, footnote at 6.68 in.
- Diagram area ends by 6.52 in. Aim for at most six labels per screen region and seven nodes per diagram.
- Sample decks keep source slide IDs (for example S11) and never renumber the teaching order.

## Elevation & Depth

Flat. No drop shadows, glows, gradients or inherited theme effects. The builder removes each shape's theme style reference so no renderer can add a shadow. Depth comes from containers and lane bands only.

## Shapes

- Nodes: rounded rectangles with a subtle radius (about 0.09 in). Containers use about 0.12 in.
- Connectors: thin (1.5 pt), glued to shape edges, triangle arrowhead at the end, never drawn through labels. Straight where aligned, orthogonal elbow between swimlanes.
- Shapes do not overlap except for intended containment (nodes inside a container or lane band) and connector endpoints.

## Components

- Question strip: band fill with a 0.08 in primary accent bar; tag "질문" 20 pt bold primary, question 24 pt ink.
- Key sentence line: tag ("정의", "핵심" or "장면") 20 pt bold primary, sentence 24 pt bold ink.
- Node styles: base (white, ink 1.25 pt), focus (focus fill, primary 2.25 pt), gate (white, amber 3 pt, bold), retained (dashed muted 2.25 pt), out of scope (no fill, dashed muted, muted text), chip (band fill, no line), note (dashed muted hairline), caution (white, dashed amber 2.25 pt, amber bold text), tile (white, hairline).
- Lane band: band fill, label column at left; the lane being taught gets focus fill and a primary outline.
- Decision diamond: a gate-styled diamond for a human decision, with yes and no branches labelled.
- Page chrome (HTML only): surround `#DCE0E5`, a 60 px control bar with previous and next buttons (44 px minimum targets), a progress bar in primary blue, a slide counter and title, and a notes toggle. Presenter notes open in a side panel, or below the slide on narrow screens. Print hides the chrome and prints one 16:9 page per slide.

## Do's and Don'ts

- Do keep one question, one key sentence and one diagram per slide; put details, caveats and backup examples in notes.
- Do label hypothetical examples and unverified sources on the slide itself.
- Do vary diagram types; do not repeat one card grid across slides.
- Don't use bullet walls, stock AI imagery, icon walls, ornamental gradient cards or fake internal screens.
- Don't shrink fonts below the floors to fit text; shorten the label or move detail to notes.
- Don't imply automatic publication, skipped human approval, independent multi-agent review or model training where the source does not support it.
