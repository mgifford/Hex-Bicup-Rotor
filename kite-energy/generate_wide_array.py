#!/usr/bin/env python3
"""Generates wide-array.svg: a solarpunk-styled TOP-DOWN (plan) view of a
wide array of parallel ▲o▲o▲ chains — several rows of alternating
tetrahedron/rotor units, offset brick-fashion so rotors in one row sit
staggered relative to the row above/below, keeping clear air around each
rotor rather than lining them up behind each other.

This is the third of three arrangement options considered in
kite-energy/README.md's "Which arrangement?" section — see that file for
the reasoning: a single LINEAR chain (chain-array.svg) has poor aspect
ratio for kite lift (real AWE kites are wide, not needle-thin, since
crosswind power scales with sail area) and poor resistance to
twisting/bending loads (no lateral triangulation between rows). A wide
array fixes both while keeping the same clear-air rotor placement.

Drawn as a top-down plan view (not a 3D oblique render like
chain-array.svg or lattice-array.svg) because a 2D grid of rows is much
easier to read from directly above than from an oblique angle — this is
a layout diagram, not a flight-attitude illustration.

Geometry: each tetrahedron's footprint (as seen from above) is the same
verified vertical-edge orientation used in generate_chain_array.py — a
vertical edge (not shown in plan view, since it's the axis pointing
toward the viewer) with two "back" vertices swept to the sides, distance
`depth` = sqrt(3/4)*cos(asin(1/sqrt(3))) from center. Row spacing is
verified to clear the tetrahedra's own footprint width with margin.
"""
import math
from pathlib import Path

edge = 1.0
r = math.sqrt(0.75)
theta = math.asin(1 / (2 * r))
depth = r * math.cos(theta)
half_w = r * math.sin(theta)

SPACING = 2.0          # tetra center-to-center spacing along a row
ROW_SPACING = 1.2       # spacing between rows — verified > 2*half_w (1.0) with margin
N_TETRA_PER_ROW = 3
N_ROWS = 3

rows = []
for row in range(N_ROWS):
    row_offset = (SPACING / 2) if row % 2 == 1 else 0
    centers = [row_offset + i * SPACING for i in range(N_TETRA_PER_ROW)]
    rows.append(centers)

# ── Screen layout (direct 2D plan view, no projection needed) ────────
W, H = 780, 480
TITLE_H = 60
DRAW_TOP = TITLE_H + 20
PAD_X = 60

all_x = [c for row in rows for c in row]
minx, maxx = min(all_x) - depth, max(all_x) + depth
draw_w_units = maxx - minx
draw_h_units = (N_ROWS - 1) * ROW_SPACING + 1.0  # +1.0 for tetra full y-extent

avail_w = W - 2 * PAD_X
avail_h = 240
scale = min(avail_w / draw_w_units, avail_h / draw_h_units)
x_offset = (W - draw_w_units * scale) / 2


def to_screen(x, y):
    sx = (x - minx) * scale + x_offset
    sy = (y - (-((N_ROWS - 1) * ROW_SPACING) / 2 - 0.5)) * scale + DRAW_TOP
    return (round(sx, 2), round(sy, 2))


face_out = []
strut_out = []
joint_out = []
rotor_out = []
face_classes = ["cell-face-a", "cell-face-b"]

for ri, centers in enumerate(rows):
    row_y = -((N_ROWS - 1) * ROW_SPACING) / 2 + ri * ROW_SPACING
    for ci, cx in enumerate(centers):
        mirror = (ri + ci) % 2 == 1
        d = depth if not mirror else -depth
        # plan-view triangle: center point (the vertical edge, seen end-on)
        # and two back vertices swept to the sides
        center_pt = to_screen(cx, row_y)
        b1 = to_screen(cx + d, row_y + half_w)
        b2 = to_screen(cx + d, row_y - half_w)
        cls = face_classes[(ri + ci) % 2]
        face_out.append(
            f'<polygon class="{cls}" points="{center_pt[0]},{center_pt[1]} {b1[0]},{b1[1]} {b2[0]},{b2[1]}"/>'
        )
        strut_out.append(
            f'<path class="strut" d="M{center_pt[0]},{center_pt[1]} L{b1[0]},{b1[1]} '
            f'M{center_pt[0]},{center_pt[1]} L{b2[0]},{b2[1]} M{b1[0]},{b1[1]} L{b2[0]},{b2[1]}"/>'
        )
        joint_out.extend([center_pt, b1, b2])
        # rotor between this tetra and the next one in the row
        if ci < len(centers) - 1:
            rcx = (cx + centers[ci + 1]) / 2
            rpt = to_screen(rcx, row_y)
            rotor_out.append(rpt)

rotor_svgs = [
    f'<circle class="rotor-icon" cx="{x}" cy="{y}" r="9"/>'
    f'<circle class="rotor-icon-core" cx="{x}" cy="{y}" r="3"/>'
    for x, y in rotor_out
]

GROUND_Y = H - 150
GS_X = 40
tether_anchor = to_screen(rows[N_ROWS // 2][0] - depth, (-((N_ROWS - 1) * ROW_SPACING) / 2))

SVG = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" role="img"
     aria-label="Top-down plan view of a wide array of parallel alternating tetrahedron/rotor chains, offset brick-fashion between rows, tethered to a ground station."
     style="max-width:100%;height:auto;">
  <title>Wide array — top-down plan view, exploratory illustration</title>
  <style>
    svg {{ background: #fdf6e3; }}
    .sky-grad {{ fill: #fbe9c9; }}
    .sun {{ fill: #f4b942; opacity: 0.85; }}
    .cell-face-a {{ fill: #e8a24a; fill-opacity: 0.55; stroke: none; }}
    .cell-face-b {{ fill: #5fae82; fill-opacity: 0.55; stroke: none; }}
    .strut {{ stroke: #6b4a2f; stroke-width: 1.4; fill: none; }}
    .joint {{ fill: #3f6b4f; stroke: #274a35; stroke-width: 0.8; }}
    .rotor-icon {{ fill: #dd6b4a; fill-opacity: 0.85; stroke: #7a3620; stroke-width: 1; }}
    .rotor-icon-core {{ fill: #274a35; }}
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

  <text class="label-bold" x="{W/2}" y="26" text-anchor="middle">Wide array: parallel chains, top-down view</text>
  <text class="callout" x="{W/2}" y="44" text-anchor="middle">Rows offset like bricklaying, so every rotor keeps clear air on both sides</text>

  {"".join(face_out)}
  {"".join(strut_out)}
  {"".join(f'<circle class="joint" cx="{x}" cy="{y}" r="3"/>' for x, y in joint_out)}
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

target = Path(__file__).resolve().parent / "wide-array.svg"
target.write_text(SVG)
print(f"wrote {target}")
