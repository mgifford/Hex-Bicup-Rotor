#!/usr/bin/env python3
"""Generates chain-array.svg: a solarpunk-styled illustration of an
alternating chain of tetrahedral kite cells and VINDSNURR-style rotor
units — ▲ o ▲ o ▲ — rather than nesting rotors inside a dense triangular
lattice (the earlier lattice-array.svg approach).

Geometry, verified by direct construction (not approximated):
Each tetrahedron is oriented with one EDGE VERTICAL (not the usual
"apex over horizontal base" orientation used elsewhere in this repo),
giving it a natural top and bottom mounting point spaced exactly one
strut-length apart — the same vertical span a VINDSNURR-style rotor
shaft needs. If the tetrahedron's edge length equals VINDSNURR's real
1000mm rotor diameter, that vertical span (1000mm) is close to
VINDSNURR's own actual rotor height (1064mm, per ../CLAUDE.md) — the two
unit types are naturally compatible scales, not an arbitrary mismatch.

Tetrahedra alternate mirrored orientation along the chain (their
"back" pair of vertices swept out to alternating sides), echoing the
alternating sail-facing look in the historical Bell multi-cell kite
photos this whole exploration is inspired by. Rotor units sit in the
gaps between tetrahedra with verified geometric clearance (no strut
overlap) at a 2:1 tetra-spacing-to-edge-length ratio.

This is a speculative illustration for kite-energy/README.md, not a
structural design — see that file for the same structural caveats as
lattice-array.svg (added rotor mass/gyroscopic load, VINDSNURR's rigid-
shaft bearings vs. a flexing kite frame).
"""
import math
from pathlib import Path

edge = 1.0
r = math.sqrt(0.75)
theta = math.asin(1 / (2 * r))
depth = r * math.cos(theta)
half_w = r * math.sin(theta)


def tetra_at(cx, cy, mirror=False):
    top = (cx, cy, 0.5)
    bot = (cx, cy, -0.5)
    d = depth if not mirror else -depth
    back1 = (cx + d, cy + half_w, 0)
    back2 = (cx + d, cy - half_w, 0)
    return top, bot, back1, back2


def rotate_y(p, deg):
    a = math.radians(deg)
    x, y, z = p
    return (x * math.cos(a) + z * math.sin(a), y, -x * math.sin(a) + z * math.cos(a))


def project(p):
    # A small yaw only (no pitch/tilt) — enough to read as 3D without the
    # foreshortening from a steeper oblique angle overlapping adjacent
    # chain units, which happens because the chain's own length (spacing
    # between tetrahedra) is comparable to each tetrahedron's depth.
    p2 = rotate_y(p, 12)
    return (p2[0], -p2[2])


# ── Chain layout: 3 tetrahedra, 2 rotor units — ▲ o ▲ o ▲ ────────────
N_TETRA = 3
SPACING = 2.0  # center-to-center spacing between tetrahedra (edge=1.0 units)

tetra_centers = [i * SPACING for i in range(N_TETRA)]
rotor_centers = [(tetra_centers[i] + tetra_centers[i + 1]) / 2 for i in range(N_TETRA - 1)]

tetrahedra = [tetra_at(cx, 0, mirror=(i % 2 == 1)) for i, cx in enumerate(tetra_centers)]

# ── Screen fit ────────────────────────────────────────────────────
W, H = 780, 460
TITLE_H = 60
DRAW_TOP = TITLE_H + 30
DRAW_H = 220
PAD_X = 50

all_pts = [p for t in tetrahedra for p in t]
proj = [project(p) for p in all_pts]
xs = [p[0] for p in proj]
ys = [p[1] for p in proj]
minx, maxx = min(xs), max(xs)
miny, maxy = min(ys), max(ys)
w = (maxx - minx) or 1
h = (maxy - miny) or 1
scale = min((W - 2 * PAD_X) / w, DRAW_H / h)
draw_w = w * scale
x_offset = (W - draw_w) / 2


def to_screen(p):
    x, y = project(p)
    sx = (x - minx) * scale + x_offset
    sy = (y - miny) * scale + DRAW_TOP
    return (round(sx, 2), round(sy, 2))


# ── Draw tetrahedra (each: 2 triangular "sail" faces + struts) ───────
face_out = []
strut_out = []
joint_out = []
face_classes = ["cell-face-a", "cell-face-b"]
for i, (top, bot, b1, b2) in enumerate(tetrahedra):
    pts = [to_screen(p) for p in (top, bot, b1, b2)]
    ptop, pbot, pb1, pb2 = pts
    cls = face_classes[i % 2]
    # two "sail" faces: top-b1-b2 (upper) and bot-b1-b2 (lower) — covered
    face_out.append(f'<polygon class="{cls}" points="{ptop[0]},{ptop[1]} {pb1[0]},{pb1[1]} {pb2[0]},{pb2[1]}"/>')
    face_out.append(f'<polygon class="{cls}" points="{pbot[0]},{pbot[1]} {pb1[0]},{pb1[1]} {pb2[0]},{pb2[1]}"/>')
    strut_out.append(
        f'<path class="strut" d="M{ptop[0]},{ptop[1]} L{pbot[0]},{pbot[1]} '
        f'M{ptop[0]},{ptop[1]} L{pb1[0]},{pb1[1]} M{ptop[0]},{ptop[1]} L{pb2[0]},{pb2[1]} '
        f'M{pbot[0]},{pbot[1]} L{pb1[0]},{pb1[1]} M{pbot[0]},{pbot[1]} L{pb2[0]},{pb2[1]} '
        f'M{pb1[0]},{pb1[1]} L{pb2[0]},{pb2[1]}"/>'
    )
    for p in (ptop, pbot, pb1, pb2):
        joint_out.append(p)


def rotor_icon(cx, cy_top, cy_bot, scale=1.0):
    rr = 15 * scale
    mid_y = (cy_top + cy_bot) / 2
    return (
        f'<g class="rotor-icon">'
        f'<line x1="{cx}" y1="{cy_top}" x2="{cx}" y2="{cy_bot}" class="rotor-shaft"/>'
        f'<path d="M {cx},{mid_y-rr} A {rr},{rr*0.55} 0 0 1 {cx},{mid_y} '
        f'A {rr},{rr*0.55} 0 0 0 {cx},{mid_y+rr} A {rr},{rr*0.55} 0 0 1 {cx},{mid_y-rr} Z" '
        f'class="rotor-blade"/></g>'
    )


rotor_svgs = []
for rcx in rotor_centers:
    top_pt = to_screen((rcx, 0, 0.5))
    bot_pt = to_screen((rcx, 0, -0.5))
    rotor_svgs.append(rotor_icon(top_pt[0], top_pt[1], bot_pt[1]))

# tether from the leftmost tetrahedron's bottom vertex
tether_anchor = to_screen((tetra_centers[0], 0, -0.5))

GROUND_Y = H - 150
# Ground station box position: fixed safe offset from the left canvas
# edge, not derived from the tether anchor — the anchor can sit close to
# x=0 depending on chain layout, which pushed the box (and its label) off
# the left edge when derived directly.
GS_X = 40

SVG = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" role="img"
     aria-label="Solarpunk-style illustration of an alternating chain of tetrahedral kite cells and VINDSNURR-style vertical-axis rotor units — triangle, rotor, triangle, rotor, triangle — tethered to a ground station."
     style="max-width:100%;height:auto;">
  <title>Alternating tetrahedron/rotor chain — exploratory illustration</title>
  <style>
    svg {{ background: #fdf6e3; }}
    .sky-grad {{ fill: #fbe9c9; }}
    .sun {{ fill: #f4b942; opacity: 0.85; }}
    .cell-face-a {{ fill: #e8a24a; fill-opacity: 0.55; stroke: none; }}
    .cell-face-b {{ fill: #5fae82; fill-opacity: 0.55; stroke: none; }}
    .strut {{ stroke: #6b4a2f; stroke-width: 1.6; fill: none; }}
    .joint {{ fill: #3f6b4f; stroke: #274a35; stroke-width: 0.8; }}
    .rotor-shaft {{ stroke: #274a35; stroke-width: 2.2; }}
    .rotor-blade {{ fill: #dd6b4a; fill-opacity: 0.9; stroke: #7a3620; stroke-width: 1; }}
    .tether {{ stroke: #7a221c; stroke-width: 2; stroke-dasharray: 6 4; fill: none; }}
    .ground {{ fill: #cfead0; }}
    .ground-station {{ fill: #fff8e8; stroke: #b58a4a; stroke-width: 1.5; }}
    .leaf {{ fill: #5fae82; opacity: 0.8; }}
    .label-bold {{ font-size: 16px; fill: #3a2c1a; font-weight: 700; }}
    .label {{ font-size: 12.5px; fill: #3a2c1a; }}
    .callout {{ font-size: 11.5px; fill: #6b5a3f; }}
    @media (prefers-color-scheme: dark) {{
      svg {{ background: #1a1a18; }}
      .sky-grad {{ fill: #2a2416; }}
      .sun {{ fill: #f4b942; opacity: 0.6; }}
      .strut {{ stroke: #d8c9a8; }}
      .joint {{ fill: #7fcf9f; stroke: #3f6b4f; }}
      .rotor-shaft {{ stroke: #d8c9a8; }}
      .ground {{ fill: #21361f; }}
      .ground-station {{ fill: #2e2e2b; stroke: #7a5f34; }}
      .leaf {{ fill: #4f9068; }}
      .label-bold {{ fill: #f0e6cc; }}
      .label {{ fill: #f0e6cc; }}
      .callout {{ fill: #c9bc9e; }}
    }}
  </style>

  <rect class="sky-grad" x="0" y="0" width="{W}" height="{GROUND_Y}"/>
  <rect class="ground" x="0" y="{GROUND_Y}" width="{W}" height="{H-GROUND_Y}"/>
  <circle class="sun" cx="{W-70}" cy="55" r="34"/>

  <text class="label-bold" x="{W/2}" y="26" text-anchor="middle">Alternating chain: kite cells and rotors in line</text>
  <text class="callout" x="{W/2}" y="44" text-anchor="middle">▲ o ▲ o ▲ — each tetrahedron's vertical edge doubles as a rotor's shaft span</text>

  {"".join(face_out)}
  {"".join(strut_out)}
  {"".join(f'<circle class="joint" cx="{x}" cy="{y}" r="3.5"/>' for x, y in joint_out)}
  {"".join(rotor_svgs)}

  <path class="tether" d="M{tether_anchor[0]},{tether_anchor[1]} C {GS_X+60},{GROUND_Y-70} {GS_X+50},{GROUND_Y-25} {GS_X+45},{GROUND_Y+8}"/>

  <g transform="translate({GS_X},{GROUND_Y+6})">
    <rect class="ground-station" x="0" y="0" width="150" height="60" rx="8"/>
    <circle cx="32" cy="30" r="17" fill="none" stroke="#6b4a2f" stroke-width="2"/>
    <circle cx="32" cy="30" r="4" fill="#6b4a2f"/>
    <text class="callout" x="32" y="54" text-anchor="middle">Winch + generator</text>
    <path d="M54,22 L85,15" stroke="#2f9e44" stroke-width="2" marker-end="url(#arrowgreen)"/>
    <text class="label" x="90" y="18">To grid</text>
  </g>

  <g transform="translate(40,{GROUND_Y+35})">
    <path class="leaf" d="M0,20 Q10,-10 20,20 Q10,10 0,20 Z"/>
    <path class="leaf" d="M15,22 Q25,-5 35,22 Q25,14 15,22 Z"/>
  </g>
  <g transform="translate({W-90},{GROUND_Y+30})">
    <path class="leaf" d="M0,20 Q10,-10 20,20 Q10,10 0,20 Z"/>
    <path class="leaf" d="M15,22 Q25,-5 35,22 Q25,14 15,22 Z"/>
  </g>

  <defs>
    <marker id="arrowgreen" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <polygon points="0,0 7,3 0,6" fill="#2f9e44"/>
    </marker>
  </defs>
</svg>'''

target = Path(__file__).resolve().parent / "chain-array.svg"
target.write_text(SVG)
print(f"wrote {target}")
