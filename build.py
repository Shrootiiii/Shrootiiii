"""Generates the profile's SVG artwork in light and dark variants.

GitHub serves README images without access to web fonts, so every SVG
uses system font stacks. Run: python3 build.py
"""
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "light": dict(bg="#F7F6F2", ink="#16161A", muted="#6E6C66", faint="#D9D6CE", line="#E6E3DB", accent="#15803D", accent_ink="#FFFFFF"),
    "dark":  dict(bg="#0E0E10", ink="#F2F1EC", muted="#8C8A84", faint="#2A2A2E", line="#1F1F23", accent="#4ADE80", accent_ink="#0E0E10"),
}


def write(name, theme, svg):
    (OUT / f"{name}-{theme}.svg").write_text(svg.strip() + "\n")


def dot_grid(w, h, step, color, fade_id):
    return f"""
  <defs>
    <pattern id="dots" width="{step}" height="{step}" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.5" fill="{color}"/>
    </pattern>
    <radialGradient id="{fade_id}" cx="78%" cy="40%" r="70%">
      <stop offset="0" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <mask id="fade"><rect width="{w}" height="{h}" fill="url(#{fade_id})"/></mask>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#dots)" mask="url(#fade)"/>"""


def header(t, c):
    w, h = 1200, 470
    # "design" is pinned to a fixed width with textLength, so the selection box
    # fits it exactly whichever system font renders it.
    dx, dy, dw = 116, 318, 322
    bx, by, bw, bh = dx - 10, dy - 92, dw + 20, 116
    handles = "".join(
        f'<rect x="{x - 6}" y="{y - 6}" width="12" height="12" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2"/>'
        for x, y in [(bx, by), (bx + bw, by), (bx, by + bh), (bx + bw, by + bh)]
    )
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Shruti Shankar Narayanan. I build what I design. Product designer who codes.">
  <style>
    .sans {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; }}
    @keyframes draw {{ from {{ stroke-dashoffset: 940; }} }}
    @keyframes pop {{ from {{ opacity: 0; transform: translateY(4px); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes nudge {{ from {{ opacity: 0; transform: translate(70px, 50px); }} }}
    /* fill-mode backwards: if a renderer skips animation, everything still shows */
    .box {{ stroke-dasharray: 940; animation: draw 1.1s cubic-bezier(.2,.7,.2,1) .4s backwards; }}
    .handles, .tag {{ animation: pop .4s ease-out 1.3s backwards; }}
    .cursor {{ animation: nudge 1s cubic-bezier(.2,.7,.2,1) .1s backwards; }}
    .caret {{ animation: blink 1.1s steps(1) infinite; }}
  </style>
  <rect width="{w}" height="{h}" rx="20" fill="{c["bg"]}"/>
  {dot_grid(w, h, 24, c["faint"], "g")}

  <text x="72" y="84" class="mono" font-size="17" letter-spacing="3" fill="{c["muted"]}">SHRUTI SHANKAR NARAYANAN</text>
  <line x1="72" y1="106" x2="152" y2="106" stroke="{c["ink"]}" stroke-width="2"/>

  <text x="64" y="204" class="sans" font-size="120" font-weight="600" letter-spacing="-5" fill="{c["ink"]}">I build what</text>
  <text x="64" y="{dy}" class="sans" font-size="120" font-weight="600" fill="{c["ink"]}">I</text>
  <text x="{dx}" y="{dy}" class="sans" font-size="120" font-weight="600" textLength="{dw}" lengthAdjust="spacingAndGlyphs" fill="{c["accent"]}">design</text>
  <text x="{bx + bw + 8}" y="{dy}" class="sans" font-size="120" font-weight="600" fill="{c["ink"]}">.</text>

  <rect class="box" x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="{c["accent"]}" stroke-width="2"/>
  <g class="handles">{handles}</g>
  <g class="tag">
    <rect x="{bx + bw / 2 - 52}" y="{by + bh + 14}" width="104" height="26" rx="4" fill="{c["accent"]}"/>
    <text x="{bx + bw / 2}" y="{by + bh + 32}" text-anchor="middle" class="mono" font-size="13" fill="{c["accent_ink"]}">{bw} × {bh}</text>
  </g>
  <g class="cursor">
    <path d="M {bx + bw + 56} {by + bh - 6} l 0 34 l 9 -9 l 7 15 l 7 -3 l -7 -15 l 13 0 z" fill="{c["ink"]}" stroke="{c["bg"]}" stroke-width="2" stroke-linejoin="round"/>
  </g>

  <text x="72" y="418" class="mono" font-size="18" fill="{c["muted"]}">Product designer who codes<tspan class="caret" fill="{c["accent"]}"> ▍</tspan></text>
  <text x="{w - 72}" y="418" text-anchor="end" class="mono" font-size="18" fill="{c["muted"]}">shrutishankarnarayanan.com ↗</text>
</svg>"""
    write("header", t, svg)


def section(t, c, name, label):
    w, h = 1200, 64
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
  <text x="4" y="40" font-family="{MONO}" font-size="20" letter-spacing="3" fill="{c["muted"]}">{label.upper()}</text>
  <line x1="{4 + len(label) * 15.5 + 24}" y1="33" x2="{w - 4}" y2="33" stroke="{c["faint"]}" stroke-width="1.5"/>
</svg>"""
    write(f"section-{name}", t, svg)


# Small abstract motifs, one per project, drawn in a 120×120 box.
def motif_medi(c):
    return f"""<rect x="10" y="10" width="100" height="100" rx="28" fill="none" stroke="{c["faint"]}" stroke-width="2"/>
    <path d="M48 30h24v18h18v24H72v18H48V72H30V48h18z" fill="{c["accent"]}"/>"""


def motif_planet(c):
    return f"""<ellipse cx="60" cy="60" rx="56" ry="18" fill="none" stroke="{c["faint"]}" stroke-width="2" transform="rotate(-18 60 60)"/>
    <circle cx="60" cy="60" r="28" fill="{c["accent"]}"/>
    <path d="M10 76 A 56 18 -18 0 0 110 44" fill="none" stroke="{c["ink"]}" stroke-width="2" transform="rotate(0)"/>
    <circle cx="104" cy="34" r="6" fill="{c["ink"]}"/>"""


def motif_color(c):
    swatches = ["#FF5A4E", "#FFB23F", c["accent"], "#3D9BFF", "#A78BFA"]
    return "".join(
        f'<rect x="{6 + i * 22}" y="{20 + (i % 2) * 14}" width="20" height="66" rx="10" fill="{s}"/>'
        for i, s in enumerate(swatches)
    )


def motif_ui(c):
    return f"""<rect x="8" y="22" width="104" height="76" rx="12" fill="none" stroke="{c["faint"]}" stroke-width="2"/>
    <rect x="22" y="38" width="50" height="10" rx="5" fill="{c["ink"]}"/>
    <rect x="22" y="56" width="76" height="8" rx="4" fill="{c["faint"]}"/>
    <rect x="22" y="74" width="34" height="14" rx="7" fill="{c["accent"]}"/>"""


PROJECTS = [
    ("ui", "01", "ui", "Open-source React + Tailwind components, shadcn-compatible", "npx shadcn add @ui-shrushank/…", motif_ui),
    ("mediclear", "02", "MediClear", "An outpatient app for clinics and their patients", "medi-clear-app.vercel.app", motif_medi),
    ("planet", "03", "Planet Explorer", "An interactive tour of the solar system", "planet-explorer-xi.vercel.app", motif_planet),
    ("color", "04", "Color Picker", "A colour tool for building palettes", "color-picker-seven-rust.vercel.app", motif_color),
]


def project(t, c, key, num, title, desc, url, motif):
    # The card is 168 tall; the extra 16 is transparent spacing, since GitHub
    # stacks README images with no gap.
    w, h = 1200, 184
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}: {desc}">
  <rect x="1" y="1" width="{w - 2}" height="166" rx="18" fill="{c["bg"]}" stroke="{c["line"]}" stroke-width="2"/>
  <text x="40" y="62" font-family="{MONO}" font-size="18" fill="{c["muted"]}">{num}</text>
  <text x="104" y="68" font-family="{SANS}" font-size="40" font-weight="600" letter-spacing="-1.2" fill="{c["ink"]}">{title}</text>
  <text x="104" y="108" font-family="{SANS}" font-size="22" fill="{c["muted"]}">{desc}</text>
  <text x="104" y="140" font-family="{MONO}" font-size="16" fill="{c["accent"]}">{url}  ↗</text>
  <g transform="translate({w - 184} 24)">{motif(c)}</g>
</svg>"""
    write(f"project-{key}", t, svg)


TOOLS = ["TypeScript", "React", "Next.js", "Tailwind", "shadcn/ui", "Rust", "Tauri", "Figma"]


def tools(t, c):
    w, h = 1200, 64
    x, chips = 4, []
    for name in TOOLS:
        cw = len(name) * 12.2 + 40
        chips.append(
            f'<rect x="{x}" y="8" width="{cw:.0f}" height="48" rx="24" fill="none" stroke="{c["faint"]}" stroke-width="2"/>'
            f'<text x="{x + cw / 2:.0f}" y="39" text-anchor="middle" font-family="{SANS}" font-size="20" fill="{c["ink"]}">{name}</text>'
        )
        x += cw + 12
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Tools: {", ".join(TOOLS)}">
  {"".join(chips)}
</svg>"""
    write("tools", t, svg)


for t, c in THEMES.items():
    header(t, c)
    section(t, c, "work", "Selected work")
    section(t, c, "tools", "Tools I reach for")
    for p in PROJECTS:
        project(t, c, *p)
    tools(t, c)

print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")
