# Profile README — Design Notes

Last updated: 2026-10-29

## What changed

### 2026-10-29 (whimsy)
- Header: a handwritten "the fun part!" note with a looping arrow that draws itself toward "design", three twinkling sparkles, and a cursor that idles with a slow bob (`build.py` `header`, `sparkle`).
- Project motifs animate gently: Sush's live dot pings, the ui button presses, the MediClear cross beats like a pulse, and the Color Picker swatches move in a wave (`project` styles, motif classes).
- New sign-off at the bottom: "thanks for scrolling this far" in handwriting over a moss squiggle (`signoff`, `README.md`).
- Every animated SVG honours `prefers-reduced-motion` (`CALM`).

### 2026-10-29 (Sush)
- Sush added as project 01, linking to sush-website-ten.vercel.app, with a motif of two overlapping avatars and a live dot (`motif_sush`). Planet Explorer removed from `PROJECTS`, `README.md` and `assets/`.
- `hl` now equals the portfolio's moss tokens (`#4D6B34` light, `#8EC16A` dark). Every green on the profile is one of those two values.

### 2026-10-29 (highlight)
- The header's selection box gets a moss-light wash (`tint`, 38% light / 20% dark) that fades in after the box draws, and "design" uses a brighter green (`hl`: `#3F6B1F` light, `#A8DD7C` dark) so it reads against the wash (`build.py` `header`). Plain moss text alone was too muted to read as the focal word.

### 2026-10-29 (portfolio palette)
- Accent set to the portfolio's moss tokens: `#4D6B34` light, `#8EC16A` dark. Background and ink switched to the portfolio's ivory `#F5F3EF` and ink `#0E0F13` (`build.py` `THEMES`), so the profile and the site share one palette.

### 2026-10-29 (accent)
- Accent changed from indigo to green: `#15803D` light, `#4ADE80` dark (`build.py` `THEMES`). The Color Picker motif swaps its green swatch for purple so the accent is not repeated.

### 2026-10-29
- Replaced the plain Markdown README with generated SVG artwork: header banner, section labels, four project cards and a tools strip (`README.md`, `assets/`).
- Added `build.py`, which writes every SVG in a light and a dark variant from one set of theme tokens (`THEMES`).
- The header draws a design-tool selection box, resize handles, a size tag and a cursor around the word "design", animated in on load.
- Each image sits in a `<picture>` element with a `prefers-color-scheme: dark` source, and each card links to its repo or live site.

## Why

GitHub READMEs accept no CSS and load no web fonts, so typographic control is only possible inside images. Generating the SVGs from a script keeps the two themes in sync and makes text edits a one-line change, at the cost of the copy no longer being editable as Markdown.

The selection box only works if it fits the word exactly, but system fonts differ in width across macOS, Windows and Linux. "design" is therefore pinned with `textLength`, which trades a slight glyph stretch on some systems for a box that always lines up.

Animations use `animation-fill-mode: backwards` so the final frame is the element's default state. A renderer that skips CSS animation still shows the complete header.

GitHub stacks README images with no gap, so each project card carries 16px of transparent space at its bottom instead of relying on Markdown spacing.

The whimsy pass keeps to the existing palette and borrows from the portfolio's handwritten accent (Caveat). Web fonts cannot load in README images, so the notes use a system handwriting stack (Bradley Hand on macOS, Segoe Print or Ink Free on Windows, generic cursive elsewhere); the exact face varies by platform, which suits a scribble. Motion is slow and small so the page stays calm, and reduced-motion visitors get the still frame.

## What makes it stand out

- Light and dark artwork follows the visitor's GitHub theme through `<picture>`, unlike single-image banners that clash with one of the themes.
- System font stacks only, so nothing depends on external font loading, which GitHub's image proxy blocks.
- Every SVG has `role="img"` and an `aria-label`, and every `<img>` has alt text, so screen readers get the full content.
- Avoids third-party stats widgets and badge services: no runtime dependencies or rate limits, and nothing that can break.
- `python3 build.py` regenerates all 16 files from one script.
