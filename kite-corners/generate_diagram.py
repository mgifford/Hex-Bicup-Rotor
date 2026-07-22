#!/usr/bin/env python3
"""Generates a two-view (front + 3/4) schematic diagram of a 4-layer,
20-cell tetrahedral kite, with exterior/interior/triple joints colour-coded.

A 4-layer assembly (10 base + 6 + 3 + 1 unit tetrahedra) is used instead of
the smaller 3-layer, 10-cell kite because it is the smallest layer count
that actually contains a "triple" vertex (3 cells meeting at one point) —
the 3-layer kite only ever has exterior (1-cell) and interior (2-cell)
vertices. Vertex positions are computed from real 3D coordinates (each
layer's base triangle anchored exactly to the layer below's apex points),
not drawn freehand. See kite-corners/README.md for the full derivation,
including why a 5th vertex type (4+ cells meeting at a point) exists at
even deeper layer counts but is not covered by any hub file yet.

Writes two variants:
- kite-corners/kite-diagram.svg — a standalone file (own fixed colours +
  prefers-color-scheme), used by kite-corners/README.md via a normal
  markdown image link. Page CSS can never reach an externally-loaded
  image, so it can only follow the OS/browser dark-mode setting, not a
  site's manual light/dark toggle.
- kite-corners/kite-diagram-inline.svg — an HTML fragment using the
  VINDSNURR site's CSS variables (var(--text-main) etc.), meant to be
  pasted directly into docs/kite-comparison.html's markup so it follows
  the site's manual theme toggle exactly. Not written automatically to
  any HTML file — paste it in by hand after regenerating, since it lives
  inside a larger page.

Run this after changing the diagram; regenerate and re-paste both copies.
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


# Layer 0 (base) at the coordinate origin; each layer above offset so its
# base triangle lands EXACTLY on the layer below's apex points (real
# coincident 3D coordinates, verified — not a visual approximation).
layer0 = build_layer([(0, 4), (1, 3), (2, 2), (3, 1)], z0=0, ox=0.0, oy=0.0)
l1_ox, l1_oy = layer0[0][1][0], layer0[0][1][1]
layer1 = build_layer([(0, 3), (1, 2), (2, 1)], z0=tetra_h, ox=l1_ox, oy=l1_oy)
l2_ox, l2_oy = layer1[0][1][0], layer1[0][1][1]
layer2 = build_layer([(0, 2), (1, 1)], z0=2 * tetra_h, ox=l2_ox, oy=l2_oy)
l3_ox, l3_oy = layer2[0][1][0], layer2[0][1][1]
layer3 = build_layer([(0, 1)], z0=3 * tetra_h, ox=l3_ox, oy=l3_oy)

all_layers = [layer0, layer1, layer2, layer3]
all_cells = layer0 + layer1 + layer2 + layer3  # 10+6+3+1 = 20 cells total


def key(p):
    return (round(p[0], 4), round(p[1], 4), round(p[2], 4))


vert_count = defaultdict(int)
for b, a in all_cells:
    for v in b:
        vert_count[key(v)] += 1
    vert_count[key(a)] += 1


def joint_class(p):
    n = vert_count[key(p)]
    if n == 1:
        return "ext-joint"
    if n == 2:
        return "int-joint"
    if n == 3:
        return "triple-joint"
    return "unhandled-joint"  # 4+ cells meeting — no hub file covers this yet


def rotate_x(p, deg):
    a = math.radians(deg)
    x, y, z = p
    return (x, y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a))


def rotate_y(p, deg):
    a = math.radians(deg)
    x, y, z = p
    return (x * math.cos(a) + z * math.sin(a), y, -x * math.sin(a) + z * math.cos(a))


def project_front(p):
    p2 = rotate_x(p, -12)
    return (p2[0], -p2[2] - p2[1] * 0.15)


def project_34(p):
    p2 = rotate_y(p, 40)
    p2 = rotate_x(p2, -28)
    return (p2[0], -p2[2])


def fit_transform(cells, project_fn, target_w, target_h, pad=24):
    pts = []
    for b, a in cells:
        pts += [project_fn(p) for p in b]
        pts.append(project_fn(a))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    w = maxx - minx or 1
    h = maxy - miny or 1
    scale = min((target_w - 2 * pad) / w, (target_h - 2 * pad) / h)

    def to_screen(p):
        x, y = project_fn(p)
        sx = (x - minx) * scale + pad
        sy = (y - miny) * scale + pad
        return (round(sx, 2), round(sy, 2))

    return to_screen


VIEW_W, VIEW_H = 300, 260

to_screen_front = fit_transform(all_cells, project_front, VIEW_W, VIEW_H)
to_screen_34 = fit_transform(all_cells, project_34, VIEW_W, VIEW_H)


def front_depth(p):
    return rotate_x(p, -12)[1]


def rot34_depth(p):
    p2 = rotate_y(p, 40)
    return rotate_x(p2, -28)[1]


def build_view(cells, depth_fn, to_screen, title, group_x, group_y):
    scored = []
    for b, a in cells:
        allp = list(b) + [a]
        d = sum(depth_fn(p) for p in allp) / len(allp)
        scored.append((d, b, a))
    scored.sort(key=lambda t: t[0])  # farthest first, nearest last (painter's algorithm)

    out = [f'<g transform="translate({group_x},{group_y})">']
    out.append(f'<text class="caption" x="{VIEW_W / 2}" y="-10" text-anchor="middle">{title}</text>')
    face_classes = ["cell-face", "cell-face-alt"]
    for i, (d, b, a) in enumerate(scored):
        pb = [to_screen(v) for v in b]
        pa = to_screen(a)
        pts_str = " ".join(f"{x},{y}" for x, y in pb)
        cls = face_classes[i % 2]
        out.append(f'<polygon class="{cls}" points="{pts_str}"/>')
        out.append(
            f'<path class="strut" d="M{pb[0][0]},{pb[0][1]} L{pb[1][0]},{pb[1][1]} '
            f'L{pb[2][0]},{pb[2][1]} Z '
            f'M{pb[0][0]},{pb[0][1]} L{pa[0]},{pa[1]} '
            f'M{pb[1][0]},{pb[1][1]} L{pa[0]},{pa[1]} '
            f'M{pb[2][0]},{pb[2][1]} L{pa[0]},{pa[1]}"/>'
        )

    seen = set()
    for b, a in cells:
        for v in list(b) + [a]:
            k = key(v)
            if k in seen:
                continue
            seen.add(k)
            sx, sy = to_screen(v)
            cls = joint_class(v)
            out.append(f'<circle class="{cls}" cx="{sx}" cy="{sy}" r="5"/>')
    out.append("</g>")
    return "\n".join(out)


view_front_svg = build_view(all_cells, front_depth, to_screen_front, "Front view", 30, 40)
view_34_svg = build_view(all_cells, rot34_depth, to_screen_34, "3/4 view", 380, 40)

BODY = f'''  <title>Tetrahedral kite — front view and 3/4 view</title>

{view_front_svg}

{view_34_svg}

  <g transform="translate(30,320)">
    <circle class="ext-joint" cx="8" cy="0" r="6"/>
    <text class="label" x="20" y="4">Exterior, 1 cell — 3 sockets (kite_corner.scad)</text>
  </g>
  <g transform="translate(30,336)">
    <circle class="int-joint" cx="8" cy="0" r="6"/>
    <text class="label" x="20" y="4">Interior, 2 cells — 6 sockets (kite_corner_interior.scad)</text>
  </g>
  <g transform="translate(30,352)">
    <circle class="triple-joint" cx="8" cy="0" r="6"/>
    <text class="label" x="20" y="4">Triple, 3 cells — 9 sockets (kite_corner_triple.scad)</text>
  </g>
  <g transform="translate(30,368)">
    <circle class="unhandled-joint" cx="8" cy="0" r="6"/>
    <text class="label" x="20" y="4">4+ cells meeting — no hub file yet (see README)</text>
  </g>'''

ARIA = (
    'Schematic diagram of a 4-layer, 20-cell tetrahedral kite from two angles, '
    'showing exterior joints (red, 3-socket hub) at the outer tips, interior '
    'joints (blue, 6-socket hub) where 2 cells meet, triple joints (green, '
    '9-socket hub) where 3 cells meet, and one 4-cell joint (orange, not yet '
    'covered by any hub design) near the middle of the assembly.'
)

# ── Standalone file variant ──────────────────────────────────────────
# Used by kite-corners/README.md (GitHub markdown) and docs/kite-diagram.svg
# as a plain <img> source. Page CSS can never reach an externally-loaded
# <img>, so this variant carries its own fixed colours plus a
# prefers-color-scheme media query keyed to the OS/browser setting — it
# cannot follow the VINDSNURR site's manual light/dark TOGGLE (that
# requires the inline variant below), only the OS-level preference.
STANDALONE_SVG = f'''<svg width="720" height="400" viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" role="img"
     aria-label="{ARIA}">
  <style>
    svg {{ background: #fafaf5; }}
    .strut {{ stroke: #3a3a3a; stroke-width: 1.4; fill: none; }}
    .cell-face {{ fill: #4f8fd6; fill-opacity: 0.55; stroke: none; }}
    .cell-face-alt {{ fill: #2fa87d; fill-opacity: 0.55; stroke: none; }}
    .ext-joint {{ fill: #d6473c; stroke: #7a221c; stroke-width: 1; }}
    .int-joint {{ fill: #2c62c9; stroke: #17356f; stroke-width: 1; }}
    .triple-joint {{ fill: #2f9e44; stroke: #1a5c27; stroke-width: 1; }}
    .unhandled-joint {{ fill: #e8830a; stroke: #8a4d06; stroke-width: 1; }}
    .label {{ font-size: 12px; fill: #2c2c2a; }}
    .caption {{ font-size: 13px; fill: #2c2c2a; font-weight: 600; }}
    @media (prefers-color-scheme: dark) {{
      svg {{ background: #1a1a18; }}
      .strut {{ stroke: #c7c7c2; }}
      .cell-face {{ fill: #85b7eb; fill-opacity: 0.5; }}
      .cell-face-alt {{ fill: #5dcaa5; fill-opacity: 0.5; }}
      .label {{ fill: #e8e7e1; }}
      .caption {{ fill: #e8e7e1; }}
    }}
  </style>
{BODY}
</svg>'''

# ── Inline HTML-embed variant ────────────────────────────────────────
# For pasting directly into docs/kite-comparison.html's DOM (not <img>),
# so it uses the site's own CSS variables and follows the manual
# light/dark TOGGLE exactly like every other themed element on the page.
INLINE_SVG = f'''<svg width="720" height="400" viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" role="img"
     aria-label="{ARIA}" style="max-width:100%;height:auto;">
  <style>
    .kite-diagram .strut {{ stroke: var(--text-muted); stroke-width: 1.4; fill: none; }}
    .kite-diagram .cell-face {{ fill: #4f8fd6; fill-opacity: 0.5; stroke: none; }}
    .kite-diagram .cell-face-alt {{ fill: #2fa87d; fill-opacity: 0.5; stroke: none; }}
    .kite-diagram .ext-joint {{ fill: #d6473c; stroke: #7a221c; stroke-width: 1; }}
    .kite-diagram .int-joint {{ fill: #2c62c9; stroke: #17356f; stroke-width: 1; }}
    .kite-diagram .triple-joint {{ fill: #2f9e44; stroke: #1a5c27; stroke-width: 1; }}
    .kite-diagram .unhandled-joint {{ fill: #e8830a; stroke: #8a4d06; stroke-width: 1; }}
    .kite-diagram .label {{ font-size: 12px; fill: var(--text-main); }}
    .kite-diagram .caption {{ font-size: 13px; fill: var(--text-main); font-weight: 600; }}
  </style>
  <g class="kite-diagram">
{BODY}
  </g>
</svg>'''

standalone_target = Path(__file__).resolve().parent / "kite-diagram.svg"
standalone_target.write_text(STANDALONE_SVG)
print(f"wrote {standalone_target}")

inline_target = Path(__file__).resolve().parent / "kite-diagram-inline.svg"
inline_target.write_text(INLINE_SVG)
print(f"wrote {inline_target} (paste into docs/kite-comparison.html by hand)")
