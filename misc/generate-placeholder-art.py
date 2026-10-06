#!/usr/bin/env python3
"""
Generate placeholder art for every James Street Tavern menu item.

Each item's art is built from one shared shell (wood ground, §5 warm overlay,
vignette, chalk label) plus a dish archetype function. Archetypes take the
item's own colours so related dishes read as a family without being clones.

Per DESIGN.md:
  - built from the --wood-gradient stops #5c3a21 -> #3a2415 -> #2c1b10
  - 1600x1000 (16:10) rendered to PNG so object-fit: cover never crops badly
  - filenames are photo-<slug>-hero.png so photoGlob resolves them from the
    page bundle with no template change; dropping in real photography with
    the same name wins automatically

Usage:  python3 misc/generate-placeholder-art.py [--svg-only] [--only <slug>]
Output: content/<section>/<slug>/photo-<slug>-hero.png

Item art is shipped as PNG only. The source SVG is rasterised through a temp
file and deleted, because a leftover .svg in a page bundle shadows the PNG
under photoGlob and would silently serve vector art instead of the raster.

The eight section placeholders (content/<section>/photo-<section>-hero.svg)
are a separate, tracked set of vector assets and are NOT touched by this
script — DESIGN.md §5 specifies those as SVG.

Rasterising bakes the chalk label into pixels, so Oswald and Permanent Marker
must be installed locally or the label degrades to a fallback sans with no
warning. Install them once per machine before regenerating:

    # any source of the two woff2 files will do, e.g. fonts.google.com
    cp <oswald>.woff2 <permanent-marker>.woff2 ~/.local/share/fonts/
    fc-cache -f
    fc-match "Permanent Marker"   # must report PermanentMarker, not DejaVu
"""

import argparse
import html
import os
import re
import sys
import tempfile

import cairosvg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")

W, H = 1200, 750          # viewBox; 16:10
OUT_W, OUT_H = 1600, 1000  # raster size per DESIGN.md §5

# --------------------------------------------------------------------------
# shell
# --------------------------------------------------------------------------

def shell(title, body, defs_extra=""):
    """Wood ground + grain + dish art + chalk label + warm overlay + vignette.

    Labels are kept inside the middle 1000px of the 1200px canvas because
    .detail-media crops the 16:10 art to 4:3, losing ~100px off each side.
    """
    d = f"""{defs_extra}
    <radialGradient id="plate" cx="0.5" cy="0.4" r="0.7">
      <stop offset="0" stop-color="#f5f0e6"/>
      <stop offset="1" stop-color="#cfc3b1"/>
    </radialGradient>
    <linearGradient id="wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5c3a21"/>
      <stop offset="0.55" stop-color="#3a2415"/>
      <stop offset="1" stop-color="#2c1b10"/>
    </linearGradient>
    <radialGradient id="warm" cx="0.5" cy="0.42" r="0.72">
      <stop offset="0" stop-color="#a9703d" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#5c3a21" stop-opacity="0.2"/>
    </radialGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}"/></clipPath>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Placeholder illustration: {html.escape(title.lower())}">
  <defs>{d}
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#wood)"/>
    <rect width="{W}" height="{H}" fill="url(#warm)"/>
    <g fill="none" stroke="#3d2412" stroke-opacity="0.22" stroke-width="3">
      <path d="M-40 120 C 260 92, 520 148, 1240 108"/>
      <path d="M-40 268 C 300 300, 700 232, 1240 272"/>
      <path d="M-40 430 C 340 396, 760 470, 1240 424"/>
      <path d="M-40 596 C 300 640, 720 570, 1240 610"/>
      <path d="M-40 700 C 380 676, 800 726, 1240 690"/>
    </g>
    <g fill="none" stroke="#8d6039" stroke-opacity="0.2" stroke-width="2">
      <path d="M-40 190 C 300 160, 700 214, 1240 176"/>
      <path d="M-40 512 C 320 480, 760 548, 1240 504"/>
    </g>
{body}
    <g text-anchor="middle" font-family="Permanent Marker, Comic Sans MS, cursive" fill="#e8c547">
      <text x="600" y="122" font-size="42" letter-spacing="2">{html.escape(title)}</text>
    </g>
    <g text-anchor="middle" font-family="Oswald, Impact, sans-serif" fill="#c2ab8d">
      <text x="600" y="706" font-size="28" letter-spacing="10">PHOTO PLACEHOLDER</text>
    </g>
    <rect width="{W}" height="{H}" fill="#5c3a21" opacity="0.12"/>
    <rect width="{W}" height="{H}" fill="none" stroke="#000" stroke-opacity="0.45" stroke-width="150"/>
  </g>
</svg>"""


def label_size(title):
    """Shrink long dish names so they stay inside the 1000px safe band."""
    n = len(title)
    for size, spacing in ((42, 2), (38, 2), (34, 1), (30, 1), (27, 0)):
        if n * (size * 0.6 + spacing) <= 880:
            return size, spacing
    return 24, 0


# --------------------------------------------------------------------------
# reusable props
# --------------------------------------------------------------------------

def plate(cx=600, cy=420, rx=360, ry=330, inner=0.87):
    """The ceramic platter every plated dish sits on."""
    return f"""    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#plate)"/>
    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#8d6039" stroke-opacity="0.35" stroke-width="4"/>
    <ellipse cx="{cx}" cy="{cy + 8}" rx="{int(rx * inner)}" ry="{int(ry * inner)}" fill="#efe7d8"/>"""


def board(cx=600, cy=430, rx=380, ry=150):
    """Wooden serving board — used for baskets and sandwiches."""
    return f"""    <ellipse cx="{cx}" cy="{cy + 12}" rx="{rx}" ry="{ry}" fill="#000" opacity="0.2"/>
    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#a9793f"/>
    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#7a4e2c" stroke-opacity="0.6" stroke-width="5"/>
    <ellipse cx="{cx}" cy="{cy + 4}" rx="{int(rx * 0.93)}" ry="{int(ry * 0.9)}" fill="#bb8a4d"/>"""


def dip(cx, cy, r=52, top="#c4483c", deep="#8b2e2e", rim="#f2ece0"):
    """Sauce cup seen at a slight angle."""
    return f"""    <g transform="translate({cx} {cy})">
      <ellipse cx="0" cy="{int(r * 0.62)}" rx="{int(r * 1.1)}" ry="{int(r * 0.3)}" fill="#000" opacity="0.2"/>
      <ellipse cx="0" cy="0" rx="{r}" ry="{int(r * 0.94)}" fill="{rim}"/>
      <ellipse cx="0" cy="0" rx="{int(r * 0.82)}" ry="{int(r * 0.76)}" fill="{top}"/>
      <ellipse cx="{int(-r * 0.24)}" cy="{int(-r * 0.26)}" rx="{int(r * 0.26)}" ry="{int(r * 0.16)}" fill="#fff" opacity="0.28"/>
    </g>"""


def fry(w, h, c):
    """One seasoned fry, centred on its own origin."""
    w2 = int(w / 2)
    h2 = int(h / 2)
    return (f'<rect x="{-w2}" y="{-h2}" width="{int(w)}" height="{int(h)}" rx="{w2}" fill="{c}"/>'
            f'<rect x="{-w2}" y="{-h2}" width="{int(w)}" height="{int(h * 0.34)}" '
            f'rx="{w2}" fill="#f0cd8d" opacity="0.55"/>')


def fries(cx=600, cy=430, n=13, seed=1, c="#e0a94a", spread=300, h=70):
    """Scattered seasoned fries."""
    out = []
    for i in range(n):
        # deterministic pseudo-random placement
        import math
        a = (i * 137.5 + seed * 41) % 360
        rad = ((i * 53 + seed * 29) % 100) / 100.0
        x = cx + math.cos(math.radians(a)) * spread * rad
        y = cy + math.sin(math.radians(a)) * 92 * rad
        rot = ((i * 47 + seed * 13) % 70) - 35
        hh = h + ((i * 17) % 26)
        ww = 21 + ((i * 11) % 9)
        out.append(
            f'    <g transform="translate({int(x)} {int(y)}) rotate({rot})">'
            f'{fry(ww * 2, hh, c)}</g>')
    return "\n".join(out)


def crumb(cx, cy, rx, ry, n=26, c="#a8701f", seed=3):
    """Breadcrumb speckles over a fried surface."""
    out = []
    for i in range(n):
        a = (i * 137.5 + seed * 17) % 360
        rad = (((i * 41 + seed * 23) % 97) / 97.0)
        import math
        x = cx + math.cos(math.radians(a)) * rx * rad
        y = cy + math.sin(math.radians(a)) * ry * rad
        r = 3 + (i % 4)
        out.append(f'    <circle cx="{int(x)}" cy="{int(y)}" r="{r}" fill="{c}" opacity="0.4"/>')
    return "\n".join(out)


def leaf(x, y, s=1.0, rot=0, c="#4a7a34"):
    return (f'    <g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<path d="M0 0 C 26 -20, 62 -16, 78 4 C 58 24, 24 22, 0 0 Z" fill="{c}"/>'
            f'<path d="M6 1 C 30 -8, 56 -6, 72 4" fill="none" stroke="#2f5220" stroke-opacity="0.55" stroke-width="3"/></g>')


def pickle_speck(c="#e0b83a"):
    return f'    <circle cx="0" cy="0" r="7" fill="{c}" opacity="0.5"/>'


# --------------------------------------------------------------------------
# dish archetypes
# --------------------------------------------------------------------------

def a_provolone(t, d, c):
    """Garlic Breaded Provolone Sticks — golden sticks with marinara."""
    sticks = []
    for rot, dx, dy, w in ((-13, -150, -34, 300), (-4, -130, 26, 288), (7, -146, 88, 272)):
        sticks.append(f"""    <g transform="rotate({rot}) translate({dx} {dy})">
      <rect x="-150" y="-30" width="{w}" height="60" rx="30" fill="#c78a30"/>
      <rect x="-150" y="-31" width="{w}" height="54" rx="27" fill="{c}"/>
      <ellipse cx="{w - 150}" cy="-4" rx="15" ry="27" fill="#f7e3ad"/>
      <ellipse cx="{w - 168}" cy="-4" rx="6" ry="14" fill="#fdf3d6" opacity="0.75"/></g>""")
    return shell(t, f"""    <ellipse cx="600" cy="486" rx="392" ry="126" fill="url(#plate)"/>
    <ellipse cx="600" cy="486" rx="392" ry="126" fill="none" stroke="#8d6039" stroke-opacity="0.35" stroke-width="4"/>
    <ellipse cx="600" cy="492" rx="330" ry="102" fill="#efe7d8"/>
    <g transform="translate(600 462)">
{chr(10).join(sticks)}
      <g fill="#a8701f" opacity="0.45">
        <circle cx="-120" cy="-52" r="5"/><circle cx="-52" cy="-58" r="4"/>
        <circle cx="18" cy="-50" r="5"/><circle cx="86" cy="-56" r="4"/>
        <circle cx="-96" cy="8" r="5"/><circle cx="-24" cy="2" r="4"/>
        <circle cx="46" cy="10" r="5"/><circle cx="108" cy="0" r="4"/></g>
    </g>
{dip(322, 520, 60, '#c4483c', '#8b2e2e')}""")


def a_hushpuppies(t, d, c):
    """Basket of Hushpuppies — squat golden nuggets, heaped."""
    import math
    nuggets = []
    for i in range(16):
        a = (i * 137.5 + 20) % 360
        rad = ((i * 47 + 13) % 96) / 96.0
        x = 600 + math.cos(math.radians(a)) * 250 * rad
        y = 430 + math.sin(math.radians(a)) * 150 * rad
        rx = 40 + (i % 4) * 7
        ry = 32 + (i % 3) * 6
        rot = ((i * 31 + 7) % 60) - 30
        nuggets.append(
            f'    <g transform="translate({int(x)} {int(y)}) rotate({rot})">'
            f'<ellipse cx="0" cy="8" rx="{rx}" ry="{ry}" fill="#c78a30"/>'
            f'<ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="{c}"/>'
            f'<ellipse cx="{int(-rx * 0.25)}" cy="{int(-ry * 0.3)}" rx="{int(rx * 0.4)}" ry="{int(ry * 0.3)}" fill="#f7e3ad" opacity="0.5"/></g>')
    return shell(t, f"""{board(600, 440, 330, 150)}
{chr(10).join(nuggets)}
{dip(880, 470, 54, '#c4483c', '#8b2e2e')}
    <g text-anchor="middle" font-family="Oswald, Impact, sans-serif" fill="#c2ab8d" font-size="24" letter-spacing="3" opacity="0.9">
      <text x="600" y="614">{html.escape(d)}</text>
    </g>""")


def a_onion_rings(t, d, c):
    """Beer Battered Onion Rings — battered rings, some leaning."""
    rings = []
    for i, (x, y, rx, rot) in enumerate([
            (470, 420, 92, -12), (620, 396, 100, 6), (760, 424, 88, 18),
            (556, 480, 84, 8), (700, 492, 80, -16), (380, 470, 66, -22)]):
        rings.append(f"""    <g transform="translate({x} {y}) rotate({rot})">
      <ellipse cx="0" cy="12" rx="{rx}" ry="{int(rx * 0.9)}" fill="#c9902f"/>
      <ellipse cx="0" cy="0" rx="{rx}" ry="{int(rx * 0.9)}" fill="{c}"/>
      <ellipse cx="0" cy="0" rx="{int(rx * 0.44)}" ry="{int(rx * 0.4)}" fill="#8d6039"/>
      <ellipse cx="0" cy="0" rx="{int(rx * 0.3)}" ry="{int(rx * 0.27)}" fill="#6b4325"/>
      <path d="M {-int(rx * 0.7)} {-int(rx * 0.3)} A {rx} {int(rx * 0.9)} 0 0 1 {int(rx * 0.5)} {-int(rx * 0.7)}" fill="none" stroke="#f7e3ad" stroke-opacity="0.45" stroke-width="6"/></g>""")
    return shell(t, f"""{plate(600, 424, 372, 322)}
{chr(10).join(rings)}
{crumb(600, 430, 300, 190, 20, '#a8701f', 7)}""")


def a_fingers(t, d, c):
    """Chicken Fingers — battered strips with fries and a dip cup."""
    strips = []
    for i, (x, y, rot) in enumerate([(520, 404, -14), (640, 392, 5), (752, 412, 16),
                                     (584, 468, -6), (700, 476, 10)]):
        strips.append(f"""    <g transform="translate({x} {y}) rotate({rot})">
      <rect x="-130" y="-24" width="260" height="48" rx="24" fill="#c9902f"/>
      <rect x="-130" y="-26" width="260" height="44" rx="22" fill="{c}"/>
      <ellipse cx="130" cy="-4" rx="14" ry="21" fill="#f7e3ad"/>
      <ellipse cx="112" cy="-4" rx="6" ry="13" fill="#fdf3d6" opacity="0.7"/></g>""")
    return shell(t, f"""{plate(600, 430, 380, 300)}
{chr(10).join(strips)}
{fries(660, 500, 9, 5, '#e0a94a', 220, 54)}
{crumb(620, 420, 260, 130, 18, '#a8701f', 11)}
{dip(866, 470, 52, '#f0e2b8', '#d9c58c', '#f7f2e6')}""")


def a_pretzels(t, d, c):
    """Soft Bavarian Pretzels — the classic twisted loop."""
    loops = []
    for i, (x, y, s, rot) in enumerate([(516, 424, 1.0, -8), (700, 416, 0.92, 12)]):
        loops.append(f"""    <g transform="translate({x} {y}) rotate({rot}) scale({s})">
      <path d="M-70 40 C -110 -30, -60 -90, 0 -84 C 58 -90, 108 -34, 70 34
               C 44 76, -40 78, -70 40 Z" fill="none" stroke="#b8812c" stroke-width="44" stroke-linecap="round"/>
      <path d="M-70 34 C -108 -34, -58 -92, 0 -86 C 56 -92, 106 -36, 70 28
               C 44 70, -40 72, -70 34 Z" fill="none" stroke="{c}" stroke-width="38" stroke-linecap="round"/>
      <path d="M-34 -84 C -14 -50, 14 -50, 34 -84" fill="none" stroke="{c}" stroke-width="34" stroke-linecap="round"/>
      <path d="M-84 6 C -60 -6, -40 -2, -26 10" fill="none" stroke="#f7e3ad" stroke-opacity="0.4" stroke-width="7" stroke-linecap="round"/>
      <circle cx="-44" cy="18" r="5" fill="#fff" opacity="0.45"/>
      <circle cx="30" cy="-4" r="4" fill="#fff" opacity="0.4"/></g>""")
    return shell(t, f"""{plate(600, 428, 372, 320)}
{chr(10).join(loops)}
{crumb(600, 440, 250, 150, 18, '#a8701f', 5)}
{dip(858, 478, 54, '#e8c15a', '#c39a34', '#f2ece0')}""")


def a_cheese_balls(t, d, c):
    """Hot Pepper Cheese Balls — breaded spheres in a bowl with ranch."""
    balls = []
    import math
    for i in range(13):
        a = (i * 137.5 + 44) % 360
        rad = ((i * 43 + 19) % 92) / 92.0
        x = 592 + math.cos(math.radians(a)) * 210 * rad
        y = 424 + math.sin(math.radians(a)) * 128 * rad
        r = 42 + (i % 3) * 6
        balls.append(f"""    <g transform="translate({int(x)} {int(y)})">
      <circle cx="0" cy="6" r="{r}" fill="#b8812c"/>
      <circle cx="0" cy="0" r="{r}" fill="{c}"/>
      <circle cx="{int(-r * 0.3)}" cy="{int(-r * 0.32)}" r="{int(r * 0.28)}" fill="#f7e3ad" opacity="0.5"/>
      <circle cx="{int(r * 0.34)}" cy="{int(r * 0.26)}" r="{int(r * 0.12)}" fill="#a8701f" opacity="0.45"/></g>""")
    return shell(t, f"""    <ellipse cx="592" cy="428" rx="286" ry="212" fill="url(#plate)"/>
    <ellipse cx="592" cy="428" rx="286" ry="212" fill="none" stroke="#8d6039" stroke-opacity="0.35" stroke-width="4"/>
    <ellipse cx="592" cy="436" rx="248" ry="180" fill="#efe7d8"/>
{chr(10).join(balls)}
{dip(870, 486, 56, '#f4ead0', '#dcc79a', '#faf6ec')}""")


def a_potato_skins(t, d, c):
    """Loaded Potato Skins — half shells, chived and loaded."""
    skins = []
    for i, (x, y, rot) in enumerate([(486, 424, -14), (606, 404, 4), (728, 430, 16),
                                     (546, 490, -4), (668, 494, 12)]):
        skins.append(f"""    <g transform="translate({x} {y}) rotate({rot})">
      <path d="M-84 30 A 84 72 0 0 1 84 30 Z" fill="#c08a3a"/>
      <path d="M-84 26 A 84 72 0 0 1 84 26 Z" fill="#e8c588"/>
      <path d="M-64 24 A 64 54 0 0 1 64 24 Z" fill="{c}"/>
      <g fill="#fdf0c8" opacity="0.85">
        <ellipse cx="-26" cy="10" rx="20" ry="11"/><ellipse cx="14" cy="18" rx="24" ry="12"/>
        <ellipse cx="40" cy="4" rx="16" ry="9"/></g>
      <g fill="#8f3b2c" opacity="0.8">
        <rect x="-52" y="14" width="20" height="6" rx="3" transform="rotate(-12 -42 17)"/>
        <rect x="6" y="-2" width="22" height="6" rx="3" transform="rotate(10 17 1)"/></g>
      <g fill="#4a7a34">
        <rect x="-14" y="-8" width="4" height="10" rx="2" transform="rotate(30 -12 -3)"/>
        <rect x="26" y="20" width="4" height="10" rx="2" transform="rotate(-24 28 25)"/>
        <rect x="-34" y="4" width="4" height="9" rx="2" transform="rotate(18 -32 8)"/></g></g>""")
    return shell(t, f"""{plate(600, 432, 376, 316)}
{chr(10).join(skins)}
{dip(866, 486, 52, '#f4ead0', '#dcc79a', '#faf6ec')}""")


def a_zucchini(t, d, c):
    """Zucchini Planks — battered strips with marinara."""
    planks = []
    for i, (x, y, rot) in enumerate([(496, 416, -16), (614, 398, 3), (730, 422, 15),
                                     (556, 480, -6), (676, 486, 10)]):
        planks.append(f"""    <g transform="translate({x} {y}) rotate({rot})">
      <rect x="-118" y="-19" width="236" height="38" rx="19" fill="#b8812c"/>
      <rect x="-118" y="-21" width="236" height="34" rx="17" fill="{c}"/>
      <rect x="-104" y="-15" width="60" height="7" rx="3.5" fill="#f7e3ad" opacity="0.45"/></g>""")
    return shell(t, f"""{plate(600, 430, 372, 314)}
{chr(10).join(planks)}
{leaf(360, 372, 0.8, -18, '#5c8a3a')}
{leaf(392, 352, 0.66, 14, '#4a7a34')}
{dip(866, 478, 54, '#c4483c', '#8b2e2e')}""")


def a_shrimp(t, d, c):
    """Shrimp Basket — panko shrimp, cocktail sauce, slaw and fries."""
    shrimp = []
    import math
    for i in range(8):
        a = (i * 137.5 + 66) % 360
        rad = ((i * 43 + 11) % 88) / 88.0
        x = 552 + math.cos(math.radians(a)) * 180 * rad
        y = 410 + math.sin(math.radians(a)) * 110 * rad
        rot = ((i * 37 + 5) % 80) - 40
        shrimp.append(f"""    <g transform="translate({int(x)} {int(y)}) rotate({rot})">
      <path d="M-42 14 C -56 -14, -30 -44, 4 -42 C 40 -40, 54 -12, 38 10
               C 24 30, -8 34, -24 22" fill="none" stroke="#c9902f" stroke-width="30" stroke-linecap="round"/>
      <path d="M-42 8 C -54 -18, -30 -46, 4 -44 C 38 -42, 52 -14, 36 8
               C 22 26, -8 30, -24 18" fill="none" stroke="{c}" stroke-width="26" stroke-linecap="round"/>
      <path d="M-30 -34 L -36 -52 M -6 -40 L -8 -60 M 18 -32 L 24 -50" stroke="#f7e3ad" stroke-opacity="0.5" stroke-width="5" stroke-linecap="round"/></g>""")
    return shell(t, f"""{plate(600, 428, 380, 318)}
{chr(10).join(shrimp)}
{fries(620, 500, 8, 9, '#e0a94a', 190, 48)}
    <g transform="translate(800 452)">
      <ellipse cx="0" cy="0" rx="74" ry="44" fill="#f0e8d6"/>
      <g fill="#e8dcc0"><ellipse cx="-28" cy="-8" rx="26" ry="11" transform="rotate(-16 -28 -8)"/>
      <ellipse cx="16" cy="8" rx="30" ry="12" transform="rotate(12 16 8)"/></g></g>
{dip(340, 486, 54, '#c4483c', '#8b2e2e')}""")


def a_pounder(t, d, c):
    """The Pounder / Loaded Pounder — a mound of fries, optional cheese."""
    loaded = "loaded" in t.lower()
    body = fries(600, 430, 26, 3, c, 300, 84) if not loaded else fries(600, 420, 24, 3, "#e6c98d", 296, 84)
    extra = ""
    if loaded:
        extra = f"""    <g opacity="0.9">
      <path d="M360 400 C 470 372, 740 372, 850 404 C 760 452, 450 452, 360 400 Z" fill="#f2d489" opacity="0.75"/>
      <path d="M400 386 C 500 366, 700 366, 800 388" fill="none" stroke="#fbe9b6" stroke-opacity="0.6" stroke-width="9"/>
    </g>
{leaf(430, 388, 0.62, -14, '#4a7a34')}
{leaf(770, 390, 0.62, 16, '#4a7a34')}
    <g fill="#8f3b2c" opacity="0.85">
      <rect x="470" y="366" width="34" height="9" rx="4.5" transform="rotate(-12 487 370)"/>
      <rect x="560" y="360" width="30" height="9" rx="4.5" transform="rotate(8 575 364)"/>
      <rect x="650" y="364" width="32" height="9" rx="4.5" transform="rotate(-6 666 368)"/></g>"""
    return shell(t, f"""{board(600, 452, 396, 176)}
{body}
{extra}""")


def a_gyro_fries(t, d, c):
    """Gyro Fries — gyro meat and cheese over fries, cucumber sauce alongside."""
    meat = []
    import math
    for i in range(11):
        a = (i * 137.5 + 88) % 360
        rad = ((i * 47 + 7) % 86) / 86.0
        x = 592 + math.cos(math.radians(a)) * 220 * rad
        y = 412 + math.sin(math.radians(a)) * 120 * rad
        rot = ((i * 41 + 3) % 70) - 35
        meat.append(f'    <g transform="translate({int(x)} {int(y)}) rotate({rot})">'
                    f'<ellipse cx="0" cy="0" rx="42" ry="17" fill="#7d4a2a"/>'
                    f'<ellipse cx="0" cy="-4" rx="42" ry="16" fill="{c}"/>'
                    f'<path d="M-26 -6 C -14 -14, 6 -12, 20 -4" fill="none" stroke="#a9713f" stroke-opacity="0.6" stroke-width="4"/></g>')
    return shell(t, f"""{board(600, 440, 380, 168)}
{fries(600, 428, 17, 6, '#e0a94a', 268, 70)}
{chr(10).join(meat)}
    <g fill="#f2d489" opacity="0.7">
      <path d="M420 398 C 500 380, 690 380, 770 400 C 690 430, 500 430, 420 398 Z"/></g>
{dip(884, 500, 52, '#f0ead2', '#d6c89c', '#f8f4ea')}""")


def a_burger(t, d, c):
    """Burgers — stacked, seeded bun, fillings visible at the cut."""
    bacon = "bacon" in t.lower()
    plain = t.lower().strip() == "hamburger"
    layers = []
    # bottom bun
    layers.append('    <path d="M388 470 C 388 520, 812 520, 812 470 Z" fill="#c08a3a"/>')
    layers.append('    <path d="M388 466 C 388 512, 812 512, 812 466 Z" fill="#e8c588"/>')
    if not plain:
        layers.append('    <rect x="372" y="440" width="456" height="30" rx="14" fill="#f2d489"/>')
        layers.append('    <rect x="372" y="442" width="456" height="24" rx="12" fill="#fbe4a8" opacity="0.85"/>')
        if bacon:
            layers.append('    <g fill="#9c3b2c" opacity="0.92">'
                          '<path d="M390 420 q 24 -16 48 0 q 24 16 48 0 q 24 -16 48 0 q 24 16 48 0 q 24 -16 48 0 q 24 16 48 0 q 24 -16 48 0" '
                          'fill="none" stroke="#9c3b2c" stroke-width="14" stroke-linecap="round"/></g>')
    layers.append('    <rect x="376" y="404" width="448" height="34" rx="12" fill="#6f3a22"/>')
    layers.append('    <rect x="376" y="408" width="448" height="26" rx="12" fill="{PATTY}"/>')
    layers.append('    <rect x="380" y="398" width="440" height="16" rx="8" fill="#4a7a34"/>')
    if not plain:
        layers.append('    <g fill="#c8402f" opacity="0.9"><ellipse cx="440" cy="396" rx="34" ry="12"/>'
                      '<ellipse cx="540" cy="392" rx="36" ry="13"/><ellipse cx="648" cy="396" rx="32" ry="12"/></g>')
        layers.append('    <g fill="none" stroke="#efe0f2" stroke-width="9" opacity="0.9">'
                      '<ellipse cx="480" cy="390" rx="26" ry="9"/><ellipse cx="600" cy="386" rx="28" ry="10"/></g>')
    # top bun
    layers.append('    <path d="M372 396 C 372 288, 828 288, 828 396 Z" fill="#d19a4a"/>')
    layers.append('    <path d="M372 392 C 372 292, 828 292, 828 392 Z" fill="#e8c588"/>')
    layers.append('    <g fill="#fdf0c8" opacity="0.85">'
                  '<ellipse cx="450" cy="352" rx="9" ry="5" transform="rotate(-16 450 352)"/>'
                  '<ellipse cx="530" cy="330" rx="9" ry="5" transform="rotate(10 530 330)"/>'
                  '<ellipse cx="620" cy="322" rx="9" ry="5" transform="rotate(-8 620 322)"/>'
                  '<ellipse cx="710" cy="344" rx="9" ry="5" transform="rotate(14 710 344)"/>'
                  '<ellipse cx="490" cy="316" rx="8" ry="4"/><ellipse cx="668" cy="310" rx="8" ry="4"/></g>')
    body = "\n".join(layers).replace("{PATTY}", c)
    return shell(t, f"""    <ellipse cx="600" cy="516" rx="250" ry="34" fill="#000" opacity="0.22"/>
{body}""")


def a_eggroll(t, d, c):
    """Eggrolls — three crisp tubes, one broken open to show the filling."""
    rolls = []
    import math
    for i, (x, y, rot) in enumerate([(486, 428, -20), (628, 404, -4), (766, 434, 14)]):
        rolls.append(f"""    <g transform="translate({x} {y}) rotate({rot})">
      <rect x="-104" y="-40" width="208" height="80" rx="38" fill="#b8812c"/>
      <rect x="-104" y="-42" width="208" height="74" rx="36" fill="{c}"/>
      <rect x="-88" y="-30" width="176" height="14" rx="7" fill="#f7e3ad" opacity="0.42"/>
      <g fill="#a8701f" opacity="0.38">
        <circle cx="-52" cy="8" r="5"/><circle cx="6" cy="16" r="4"/><circle cx="58" cy="-2" r="5"/></g>
      <ellipse cx="-104" cy="-4" rx="12" ry="30" fill="#f2cd7c"/>
      <ellipse cx="-104" cy="-4" rx="8" ry="21" fill="#fbeec2" opacity="0.8"/></g>""")
    buffalo = "buffalo" in t.lower()
    dip_c = "#f0e2b8" if not buffalo else "#c4483c"
    dip_d = "#d9c58c" if not buffalo else "#8b2e2e"
    return shell(t, f"""{plate(600, 432, 378, 320)}
{chr(10).join(rolls)}
{crumb(600, 440, 280, 150, 20, '#a8701f', 13)}
{dip(872, 486, 54, dip_c, dip_d, '#f7f2e6' if not buffalo else '#f2ece0')}""")


def a_hoagie(t, d, c):
    """Hoagies / sandwiches — cut on the bias, fillings spilling."""
    long_ = t.lower()
    veg = "veggie" in long_
    meatball = "meatball" in long_
    gyro = t.lower().strip() == "gyro"
    cod = "cod" in long_
    steak = "philly" in long_
    italian = "italian" in long_

    fillings = []
    if gyro:
        fills = ('        <ellipse cx="-90" cy="-6" rx="52" ry="15" fill="#c9a06a"/>'
                 '<ellipse cx="10" cy="-4" rx="54" ry="15" fill="#b8895a"/>'
                 '<ellipse cx="106" cy="-8" rx="50" ry="14" fill="#c9a06a"/>')
    elif meatball:
        fills = ('        <circle cx="-86" cy="-8" r="34" fill="#8f5a30"/>'
                 '<circle cx="10" cy="-4" r="36" fill="#9c6437"/>'
                 '<circle cx="108" cy="-10" r="33" fill="#8f5a30"/>'
                 '<path d="M-160 6 C -80 -14, 80 -12, 160 4" fill="none" stroke="#c4483c" stroke-width="12" opacity="0.85"/>')
    else:
        fills = ('        <rect x="-150" y="-16" width="120" height="26" rx="12" fill="#8f4a26"/>'
                 '<rect x="-20" y="-14" width="130" height="24" rx="12" fill="#a35a2e"/>'
                 '<rect x="120" y="-16" width="80" height="26" rx="12" fill="#8f4a26"/>')
        if italian:
            fills += ('<ellipse cx="-120" cy="-20" rx="42" ry="10" fill="#d4604f"/>'
                     '<ellipse cx="-40" cy="-22" rx="44" ry="10" fill="#c8503f"/>'
                     '<ellipse cx="46" cy="-20" rx="42" ry="10" fill="#d4604f"/>')
        if cod:
            fills = ('        <path d="M-160 -12 C -110 -26, -50 -20, 10 -12 C 70 -4, 120 -10, 160 -14 '
                     'L160 8 C 110 16, 40 12, -20 6 C -80 0, -120 6, -160 8 Z" fill="#f2ead6"/>'
                     '<path d="M-160 -8 C -100 -18, -30 -14, 40 -8" fill="none" stroke="#e0d4b8" stroke-width="7"/>')
    veg_bits = ""
    if veg or steak or gyro:
        veg_bits = f"""      <g fill="#4a7a34"><path d="M-120 6 C -100 -8, -70 -8, -52 6 Z"/>
        <path d="M40 4 C 60 -10, 92 -10, 110 4 Z"/></g>
      <g fill="#c8402f" opacity="0.9"><ellipse cx="-16" cy="2" rx="30" ry="11"/>
        <ellipse cx="96" cy="6" rx="28" ry="10"/></g>
      <g fill="none" stroke="#efe0f2" stroke-width="8" opacity="0.9">
        <ellipse cx="52" cy="0" rx="26" ry="9"/></g>"""
        if steak or veg:
            veg_bits += """      <g fill="#8a5a33"><ellipse cx="-96" cy="4" rx="24" ry="9" transform="rotate(-12 -96 4)"/>
        <ellipse cx="70" cy="8" rx="24" ry="9" transform="rotate(10 70 8)"/></g>"""
    else:
        veg_bits = """      <g fill="#4a7a34"><path d="M-90 4 C -70 -10, -40 -10, -22 4 Z"/></g>
      <g fill="#c8402f" opacity="0.9"><ellipse cx="40" cy="2" rx="28" ry="10"/></g>
      <g fill="none" stroke="#efe0f2" stroke-width="8" opacity="0.9"><ellipse cx="104" cy="6" rx="24" ry="9"/></g>"""

    bun_bot = '    <path d="M300 430 C 300 496, 900 496, 900 430 Z" fill="#c08a3a"/>'
    bun_bot2 = '    <path d="M300 426 C 300 490, 900 490, 900 426 Z" fill="#e8c588"/>'
    bun_top = """    <path d="M296 428 C 296 302, 904 302, 904 428 Z" fill="#d19a4a"/>
    <path d="M296 424 C 296 306, 904 306, 904 424 Z" fill="#e8c588"/>
    <g fill="#fdf0c8" opacity="0.8">
      <ellipse cx="400" cy="382" rx="10" ry="5" transform="rotate(-14 400 382)"/>
      <ellipse cx="500" cy="356" rx="10" ry="5" transform="rotate(8 500 356)"/>
      <ellipse cx="610" cy="344" rx="10" ry="5" transform="rotate(-6 610 344)"/>
      <ellipse cx="720" cy="366" rx="10" ry="5" transform="rotate(12 720 366)"/>
      <ellipse cx="812" cy="396" rx="9" ry="5"/></g>"""
    cut = """    <g transform="translate(880 430) rotate(14)">
      <ellipse cx="0" cy="0" rx="66" ry="62" fill="#fbe4a8"/>
      <ellipse cx="0" cy="0" rx="52" ry="48" fill="#fdf0c8"/>"""
    fill_cut = f"""      <g fill="#8f4a26" opacity="0.9"><ellipse cx="-14" cy="-8" rx="26" ry="12"/>
        <ellipse cx="18" cy="12" rx="24" ry="11"/></g>
      <g fill="#f2d489"><path d="M-44 4 C -20 -8, 20 -6, 44 4 C 20 18, -20 16, -44 4 Z"/></g>
      <g fill="#4a7a34"><path d="M-30 14 C -14 2, 14 2, 30 14 Z"/></g>
      <g fill="#c8402f" opacity="0.85"><circle cx="-16" cy="-14" r="9"/><circle cx="20" cy="2" r="8"/></g>
    </g>"""

    body = f"""{bun_bot}
{bun_bot2}
    <g transform="translate(0 0)">
      <clipPath id="fillclip"><path d="M320 414 L880 414 L880 452 L320 452 Z"/></clipPath>
      <g clip-path="url(#fillclip)">
{fills}
{veg_bits}
      </g>
    </g>
{bun_top}
    <g>
{cut}
{fill_cut}
    </g>"""
    return shell(t, body)


def a_salad(t, d, c):
    """Salads — a deep bowl of greens with the item's own toppings."""
    steak = "steak" in t.lower()
    gyro = "gyro" in t.lower()
    toasted = "breaded" in t.lower()
    tossed = t.lower().strip() == "tossed salad"

    top = ""
    if not tossed:
        if toasted:
            top = f"""      <g>
        <rect x="-70" y="-16" width="90" height="32" rx="16" fill="#c9902f" transform="rotate(-12 -25 0)"/>
        <rect x="-70" y="-18" width="90" height="28" rx="14" fill="{c}" transform="rotate(-12 -25 -2)"/>
        <rect x="14" y="-14" width="84" height="30" rx="15" fill="#c9902f" transform="rotate(14 56 2)"/>
        <rect x="14" y="-16" width="84" height="26" rx="13" fill="{c}" transform="rotate(14 56 0)"/>
      </g>"""
        elif gyro:
            top = f"""      <g>
        <ellipse cx="-52" cy="-6" rx="48" ry="16" fill="#c9a06a"/>
        <ellipse cx="16" cy="4" rx="50" ry="16" fill="#b8895a"/>
        <ellipse cx="80" cy="-10" rx="46" ry="15" fill="#c9a06a"/>
      </g>"""
        else:
            top = f"""      <g>
        <ellipse cx="-44" cy="-4" rx="52" ry="17" fill="#8f5a30"/>
        <ellipse cx="34" cy="8" rx="54" ry="17" fill="{c}"/>
        <ellipse cx="96" cy="-8" rx="46" ry="16" fill="#8f5a30"/>
      </g>"""
    toppings = """      <g fill="#c8402f" opacity="0.92">
        <ellipse cx="-88" cy="14" rx="26" ry="10"/><ellipse cx="34" cy="-26" rx="24" ry="9"/>
        <ellipse cx="104" cy="18" rx="24" ry="9"/></g>
      <g fill="none" stroke="#fdf0c8" stroke-width="7" opacity="0.95">
        <ellipse cx="-16" cy="26" rx="26" ry="10"/>
        <ellipse cx="82" cy="-30" rx="22" ry="9"/></g>
      <g fill="none" stroke="#efe0f2" stroke-width="8" opacity="0.9">
        <ellipse cx="-58" cy="-24" rx="24" ry="9"/><ellipse cx="60" cy="30" rx="22" ry="9"/></g>
      <g fill="#3f4a33">
        <ellipse cx="8" cy="-14" rx="11" ry="13"/><ellipse cx="120" cy="4" rx="10" ry="12"/>
        <ellipse cx="-110" cy="-6" rx="10" ry="12"/></g>"""
    greens = "".join([
        leaf(600 + (i * 97 - 300) // 2, 420 + ((i * 53) % 90) - 45, 1.5, (i * 47) % 360 - 180)
        for i in range(11)])
    body = f"""{plate(600, 436, 372, 316)}
    <g transform="translate(600 420)">{greens}</g>
    <g transform="translate(600 420)">
{top}
{toppings}
    </g>"""
    return shell(t, body)


def a_stromboli(t, d, c):
    """Stromboli — the folded bake, seam and blistered top showing."""
    toppings = ""
    if "pepperoni" in t.lower():
        toppings = """      <g fill="#c9553f">
        <ellipse cx="-92" cy="-16" rx="26" ry="20"/><ellipse cx="-14" cy="-34" rx="26" ry="20"/>
        <ellipse cx="62" cy="-14" rx="26" ry="20"/><ellipse cx="124" cy="-34" rx="24" ry="19"/></g>"""
    elif "meatball" in t.lower():
        toppings = """      <g fill="#8f5a30">
        <ellipse cx="-70" cy="-18" rx="28" ry="21"/><ellipse cx="6" cy="-34" rx="30" ry="22"/>
        <ellipse cx="84" cy="-16" rx="28" ry="21"/></g>
      <path d="M-140 6 C -70 -10, 60 -8, 140 6" fill="none" stroke="#c4483c" stroke-width="11" opacity="0.8"/>"""
    elif "philly" in t.lower():
        toppings = """      <g fill="#8f4a26">
        <rect x="-120" y="-30" width="96" height="24" rx="12" transform="rotate(-10 -72 -18)"/>
        <rect x="-10" y="-38" width="104" height="24" rx="12" transform="rotate(6 42 -26)"/></g>
      <g fill="#4a7a34"><path d="M-40 -14 C -20 -30, 10 -28, 28 -12 Z"/>
        <path d="M88 -10 C 106 -26, 134 -24, 150 -8 Z"/></g>
      <g fill="#8a5a33"><ellipse cx="-96" cy="-4" rx="22" ry="9"/>
        <ellipse cx="62" cy="-2" rx="22" ry="9"/></g>"""
    else:  # chicken / sausage
        bits = "#c9902f" if "chicken" in t.lower() else "#a35a2e"
        toppings = f"""      <g fill="{bits}">
        <ellipse cx="-84" cy="-16" rx="34" ry="18" transform="rotate(-12 -84 -16)"/>
        <ellipse cx="0" cy="-32" rx="36" ry="18" transform="rotate(8 0 -32)"/>
        <ellipse cx="86" cy="-14" rx="34" ry="18" transform="rotate(-6 86 -14)"/></g>
      <g fill="#4a7a34"><path d="M-40 -8 C -18 -24, 14 -22, 34 -6 Z"/>
        <path d="M56 -2 C 76 -18, 104 -16, 122 0 Z"/></g>"""

    body = f"""    <ellipse cx="600" cy="530" rx="330" ry="40" fill="#000" opacity="0.22"/>
    <g transform="translate(600 424) rotate(-4)">
      <path d="M-360 40 C -370 -60, -300 -130, -120 -140 C 60 -150, 250 -136, 340 -80
               C 372 -58, 376 -14, 360 40 Z" fill="#b8812c"/>
      <path d="M-356 34 C -364 -62, 296 -66, 354 34 Z" fill="{c}"/>
      <path d="M-330 10 C -300 -84, 260 -90, 320 4" fill="none" stroke="#f7e3ad" stroke-opacity="0.4" stroke-width="12"/>
      {toppings}
      <g fill="#c9902f" opacity="0.35">
        <ellipse cx="-140" cy="-58" rx="16" ry="9"/><ellipse cx="-20" cy="-84" rx="13" ry="8"/>
        <ellipse cx="110" cy="-70" rx="15" ry="8"/><ellipse cx="210" cy="-42" rx="12" ry="7"/></g>
      <g fill="#fdf0c8" opacity="0.55">
        <ellipse cx="-230" cy="-30" rx="18" ry="7" transform="rotate(-14 -230 -30)"/>
        <ellipse cx="60" cy="-16" rx="16" ry="6"/></g>
      <path d="M-350 34 C -250 66, 240 66, 352 34" fill="none" stroke="#8f5a20" stroke-opacity="0.55" stroke-width="7"/>
    </g>"""
    return shell(t, body)


def a_wings(t, d, c):
    """Wings — glazed drums and flats, celery and ranch alongside."""
    boneless = "boneless" in t.lower()
    bbq = "bbq" in t.lower()
    pieces = []
    import math
    n = 11 if boneless else 8
    for i in range(n):
        a = (i * 137.5 + 30) % 360
        rad = ((i * 47 + 21) % 90) / 90.0
        x = 560 + math.cos(math.radians(a)) * 216 * rad
        y = 416 + math.sin(math.radians(a)) * 132 * rad
        rot = ((i * 53 + 9) % 100) - 50
        if boneless:
            shape = (f'<path d="M-46 20 C -62 -12, -30 -44, 8 -40 C 46 -36, 58 -6, 38 16 '
                     f'C 20 36, -18 38, -32 26" fill="none" stroke="{c if not bbq else "#a5522a"}" stroke-width="38" stroke-linecap="round"/>'
                     f'<path d="M-30 -30 C -18 -44, 4 -46, 16 -36" fill="none" stroke="#f7e3ad" stroke-opacity="0.35" stroke-width="8" stroke-linecap="round"/>')
        else:
            shape = (f'<ellipse cx="-16" cy="4" rx="34" ry="26" fill="{c if not bbq else "#a5522a"}"/>'
                     f'<ellipse cx="30" cy="-14" rx="30" ry="22" fill="{c if not bbq else "#a5522a"}"/>'
                     f'<path d="M-34 -6 C -14 -14, 2 -12, 10 -4" fill="none" stroke="#f7e3ad" stroke-opacity="0.4" stroke-width="8" stroke-linecap="round"/>'
                     f'<path d="M-44 16 C -30 24, -16 26, -8 22" fill="none" stroke="#7a3a12" stroke-opacity="0.35" stroke-width="7" stroke-linecap="round"/>')
        pieces.append(f'    <g transform="translate({int(x)} {int(y)}) rotate({rot})">{shape}</g>')

    celery = """    <g transform="translate(872 462)">
      <g fill="#7ba64a"><path d="M-14 34 C -30 4, -18 -28, 0 -46 C 18 -28, 30 4, 14 34 Z"/></g>
      <g fill="#9ccb6a" opacity="0.7"><path d="M-8 34 C -20 6, -12 -22, 0 -38 C 10 -20, 16 8, 6 34 Z"/></g>
      <g fill="#5c8a3a"><path d="M16 36 C 2 8, 10 -22, 26 -38 C 42 -20, 52 8, 38 36 Z"/></g>
    </g>"""
    return shell(t, f"""{plate(600, 430, 378, 322)}
{chr(10).join(pieces)}
{celery if boneless or "jumbo" in t.lower() else ""}
{dip(872, 528, 50, '#f0e2b8', '#d9c58c', '#f7f2e6')}""")


def a_wing_flavors(t, d, c):
    """Wing Flavors — the sauce lineup, the only page that is a list."""
    sauces = [
        ("Hot", "#c8402f", "#8b2e2e"), ("Mild", "#d88a3a", "#a8642c"),
        ("Thai-Chili", "#b8452c", "#7f2b1c"), ("Garlic Butter", "#e0c169", "#b39543"),
        ("Hot Garlic Parm", "#c4693a", "#94431f"), ("BBQ", "#8f4a26", "#5f2e17"),
        ("Spicy BBQ", "#7d3a1c", "#4f2310"), ("Garlic Parm", "#e2c98a", "#b8a267"),
        ("Cajun", "#b06a30", "#7d4520"), ("Seasoned", "#9a7a4a", "#6b5330"),
        ("Ranch", "#f0e6cc", "#cfc2a2"), ("Bleu Cheese", "#dfe4ea", "#b3bcc8"),
    ]
    cups = []
    for i, (name, top, deep) in enumerate(sauces):
        col, row = i % 4, i // 4
        x = 372 + col * 152
        y = 300 + row * 132
        cups.append(f"""    <g transform="translate({x} {y})">
      <ellipse cx="0" cy="10" rx="46" ry="13" fill="#000" opacity="0.2"/>
      <ellipse cx="0" cy="0" rx="42" ry="40" fill="#f2ece0"/>
      <ellipse cx="0" cy="0" rx="33" ry="31" fill="{top}"/>
      <ellipse cx="0" cy="0" rx="33" ry="31" fill="none" stroke="{deep}" stroke-opacity="0.5" stroke-width="3"/>
      <ellipse cx="-11" cy="-11" rx="9" ry="6" fill="#fff" opacity="0.28"/>
      <text x="0" y="66" text-anchor="middle" font-family="Oswald, Impact, sans-serif" fill="#d6c3a4" font-size="19" letter-spacing="1">{name}</text>
    </g>""")
    return shell(t, "\n".join(cups))


def a_pizza_pie(t, d, c):
    """Small / Medium / Large Pizza — plain cheese, drawn to real diameter.

    Each size is the same construction scaled to its actual inch diameter
    (10 / 14 / 18) so the size difference reads in the art itself.
    """
    scale = {"small pizza": 0.556, "medium pizza": 0.778}.get(t.lower().strip(), 1.0)
    return shell(t, f"""{plate(600, 404, 372, 344, inner=0.9)}
    <g transform="translate(600 400) scale({scale:.3f})">
      <ellipse cx="0" cy="10" rx="298" ry="282" fill="#000" opacity="0.18"/>
      <ellipse cx="0" cy="0" rx="298" ry="282" fill="#d99b45"/>
      <ellipse cx="0" cy="0" rx="298" ry="282" fill="none" stroke="#a06a22" stroke-opacity="0.5" stroke-width="3"/>
      <g fill="#f0cd8d" opacity="0.6">
        <ellipse cx="-200" cy="-98" rx="17" ry="12"/><ellipse cx="-86" cy="-212" rx="19" ry="13"/>
        <ellipse cx="54" cy="-230" rx="16" ry="11"/><ellipse cx="180" cy="-154" rx="18" ry="12"/>
        <ellipse cx="234" cy="-16" rx="15" ry="10"/><ellipse cx="192" cy="132" rx="17" ry="12"/>
        <ellipse cx="60" cy="222" rx="19" ry="13"/><ellipse cx="-90" cy="218" rx="16" ry="11"/>
        <ellipse cx="-208" cy="122" rx="18" ry="12"/><ellipse cx="-242" cy="14" rx="15" ry="10"/>
      </g>
      <ellipse cx="0" cy="0" rx="244" ry="230" fill="#c94a35"/>
      <g fill="{c}">
        <ellipse cx="-122" cy="-116" rx="130" ry="100"/><ellipse cx="100" cy="-144" rx="116" ry="90"/>
        <ellipse cx="172" cy="-18" rx="124" ry="104"/><ellipse cx="46" cy="136" rx="136" ry="108"/>
        <ellipse cx="-144" cy="88" rx="122" ry="96"/><ellipse cx="-24" cy="-8" rx="134" ry="108"/>
      </g>
      <g fill="#fbe9b6" opacity="0.75">
        <ellipse cx="-100" cy="-136" rx="60" ry="38"/><ellipse cx="108" cy="-156" rx="52" ry="34"/>
        <ellipse cx="154" cy="6" rx="58" ry="40"/><ellipse cx="28" cy="144" rx="62" ry="42"/>
        <ellipse cx="-160" cy="100" rx="54" ry="36"/>
      </g>
      <g fill="#c98a34" opacity="0.28">
        <ellipse cx="-32" cy="-60" rx="32" ry="17"/><ellipse cx="76" cy="74" rx="28" ry="15"/>
        <ellipse cx="-122" cy="36" rx="26" ry="14"/>
      </g>
    </g>""")


def a_ultimate_pepperoni(t, d, c):
    """Ultimate Pepperoni — cheese field under pepperoni cups."""
    return shell(t, f"""{plate(600, 404, 372, 344, inner=0.9)}
    <g transform="translate(600 400)">
      <ellipse cx="0" cy="10" rx="292" ry="276" fill="#000" opacity="0.18"/>
      <ellipse cx="0" cy="0" rx="292" ry="276" fill="#d99b45"/>
      <ellipse cx="0" cy="0" rx="292" ry="276" fill="none" stroke="#a06a22" stroke-opacity="0.5" stroke-width="3"/>
      <g fill="#f0cd8d" opacity="0.6">
        <ellipse cx="-196" cy="-96" rx="17" ry="12"/><ellipse cx="-84" cy="-206" rx="19" ry="13"/>
        <ellipse cx="52" cy="-224" rx="16" ry="11"/><ellipse cx="176" cy="-150" rx="18" ry="12"/>
        <ellipse cx="228" cy="-16" rx="15" ry="10"/><ellipse cx="188" cy="128" rx="17" ry="12"/>
      </g>
      <ellipse cx="0" cy="0" rx="238" ry="224" fill="#c94a35"/>
      <g fill="#fdf0c8">
        <ellipse cx="-118" cy="-112" rx="126" ry="98"/><ellipse cx="96" cy="-140" rx="112" ry="86"/>
        <ellipse cx="168" cy="-18" rx="120" ry="100"/><ellipse cx="44" cy="132" rx="132" ry="104"/>
        <ellipse cx="-140" cy="86" rx="118" ry="92"/><ellipse cx="-24" cy="-8" rx="130" ry="104"/>
      </g>
      <g fill="{c}" stroke="#6d2222" stroke-opacity="0.5" stroke-width="2">
        <ellipse cx="-96" cy="-104" rx="40" ry="36"/><ellipse cx="86" cy="-128" rx="38" ry="35"/>
        <ellipse cx="158" cy="-14" rx="41" ry="38"/><ellipse cx="34" cy="128" rx="39" ry="36"/>
        <ellipse cx="-148" cy="74" rx="38" ry="35"/><ellipse cx="-6" cy="-6" rx="42" ry="39"/>
        <ellipse cx="-176" cy="-34" rx="34" ry="31"/><ellipse cx="112" cy="66" rx="35" ry="32"/>
      </g>
      <g fill="#7d2a26" opacity="0.55">
        <ellipse cx="-104" cy="-96" rx="9" ry="8"/><ellipse cx="-82" cy="-112" rx="8" ry="7"/>
        <ellipse cx="78" cy="-120" rx="9" ry="8"/><ellipse cx="96" cy="-136" rx="7" ry="6"/>
        <ellipse cx="150" cy="-8" rx="9" ry="8"/><ellipse cx="-14" cy="-14" rx="10" ry="9"/>
      </g>
      <g fill="#4a6b32" opacity="0.7">
        <ellipse cx="-146" cy="-88" rx="7" ry="4" transform="rotate(24 -146 -88)"/>
        <ellipse cx="112" cy="-96" rx="7" ry="4" transform="rotate(-14 112 -96)"/>
        <ellipse cx="118" cy="104" rx="7" ry="4" transform="rotate(32 118 104)"/>
      </g>
    </g>""")


def a_toppings(t, d, c):
    """Pizza Toppings — the ingredient spread."""
    items = [
        ('<ellipse cx="-96" cy="-104" rx="40" ry="36" fill="#c9553f"/><ellipse cx="-104" cy="-114" rx="9" ry="8" fill="#7d2a26" opacity="0.55"/>', 0),
        ('<ellipse cx="86" cy="-128" rx="38" ry="35" fill="#c9553f"/><ellipse cx="78" cy="-138" rx="9" ry="8" fill="#7d2a26" opacity="0.55"/>', 0),
        ('<ellipse cx="158" cy="-14" rx="41" ry="38" fill="#c9553f"/><ellipse cx="150" cy="-24" rx="9" ry="8" fill="#7d2a26" opacity="0.55"/>', 0),
        ('<ellipse cx="-148" cy="74" rx="38" ry="35" fill="#c9553f"/>', 0),
        ('<ellipse cx="34" cy="128" rx="39" ry="36" fill="#c9553f"/>', 0),
        ('<ellipse cx="-40" cy="20" rx="26" ry="18" fill="#8a5a33" transform="rotate(-18 -40 20)"/>', 0),
        ('<ellipse cx="60" cy="60" rx="24" ry="17" fill="#a9713f" transform="rotate(14 60 60)"/>', 0),
        ('<ellipse cx="-160" cy="-24" rx="24" ry="17" fill="#8a5a33" transform="rotate(24 -160 -24)"/>', 0),
        ('<path d="M-40 -10 A 40 34 0 0 1 40 -10 Z" fill="#d8c3a4"/><rect x="-6" y="-10" width="12" height="26" rx="6" fill="#e6dccb"/>', 0),
        ('<path d="M30 -46 A 34 29 0 0 1 98 -46 Z" fill="#d8c3a4"/><rect x="58" y="-46" width="10" height="22" rx="5" fill="#e6dccb"/>', 0),
        ('<path d="M-140 92 q 40 -26 82 -6 q -34 26 -82 6 Z" fill="#7ba64a"/>', 0),
        ('<path d="M76 104 q 40 -26 82 -6 q -34 26 -82 6 Z" fill="#7ba64a"/>', 0),
        ('<path d="M-120 -80 q 38 -24 78 -4 q -32 24 -78 4 Z" fill="#d8563f"/>', 0),
        ('<path d="M92 -92 q 36 -22 72 -2 q -30 22 -72 2 Z" fill="#d8563f"/>', 0),
        ('<ellipse cx="150" cy="72" rx="30" ry="26" fill="none" stroke="#e0b83a" stroke-width="11"/>', 0),
        ('<ellipse cx="-190" cy="96" rx="27" ry="23" fill="none" stroke="#e0b83a" stroke-width="11"/>', 0),
        ('<ellipse cx="182" cy="30" rx="32" ry="28" fill="none" stroke="#d6c4e4" stroke-width="10"/>', 0),
        ('<ellipse cx="-56" cy="-142" rx="28" ry="24" fill="none" stroke="#d6c4e4" stroke-width="10"/>', 0),
        ('<ellipse cx="112" cy="150" rx="19" ry="22" fill="#3f4a33"/>', 0),
        ('<ellipse cx="46" cy="164" rx="17" ry="20" fill="#3f4a33"/>', 0),
        ('<ellipse cx="-190" cy="-4" rx="16" ry="19" fill="#3f4a33"/>', 0),
        ('<ellipse cx="-20" cy="176" rx="30" ry="16" fill="#3f6b34" transform="rotate(-14 -20 176)"/>', 0),
    ]
    bodies = "\n      ".join(i[0] for i in items)
    return shell(t, f"""{plate(600, 428, 372, 316)}
    <g>
      {bodies}
    </g>""")


# --------------------------------------------------------------------------
# item -> archetype table
# --------------------------------------------------------------------------

ARCHETYPES = {
    "garlic-breaded-provolone-sticks": a_provolone,
    "basket-of-hushpuppies": a_hushpuppies,
    "beer-battered-onion-rings": a_onion_rings,
    "chicken-fingers": a_fingers,
    "gyro-fries": a_gyro_fries,
    "hot-pepper-cheese-balls": a_cheese_balls,
    "loaded-potato-skins": a_potato_skins,
    "loaded-pounder-basket": a_pounder,
    "shrimp-basket": a_shrimp,
    "soft-bavarian-pretzels": a_pretzels,
    "the-pounder-basket": a_pounder,
    "zucchini-planks": a_zucchini,

    "bacon-cheeseburger": a_burger,
    "cheeseburger": a_burger,
    "hamburger": a_burger,

    "buffalo-chicken-cheese-eggrolls": a_eggroll,
    "pepperoni-cheese-eggrolls": a_eggroll,

    "breaded-chicken-sandwich": a_hoagie,
    "grilled-chicken-sandwich": a_hoagie,
    "gyro": a_hoagie,
    "homemade-meatball-hoagie": a_hoagie,
    "hot-sausage-hoagie": a_hoagie,
    "italian-hoagie": a_hoagie,
    "jumbo-cod-sandwich": a_hoagie,
    "philly-cheese-steak": a_hoagie,
    "veggie-hoagie": a_hoagie,

    "breaded-chicken-salad": a_salad,
    "grilled-chicken-salad": a_salad,
    "grilled-flat-iron-steak-salad": a_salad,
    "gyro-salad": a_salad,
    "tossed-salad": a_salad,

    "crispy-breaded-chicken-stromboli": a_stromboli,
    "homemade-meatball-stromboli": a_stromboli,
    "hot-sausage-cheese-stromboli": a_stromboli,
    "pepperoni-cheese-stromboli": a_stromboli,
    "philly-cheese-steak-stromboli": a_stromboli,

    "boneless-wings": a_wings,
    "carols-burnt-spicy-bbq-wings": a_wings,
    "spicy-breaded-wing-dings": a_wings,
    "whole-jumbo-wings": a_wings,
    "wing-flavors": a_wing_flavors,

    "toppings": a_toppings,
    "large": a_pizza_pie,
    "medium": a_pizza_pie,
    "small": a_pizza_pie,
    "ultimate-pepperoni": a_ultimate_pepperoni,
}

# per-item palette overrides, keyed by slug. (c1, c2) is passed to the
# archetype as `c`; archetypes that need a second colour read it from the item.
PALETTE = {
    "garlic-breaded-provolone-sticks": "#e3ac4e",
    "basket-of-hushpuppies": "#e3ac4e",
    "beer-battered-onion-rings": "#e8bc66",
    "chicken-fingers": "#e6b455",
    "gyro-fries": "#c9a06a",
    "hot-pepper-cheese-balls": "#e3ac4e",
    "loaded-potato-skins": "#f2d489",
    "loaded-pounder-basket": "#e6c98d",
    "shrimp-basket": "#e8bb6a",
    "soft-bavarian-pretzels": "#dfae5c",
    "the-pounder-basket": "#e0a94a",
    "zucchini-planks": "#dcb262",
    "bacon-cheeseburger": "#7a4126",
    "cheeseburger": "#7a4126",
    "hamburger": "#7a4126",
    "buffalo-chicken-cheese-eggrolls": "#df9a45",
    "pepperoni-cheese-eggrolls": "#e2ab55",
    "crispy-breaded-chicken-stromboli": "#e2b463",
    "homemade-meatball-stromboli": "#e2b463",
    "hot-sausage-cheese-stromboli": "#e2b463",
    "pepperoni-cheese-stromboli": "#e2b463",
    "philly-cheese-steak-stromboli": "#e2b463",
    "boneless-wings": "#c4693a",
    "carols-burnt-spicy-bbq-wings": "#a5522a",
    "spicy-breaded-wing-dings": "#c4693a",
    "whole-jumbo-wings": "#c4693a",
    "breaded-chicken-salad": "#e0b25a",
    "grilled-chicken-salad": "#c08a4a",
    "grilled-flat-iron-steak-salad": "#8f5a30",
    "gyro-salad": "#c9a06a",
    "tossed-salad": "#4a7a34",
    "breaded-chicken-sandwich": "#e6b455",
    "grilled-chicken-sandwich": "#c08a4a",
    "gyro": "#c9a06a",
    "homemade-meatball-hoagie": "#c9a06a",
    "hot-sausage-hoagie": "#a35a2e",
    "italian-hoagie": "#c8503f",
    "jumbo-cod-sandwich": "#f2ead6",
    "philly-cheese-steak": "#8f4a26",
    "veggie-hoagie": "#4a7a34",
    "toppings": "#f2d489",
    "large": "#f0cf87",
    "medium": "#f0cf87",
    "small": "#f0cf87",
    "ultimate-pepperoni": "#c9553f",
    "wing-flavors": "#c8402f",
}

# short caption under the dish, per section, to fill the plate area
CAPTIONS = {
    "appetizers": "APPETIZERS",
    "burgers": "BURGERS",
    "eggrolls": "EGGROLLS",
    "hoagies-sandwiches": "SANDWICHES",
    "salads": "SALADS",
    "stromboli": "STROMBOLI",
    "wings": "WINGS",
}


def read_items():
    items = []
    for dirpath, dirnames, filenames in os.walk(CONTENT):
        if os.path.basename(dirpath) == "specials":
            continue
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, CONTENT)
            if fn == "_index.md" or rel in ("index.md", "menu.md", "_index.md"):
                continue
            txt = open(path).read()
            m = re.match(r"\+\+\+(.*?)\+\+\+", txt, re.S)
            if not m:
                continue
            fm = dict(re.findall(r'^(\w+)\s*=\s*"?(.*?)"?\s*$', m.group(1), re.M))
            if "title" not in fm:
                continue
            # For a bundle (foo/index.md) the slug is the *parent* directory
            # name; for a flat file (foo.md) it is the file stem. The section
            # is the section directory, i.e. the parent of the bundle.
            if fn == "index.md":
                slug = os.path.basename(dirpath)
                section = os.path.basename(os.path.dirname(dirpath))
            else:
                slug = fn[:-3]
                section = os.path.basename(dirpath)
            items.append({
                "section": section, "slug": slug, "path": path,
                "title": fm["title"], "desc": fm.get("description", ""),
            })
    return sorted(items, key=lambda i: (i["section"], i["slug"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg-only", action="store_true",
                    help="write the source SVG into the bundle and stop "
                         "(item art is normally shipped as PNG only)")
    ap.add_argument("--png-only", action="store_true",
                    help="rasterise only; the SVG is written to a temp file "
                         "and never lands in the bundle (default)")
    ap.add_argument("--only", help="limit to one slug")
    args = ap.parse_args()
    if args.svg_only and args.png_only:
        ap.error("--svg-only and --png-only are mutually exclusive")

    items = read_items()
    if args.only:
        items = [i for i in items if i["slug"] == args.only]

    made, skipped = [], []
    for it in items:
        slug, title = it["slug"], it["title"]
        fn = ARCHETYPES.get(slug)
        if fn is None:
            skipped.append(slug)
            continue
        colour = PALETTE.get(slug, "#e0a94a")
        caption = CAPTIONS.get(it["section"], "")

        svg = fn(title, caption, colour)

        # auto-fit the chalk label
        size, spacing = label_size(title)
        svg = svg.replace('font-size="42" letter-spacing="2"',
                          f'font-size="{size}" letter-spacing="{spacing}"')

        bundle = os.path.join(CONTENT, it["section"], slug)
        os.makedirs(bundle, exist_ok=True)

        png_path = os.path.join(bundle, f"photo-{slug}-hero.png")

        if args.svg_only:
            # Debugging aid: keep the vector source beside the raster so it can
            # be opened in a browser. Item art is shipped as PNG only, so this
            # is opt-in and never the default.
            with open(os.path.join(bundle, f"photo-{slug}-hero.svg"), "w") as fh:
                fh.write(svg)
        else:
            # The SVG is an intermediate, not a deliverable. Rasterising needs a
            # file on disk for cairosvg, so use a temp file and let it go —
            # otherwise every regeneration drops 46 stray .svg files into the
            # bundles, where they would shadow the PNG under photoGlob.
            with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as tmp:
                tmp.write(svg)
                tmp_path = tmp.name
            try:
                cairosvg.svg2png(
                    url=tmp_path, write_to=png_path,
                    output_width=OUT_W, output_height=OUT_H)
            finally:
                os.unlink(tmp_path)
        made.append((slug, it["section"]))

    print(f"generated {len(made)} item images")
    if skipped:
        print("NO ARCHETYPE (skipped):", ", ".join(skipped))
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
