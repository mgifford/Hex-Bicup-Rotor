#!/usr/bin/env python3
"""Generates lattice-array.svg: a solarpunk-styled illustration of a large
multi-cell tetrahedral kite lattice (scaled up from the same 4-layer,
20-cell geometry used throughout kite-corners/) with small VINDSNURR-style
rotor icons placed at real vertical inter-layer joints — the natural shaft
locations where one layer's apex is the same physical point as the layer
above's base corner (already verified in kite-corners/generate_diagram.py).

This is a speculative illustration for kite-energy/README.md, not a
structural design. See that file's "Best arrangement of kite elements to
support circular turbine elements" section for the open questions this
doesn't resolve (whether a spinning rotor mass could actually be carried
at these joints without redesigning the frame).

Geometry is identical to kite-corners/generate_diagram.py's 4-layer,
20-cell assembly (10+6+3+1 unit tetrahedra, each layer's base triangle
anchored exactly to the layer below's apex points) — not re-derived here,
just reused, since it's already verified.
"""
import math
from collections import defaultdict
from pathlib import Path

s3 = math.sqrt(3) / 2
tetra_h = math.sqrt(2 / 3)


def up_triangle_2d(col, row, ox=0.0, oy=0.0):
    y0 = row * s3 + oy
    y1 = (row + 1) * s3 + oy
    p0 = (col + row * 0.5 + ox, y0)
    p1 = (col + 1 + row * 0.5 + ox, y0)
    p2 = (col + 0.5 + row * 0.5 + ox, y1)
    return p0, p1, p2


def centroid2(p0, p1, p2):
    return ((p0[0] + p1[0] + p2[0]) / 3, (p0[1] + p1[1] + p2[1]) / 3)


def build_layer(cell_rows, z0, ox=0.0, oy=0.0):
    cells = []
    for row, ncols in cell_rows:
        for col in range(ncols):
            p0, p1, p2 = up_triangle_2d(col, row, ox, oy)
            base3d = [(p0[0], p0[1], z0), (p1[0], p1[1], z0), (p2[0], p2[1], z0)]
            cx, cy = centroid2(p0, p1, p2)
            apex3d = (cx, cy, z0 + tetra_h)
            cells.append((base3d, apex3d))
    return cells


layer0 = build_layer([(0, 4), (1, 3), (2, 2), (3, 1)], z0=0, ox=0.0, oy=0.0)
l1_ox, l1_oy = layer0[0][1][0], layer0[0][1][1]
layer1 = build_layer([(0, 3), (1, 2), (2, 1)], z0=tetra_h, ox=l1_ox, oy=l1_oy)
l2_ox, l2_oy = layer1[0][1][0], layer1[0][1][1]
layer2 = build_layer([(0, 2), (1, 1)], z0=2 * tetra_h, ox=l2_ox, oy=l2_oy)
l3_ox, l3_oy = layer2[0][1][0], layer2[0][1][1]
layer3 = build_layer([(0, 1)], z0=3 * tetra_h, ox=l3_ox, oy=l3_oy)
all_cells = layer0 + layer1 + layer2 + layer3


def key(p):
    return (round(p[0], 4), round(p[1], 4), round(p[2], 4))


def rotate_x(p, deg):
    a = math.radians(deg)
    x, y, z = p
    return (x, y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a))


def project_front(p):
    p2 = rotate_x(p, -12)
    return (p2[0], -p2[2] - p2[1] * 0.15)


def vertical_joints(lower, upper):
    lower_apex = {key(a): a for b, a in lower}
    upper_base = {key(v): v for b, a in upper for v in b}
    shared = set(lower_apex) & set(upper_base)
    return [lower_apex[k] for k in shared]


rotor_bays = (
    vertical_joints(layer0, layer1)
    + vertical_joints(layer1, layer2)
    + vertical_joints(layer2, layer3)
)

# ── Layout ──────────────────────────────────────────────────────
W, H = 720, 560
TITLE_H = 60          # reserved band at the top for title text, ABOVE the drawing
LATTICE_TOP = TITLE_H + 20
LATTICE_H = 260        # vertical space the lattice itself is scaled to fill
PAD_X = 60

all_pts = []
for b, a in all_cells:
    all_pts += list(b) + [a]

proj = [project_front(p) for p in all_pts]
xs = [p[0] for p in proj]
ys = [p[1] for p in proj]
minx, maxx = min(xs), max(xs)
miny, maxy = min(ys), max(ys)
w = (maxx - minx) or 1
h = (maxy - miny) or 1
scale = min((W - 2 * PAD_X) / w, LATTICE_H / h)
draw_w = w * scale
x_offset = (W - draw_w) / 2


def to_screen(p):
    x, y = project_front(p)
    sx = (x - minx) * scale + x_offset
    sy = (y - miny) * scale + LATTICE_TOP
    return (round(sx, 2), round(sy, 2))


def depth(p):
    return rotate_x(p, -12)[1]


scored = []
for b, a in all_cells:
    d = sum(depth(p) for p in list(b) + [a]) / 4
    scored.append((d, b, a))
scored.sort(key=lambda t: t[0])

face_out = []
strut_out = []
joint_out = []
seen = set()
face_classes = ["cell-face-a", "cell-face-b"]
for i, (d, b, a) in enumerate(scored):
    pb = [to_screen(v) for v in b]
    pa = to_screen(a)
    cls = face_classes[i % 2]
    pts = " ".join(f"{x},{y}" for x, y in pb)
    face_out.append(f'<polygon class="{cls}" points="{pts}"/>')
    strut_out.append(
        f'<path class="strut" d="M{pb[0][0]},{pb[0][1]} L{pb[1][0]},{pb[1][1]} L{pb[2][0]},{pb[2][1]} Z '
        f'M{pb[0][0]},{pb[0][1]} L{pa[0]},{pa[1]} M{pb[1][0]},{pb[1][1]} L{pa[0]},{pa[1]} M{pb[2][0]},{pb[2][1]} L{pa[0]},{pa[1]}"/>'
    )
    for v in list(b) + [a]:
        k = key(v)
        if k in seen:
            continue
        seen.add(k)
        sx, sy = to_screen(v)
        joint_out.append((sx, sy))


def rotor_icon(cx, cy, scale=1.0):
    r = 11 * scale
    return (
        f'<g class="rotor-icon" transform="translate({cx},{cy})">'
        f'<line x1="0" y1="{-r-4}" x2="0" y2="{r+4}" class="rotor-shaft"/>'
        f'<path d="M 0,{-r} A {r},{r*0.6} 0 0 1 0,0 A {r},{r*0.6} 0 0 0 0,{r} '
        f'A {r},{r*0.6} 0 0 1 0,{-r} Z" class="rotor-blade"/></g>'
    )


rotor_svgs = [rotor_icon(*to_screen(j), 0.85) for j in rotor_bays]

lattice_bottom_y = max(y for x, y in (to_screen(p) for p in all_pts))
bottom_pts = [to_screen(p) for p in all_pts if abs(to_screen(p)[1] - lattice_bottom_y) < 3]
tether_x = min(x for x, y in bottom_pts)
tether_y = lattice_bottom_y

GROUND_Y = H - 160

SVG = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" role="img"
     aria-label="Solarpunk-style illustration of a large multi-cell tetrahedral kite lattice, similar in scale to Alexander Graham Bell's historical multi-cell kite arrays, with small VINDSNURR-style vertical-axis rotors nested in the open bays between layers, tethered to a small ground station.">
  <title>Tetrahedral kite lattice with embedded rotor array — exploratory illustration</title>
  <style>
    svg {{ background: #fdf6e3; }}
    .sky-grad {{ fill: #fbe9c9; }}
    .sun {{ fill: #f4b942; opacity: 0.85; }}
    .cell-face-a {{ fill: #e8a24a; fill-opacity: 0.55; stroke: none; }}
    .cell-face-b {{ fill: #5fae82; fill-opacity: 0.55; stroke: none; }}
    .strut {{ stroke: #6b4a2f; stroke-width: 1.3; fill: none; }}
    .joint {{ fill: #3f6b4f; stroke: #274a35; stroke-width: 0.8; }}
    .rotor-shaft {{ stroke: #274a35; stroke-width: 1.6; }}
    .rotor-blade {{ fill: #dd6b4a; fill-opacity: 0.9; stroke: #7a3620; stroke-width: 0.8; }}
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

  <text class="label-bold" x="{W/2}" y="26" text-anchor="middle">A kite lattice carrying its own wind rotors</text>
  <text class="callout" x="{W/2}" y="44" text-anchor="middle">Exploratory illustration — see kite-energy/README.md for the physics and open structural questions</text>

  {"".join(face_out)}
  {"".join(strut_out)}
  {"".join(f'<circle class="joint" cx="{x}" cy="{y}" r="3"/>' for x, y in joint_out)}
  {"".join(rotor_svgs)}

  <path class="tether" d="M{tether_x},{tether_y} C {tether_x-10},{GROUND_Y-70} {tether_x-20},{GROUND_Y-25} {tether_x-25},{GROUND_Y+8}"/>

  <g transform="translate({tether_x-95},{GROUND_Y+6})">
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

target = Path(__file__).resolve().parent / "lattice-array.svg"
target.write_text(SVG)
print(f"wrote {target}")
