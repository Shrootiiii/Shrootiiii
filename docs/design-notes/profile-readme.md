# Profile README — Design Notes

Last updated: 2026-10-29

## What changed

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

## What makes it stand out

- Light and dark artwork follows the visitor's GitHub theme through `<picture>`, unlike single-image banners that clash with one of the themes.
- System font stacks only, so nothing depends on external font loading, which GitHub's image proxy blocks.
- Every SVG has `role="img"` and an `aria-label`, and every `<img>` has alt text, so screen readers get the full content.
- Avoids third-party stats widgets and badge services: no runtime dependencies or rate limits, and nothing that can break.
- `python3 build.py` regenerates all 16 files from one script.
