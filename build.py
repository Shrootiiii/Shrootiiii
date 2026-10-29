"""Generates the profile's SVG artwork in light and dark variants.

GitHub serves README images without access to web fonts, so every SVG
uses system font stacks. Run: python3 build.py
"""
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
# Handwriting for the whimsical notes: macOS, then Windows, then whatever cursive exists.
HAND = "'Bradley Hand', Noteworthy, 'Segoe Print', 'Ink Free', 'Comic Sans MS', cursive"

# Every animated SVG carries this, so visitors who ask for less motion get the still frame.
CALM = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def sparkle(x, y, r, color, delay, cls="twinkle"):
    # Four-point star centred on (x, y).
    k = r * 0.28
    d = f"M{x} {y - r} Q{x + k} {y - k} {x + r} {y} Q{x + k} {y + k} {x} {y + r} Q{x - k} {y + k} {x - r} {y} Q{x - k} {y - k} {x} {y - r}Z"
    return f'<path class="{cls}" style="animation-delay:{delay}s" d="{d}" fill="{color}"/>'

THEMES = {
    "light": dict(bg="#F5F3EF", ink="#0E0F13", muted="#6E6C66", faint="#D9D6CE", line="#E6E3DB", accent="#4D6B34", accent_ink="#FFFFFF", hl="#4D6B34", tint="#8EC16A", tint_op="0.38"),
    "dark":  dict(bg="#0E0F13", ink="#F2F1EC", muted="#8C8A84", faint="#2A2A2E", line="#1F1F23", accent="#8EC16A", accent_ink="#0E0F13", hl="#8EC16A", tint="#8EC16A", tint_op="0.2"),
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
    .wash {{ animation: pop .6s ease-out 1s backwards; }}
    .handles, .tag {{ animation: pop .4s ease-out 1.3s backwards; }}
    .cursor {{ animation: nudge 1s cubic-bezier(.2,.7,.2,1) .1s backwards; }}
    .caret {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes twinkle {{ 0%, 100% {{ transform: scale(1) rotate(0deg); opacity: 1; }} 50% {{ transform: scale(.45) rotate(45deg); opacity: .5; }} }}
    @keyframes bob {{ 50% {{ transform: translate(-5px, -4px); }} }}
    @keyframes scribble {{ from {{ stroke-dashoffset: 700; }} }}
    .twinkle {{ transform-box: fill-box; transform-origin: center; animation: twinkle 2.6s ease-in-out infinite; }}
    .cursor {{ animation: nudge 1s cubic-bezier(.2,.7,.2,1) .1s backwards, bob 3.2s ease-in-out 1.2s infinite; }}
    .arrow {{ stroke-dasharray: 700; animation: scribble 1.2s ease-out 1.7s backwards; }}
    .note {{ animation: pop .5s ease-out 2.4s backwards; }}
    {CALM}
  </style>
  <rect width="{w}" height="{h}" rx="20" fill="{c["bg"]}"/>
  {dot_grid(w, h, 24, c["faint"], "g")}

  <text x="72" y="84" class="mono" font-size="17" letter-spacing="3" fill="{c["muted"]}">SHRUTI SHANKAR NARAYANAN</text>
  <line x1="72" y1="106" x2="152" y2="106" stroke="{c["ink"]}" stroke-width="2"/>

  <text x="64" y="204" class="sans" font-size="120" font-weight="600" letter-spacing="-5" fill="{c["ink"]}">I build what</text>
  <text x="64" y="{dy}" class="sans" font-size="120" font-weight="600" fill="{c["ink"]}">I</text>
  <rect class="wash" x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{c["tint"]}" fill-opacity="{c["tint_op"]}"/>
  <text x="{dx}" y="{dy}" class="sans" font-size="120" font-weight="600" textLength="{dw}" lengthAdjust="spacingAndGlyphs" fill="{c["hl"]}">design</text>
  <text x="{bx + bw + 8}" y="{dy}" class="sans" font-size="120" font-weight="600" fill="{c["ink"]}">.</text>

  <rect class="box" x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="{c["accent"]}" stroke-width="2"/>
  <g class="handles">{handles}</g>
  <g class="tag">
    <rect x="{bx + bw / 2 - 52}" y="{by + bh + 14}" width="104" height="26" rx="4" fill="{c["accent"]}"/>
    <text x="{bx + bw / 2}" y="{by + bh + 32}" text-anchor="middle" class="mono" font-size="13" fill="{c["accent_ink"]}">{bw} × {bh}</text>
  </g>
  {sparkle(668, 118, 14, c["accent"], 0)}
  {sparkle(bx + bw + 44, by - 4, 7, c["ink"], .9)}
  {sparkle(bx - 22, by + bh + 22, 9, c["accent"], 1.6)}

  <!-- A margin note, as if scribbled on the canvas -->
  <path class="arrow" d="M 800 232 C 780 300, 700 318, 676 280 C 656 248, 708 236, 712 272 C 716 312, 620 316, 520 268" fill="none" stroke="{c["muted"]}" stroke-width="2.5" stroke-linecap="round"/>
  <path class="arrow" d="M 534 290 L 516 266 L 544 258" fill="none" stroke="{c["muted"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <text class="note" x="790" y="214" font-family="{HAND}" font-size="34" fill="{c["accent"]}" transform="rotate(-5 790 214)">the fun part!</text>

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
    <path class="beat" d="M48 30h24v18h18v24H72v18H48V72H30V48h18z" fill="{c["accent"]}"/>"""


def motif_sush(c):
    # Two people in one live session: overlapping avatars and a live dot.
    return f"""<rect x="8" y="18" width="104" height="84" rx="14" fill="none" stroke="{c["faint"]}" stroke-width="2"/>
    <circle cx="48" cy="62" r="20" fill="{c["accent"]}"/>
    <circle cx="74" cy="62" r="20" fill="{c["ink"]}" stroke="{c["bg"]}" stroke-width="4"/>
    <text x="48" y="69" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="600" fill="{c["accent_ink"]}">S</text>
    <text x="74" y="69" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="600" fill="{c["bg"]}">S</text>
    <circle class="ping" cx="96" cy="32" r="5" fill="none" stroke="{c["accent"]}" stroke-width="2"/>
    <circle cx="96" cy="32" r="5" fill="{c["accent"]}"/>"""


def motif_color(c):
    swatches = ["#FF5A4E", "#FFB23F", c["accent"], "#3D9BFF", "#A78BFA"]
    return "".join(
        f'<rect class="wave" style="animation-delay:{i * .14:.2f}s" x="{6 + i * 22}" y="{20 + (i % 2) * 14}" width="20" height="66" rx="10" fill="{s}"/>'
        for i, s in enumerate(swatches)
    )


def motif_ui(c):
    return f"""<rect x="8" y="22" width="104" height="76" rx="12" fill="none" stroke="{c["faint"]}" stroke-width="2"/>
    <rect x="22" y="38" width="50" height="10" rx="5" fill="{c["ink"]}"/>
    <rect x="22" y="56" width="76" height="8" rx="4" fill="{c["faint"]}"/>
    <rect class="press" x="22" y="74" width="34" height="14" rx="7" fill="{c["accent"]}"/>"""


PROJECTS = [
    ("sush", "01", "Sush", "A desktop AI agent your team can run together, live and end-to-end encrypted", "sush-website-ten.vercel.app", motif_sush),
    ("ui", "02", "ui", "Open-source React + Tailwind components, shadcn-compatible", "npx shadcn add @ui-shrushank/…", motif_ui),
    ("mediclear", "03", "MediClear", "An outpatient app for clinics and their patients", "medi-clear-app.vercel.app", motif_medi),
    ("color", "04", "Color Picker", "A colour tool for building palettes", "color-picker-seven-rust.vercel.app", motif_color),
]


def project(t, c, key, num, title, desc, url, motif):
    # The card is 168 tall; the extra 16 is transparent spacing, since GitHub
    # stacks README images with no gap.
    w, h = 1200, 184
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}: {desc}">
  <style>
    .beat, .ping, .wave, .press {{ transform-box: fill-box; transform-origin: center; }}
    @keyframes beat {{ 0%, 40%, 100% {{ transform: scale(1); }} 10%, 28% {{ transform: scale(1.12); }} }}
    @keyframes ping {{ to {{ transform: scale(2.8); opacity: 0; }} }}
    @keyframes wave {{ 50% {{ transform: translateY(-7px); }} }}
    @keyframes press {{ 0%, 70%, 100% {{ transform: scale(1); }} 80% {{ transform: scale(.88); }} }}
    .beat {{ animation: beat 2.4s ease-in-out infinite; }}
    .ping {{ animation: ping 1.8s ease-out infinite; }}
    .wave {{ animation: wave 2.2s ease-in-out infinite; }}
    .press {{ animation: press 3s ease-in-out infinite; }}
    {CALM}
  </style>
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


def signoff(t, c):
    w, h = 1200, 120
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Thanks for scrolling this far.">
  <style>
    .twinkle {{ transform-box: fill-box; transform-origin: center; animation: twinkle 2.6s ease-in-out infinite; }}
    @keyframes twinkle {{ 50% {{ transform: scale(.45) rotate(45deg); opacity: .5; }} }}
    {CALM}
  </style>
  <path d="M 420 92 q 20 -14 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0" fill="none" stroke="{c["accent"]}" stroke-width="2.5" stroke-linecap="round"/>
  <text x="{w / 2}" y="62" text-anchor="middle" font-family="{HAND}" font-size="34" fill="{c["muted"]}">thanks for scrolling this far</text>
  {sparkle(w / 2 + 250, 40, 11, c["accent"], 0)}
  {sparkle(w / 2 - 250, 52, 8, c["accent"], 1.1)}
</svg>"""
    write("signoff", t, svg)


for t, c in THEMES.items():
    header(t, c)
    section(t, c, "work", "Selected work")
    section(t, c, "tools", "Tools I reach for")
    for p in PROJECTS:
        project(t, c, *p)
    tools(t, c)
    signoff(t, c)

print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")
