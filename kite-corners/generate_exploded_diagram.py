#!/usr/bin/env python3
"""Generates an exploded-view diagram of a 4-layer, 20-cell tetrahedral
kite: each layer is drawn as its own flat triangular panel, separated
vertically, with dashed connector lines showing which vertex in one layer
is the SAME physical joint as a vertex in the layer above/below it.

This supplements (does not replace) kite-diagram.svg's compact two-view
schematic. Where that diagram shows the whole assembled shape from two
camera angles, this one pulls the layers apart so you can see, layer by
layer, bottom to top, which hub type (exterior / interior / triple) goes
at each vertex — useful for planning a print run layer-by-layer rather than
puzzling over the whole 3D structure at once.

Geometry: identical derivation to generate_diagram.py (same 4-layer, 20-cell
assembly, each layer's base triangle anchored exactly to the layer below's
apex points). See kite-corners/README.md for the full derivation. Layers are
shown as a straight top-down (X,Y) projection of each layer's own triangular
footprint — no 3D perspective per layer, since separating them vertically in
2D already conveys the stacking; this keeps each layer's own triangle grid
undistorted and easy to read.

Writes two variants, matching generate_diagram.py's pattern:
- kite-corners/kite-exploded.svg — standalone file for README.md via <img>.
- kite-corners/kite-exploded-inline.svg — HTML fragment for pasting into
  docs/kite-comparison.html so it follows the site's manual theme toggle.

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


# Same 4-layer, 20-cell assembly as generate_diagram.py.
layer0 = build_layer([(0, 4), (1, 3), (2, 2), (3, 1)], z0=0, ox=0.0, oy=0.0)
l1_ox, l1_oy = layer0[0][1][0], layer0[0][1][1]
layer1 = build_layer([(0, 3), (1, 2), (2, 1)], z0=tetra_h, ox=l1_ox, oy=l1_oy)
l2_ox, l2_oy = layer1[0][1][0], layer1[0][1][1]
layer2 = build_layer([(0, 2), (1, 1)], z0=2 * tetra_h, ox=l2_ox, oy=l2_oy)
l3_ox, l3_oy = layer2[0][1][0], layer2[0][1][1]
layer3 = build_layer([(0, 1)], z0=3 * tetra_h, ox=l3_ox, oy=l3_oy)

all_layers = [layer0, layer1, layer2, layer3]
all_cells = layer0 + layer1 + layer2 + layer3


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
    return "unhandled-joint"


JOINT_LABEL = {
    "ext-joint": "ext",
    "int-joint": "int",
    "triple-joint": "3x",
    "unhandled-joint": "4x",
}

# ── Layout constants ──────────────────────────────────────────────
PANEL_W = 640
PANEL_H = 150   # height of one layer's triangle panel
GAP = 70        # vertical gap between panels (where connector lines run)
PAD = 30
LABEL_W = 90    # left margin for the "Layer N" label + hub-count text
PANEL_MARGIN = 20  # inner margin so triangles don't touch the panel border

# Each layer's own triangular footprint is a very different size (Layer 0
# spans ~3.46 units tall, Layer 3 only ~0.87), so ONE global scale factor
# either overflows the small panels or makes the big layers illegibly tiny.
# Fit each layer independently into its own panel (both width and height
# constrained, aspect ratio preserved, centered horizontally) — this is a
# build-planning aid, not a scale-accurate render, so per-layer legibility
# matters more than relative size between layers.


def layer_footprint(layer):
    xs, ys = [], []
    for b, a in layer:
        for v in b:
            xs.append(v[0])
            ys.append(v[1])
        xs.append(a[0])
        ys.append(a[1])
    return min(xs), max(xs), min(ys), max(ys)


def make_transform(layer, panel_top_y):
    minx, maxx, miny, maxy = layer_footprint(layer)
    w = (maxx - minx) or 1
    h = (maxy - miny) or 1
    avail_w = PANEL_W - LABEL_W - 2 * PANEL_MARGIN
    avail_h = PANEL_H - 2 * PANEL_MARGIN
    s = min(avail_w / w, avail_h / h)
    drawn_w = w * s
    x_offset = LABEL_W + PANEL_MARGIN + (avail_w - drawn_w) / 2

    def to_panel_xy(p):
        x = (p[0] - minx) * s + x_offset
        # base row near the bottom of the panel, apex near the top
        y = panel_top_y + PANEL_H - PANEL_MARGIN - (p[1] - miny) * s
        return (round(x, 2), round(y, 2))

    return to_panel_xy


def layer_svg(layer_idx, layer, panel_top_y, cell_face_classes):
    to_panel_xy = make_transform(layer, panel_top_y)

    out = [f'<g class="layer-panel">']
    # panel background + border to visually separate each layer
    out.append(
        f'<rect class="panel-bg" x="{LABEL_W}" y="{panel_top_y}" '
        f'width="{PANEL_W - LABEL_W}" height="{PANEL_H}" rx="6"/>'
    )
    out.append(
        f'<text class="layer-label" x="10" y="{panel_top_y + PANEL_H/2 - 6}">Layer {layer_idx}</text>'
    )
    n_cells = len(layer)
    out.append(
        f'<text class="layer-sublabel" x="10" y="{panel_top_y + PANEL_H/2 + 12}">{n_cells} cell{"s" if n_cells != 1 else ""}</text>'
    )

    for i, (b, a) in enumerate(layer):
        pb = [to_panel_xy(v) for v in b]
        pa = to_panel_xy(a)
        cls = cell_face_classes[i % 2]
        pts_str = " ".join(f"{x},{y}" for x, y in pb)
        out.append(f'<polygon class="{cls}" points="{pts_str}"/>')
        out.append(
            f'<path class="strut" d="M{pb[0][0]},{pb[0][1]} L{pb[1][0]},{pb[1][1]} '
            f'L{pb[2][0]},{pb[2][1]} Z '
            f'M{pb[0][0]},{pb[0][1]} L{pa[0]},{pa[1]} '
            f'M{pb[1][0]},{pb[1][1]} L{pa[0]},{pa[1]} '
            f'M{pb[2][0]},{pb[2][1]} L{pa[0]},{pa[1]}"/>'
        )

    seen = set()
    vert_screen_pos = {}
    for b, a in layer:
        for v in list(b) + [a]:
            k = key(v)
            if k in seen:
                continue
            seen.add(k)
            sx, sy = to_panel_xy(v)
            cls = joint_class(v)
            out.append(f'<circle class="{cls}" cx="{sx}" cy="{sy}" r="6"/>')
            vert_screen_pos[k] = (sx, sy)
    out.append("</g>")
    return "\n".join(out), vert_screen_pos


def connectors_svg(lower_pos, upper_pos, lower_top_of_panel_y, upper_bottom_of_panel_y):
    # For every vertex key present in BOTH the lower layer's apex set and
    # the upper layer's base set (i.e. actually the same physical joint),
    # draw a dashed line between their two panel positions.
    out = []
    shared_keys = set(lower_pos.keys()) & set(upper_pos.keys())
    for k in shared_keys:
        x1, y1 = lower_pos[k]
        x2, y2 = upper_pos[k]
        out.append(f'<path class="connector" d="M{x1},{y1} L{x2},{y2}"/>')
    return "\n".join(out)


# Build panels bottom-to-top: Layer 0 at the BOTTOM of the image (largest
# panel_top_y), Layer 3 at the TOP (smallest panel_top_y) — matches how the
# kite is physically built and matches "bottom to top" from the request.
n_layers = len(all_layers)
total_h = n_layers * PANEL_H + (n_layers - 1) * GAP + 2 * PAD

panel_tops = []
for li in range(n_layers):
    # li=0 (Layer 0 / base) should be at the BOTTOM of the image.
    from_bottom = li
    panel_top_y = PAD + (n_layers - 1 - from_bottom) * (PANEL_H + GAP)
    panel_tops.append(panel_top_y)

face_classes = ["cell-face", "cell-face-alt"]
panels_svg = []
vert_positions_by_layer = []
for li, layer in enumerate(all_layers):
    svg, positions = layer_svg(li, layer, panel_tops[li], face_classes)
    panels_svg.append(svg)
    vert_positions_by_layer.append(positions)

# Connectors: between layer li's BASE vertices and layer (li-1)'s APEX
# vertices (li-1 is physically below li). Since vert_positions_by_layer[li]
# contains ALL of that layer's vertices (base + apex) keyed by 3D position,
# and shared vertices have IDENTICAL 3D keys across layers (verified in
# generate_diagram.py's derivation), the shared-key intersection between
# adjacent layers automatically finds exactly the joint vertices, no manual
# bookkeeping of "which are base vs apex" required.
connector_blocks = []
for li in range(1, n_layers):
    lower = vert_positions_by_layer[li - 1]
    upper = vert_positions_by_layer[li]
    connector_blocks.append(connectors_svg(lower, upper, None, None))

BODY = f'''  <title>Tetrahedral kite — exploded layer view, bottom to top</title>
{"".join(connector_blocks)}
{"".join(panels_svg)}
  <g transform="translate({LABEL_W},{total_h - 6})">
    <circle class="ext-joint" cx="8" cy="0" r="6"/>
    <text class="label" x="20" y="4">Exterior — 3 sockets (kite_corner.scad)</text>
  </g>
  <g transform="translate({LABEL_W},{total_h + 12})">
    <circle class="int-joint" cx="8" cy="0" r="6"/>
    <text class="label" x="20" y="4">Interior, 2 cells — 6 sockets (kite_corner_interior.scad)</text>
  </g>
  <g transform="translate({LABEL_W},{total_h + 30})">
    <circle class="triple-joint" cx="8" cy="0" r="6"/>
    <text class="label" x="20" y="4">Triple, 3 cells — 9 sockets (kite_corner_triple.scad)</text>
  </g>
  <g transform="translate({LABEL_W},{total_h + 48})">
    <circle class="unhandled-joint" cx="8" cy="0" r="6"/>
    <text class="label" x="20" y="4">4+ cells meeting — no hub file yet (see README)</text>
  </g>
  <g transform="translate({LABEL_W},{total_h + 66})">
    <path class="connector" d="M8,0 L40,0"/>
    <text class="label" x="48" y="4">Dashed line = same physical joint shared between adjacent layers</text>
  </g>'''

TOTAL_H = total_h + 90

ARIA = (
    'Exploded view of a 4-layer, 20-cell tetrahedral kite, showing each '
    'layer as a separate flat panel from Layer 0 (base, bottom) to Layer 3 '
    '(top), with dashed lines connecting each vertex to the matching joint '
    'in the layer above or below, and joints colour-coded by how many '
    'cells meet there: exterior (red), interior 2-cell (blue), triple '
    '3-cell (green), and one unhandled 4-cell joint (orange).'
)

STANDALONE_SVG = f'''<svg width="{PANEL_W}" height="{TOTAL_H}" viewBox="0 0 {PANEL_W} {TOTAL_H}" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" role="img"
     aria-label="{ARIA}">
  <style>
    svg {{ background: #fafaf5; }}
    .panel-bg {{ fill: #eeece4; stroke: #d8d5cb; stroke-width: 1; }}
    .strut {{ stroke: #3a3a3a; stroke-width: 1.2; fill: none; }}
    .connector {{ stroke: #9a9a94; stroke-width: 1.2; fill: none; stroke-dasharray: 4 3; }}
    .cell-face {{ fill: #4f8fd6; fill-opacity: 0.55; stroke: none; }}
    .cell-face-alt {{ fill: #2fa87d; fill-opacity: 0.55; stroke: none; }}
    .ext-joint {{ fill: #d6473c; stroke: #7a221c; stroke-width: 1; }}
    .int-joint {{ fill: #2c62c9; stroke: #17356f; stroke-width: 1; }}
    .triple-joint {{ fill: #2f9e44; stroke: #1a5c27; stroke-width: 1; }}
    .unhandled-joint {{ fill: #e8830a; stroke: #8a4d06; stroke-width: 1; }}
    .label {{ font-size: 12px; fill: #2c2c2a; }}
    .layer-label {{ font-size: 14px; fill: #2c2c2a; font-weight: 700; }}
    .layer-sublabel {{ font-size: 11px; fill: #5f5e5a; }}
    @media (prefers-color-scheme: dark) {{
      svg {{ background: #1a1a18; }}
      .panel-bg {{ fill: #232320; stroke: #35342f; }}
      .strut {{ stroke: #c7c7c2; }}
      .connector {{ stroke: #6b6a64; }}
      .cell-face {{ fill: #85b7eb; fill-opacity: 0.5; }}
      .cell-face-alt {{ fill: #5dcaa5; fill-opacity: 0.5; }}
      .label {{ fill: #e8e7e1; }}
      .layer-label {{ fill: #e8e7e1; }}
      .layer-sublabel {{ fill: #a8a79f; }}
    }}
  </style>
{BODY}
</svg>'''

INLINE_SVG = f'''<svg width="{PANEL_W}" height="{TOTAL_H}" viewBox="0 0 {PANEL_W} {TOTAL_H}" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" role="img"
     aria-label="{ARIA}" style="max-width:100%;height:auto;">
  <style>
    .kite-exploded .panel-bg {{ fill: var(--bg-code); stroke: var(--border); stroke-width: 1; }}
    .kite-exploded .strut {{ stroke: var(--text-muted); stroke-width: 1.2; fill: none; }}
    .kite-exploded .connector {{ stroke: var(--text-faint); stroke-width: 1.2; fill: none; stroke-dasharray: 4 3; }}
    .kite-exploded .cell-face {{ fill: #4f8fd6; fill-opacity: 0.5; stroke: none; }}
    .kite-exploded .cell-face-alt {{ fill: #2fa87d; fill-opacity: 0.5; stroke: none; }}
    .kite-exploded .ext-joint {{ fill: #d6473c; stroke: #7a221c; stroke-width: 1; }}
    .kite-exploded .int-joint {{ fill: #2c62c9; stroke: #17356f; stroke-width: 1; }}
    .kite-exploded .triple-joint {{ fill: #2f9e44; stroke: #1a5c27; stroke-width: 1; }}
    .kite-exploded .unhandled-joint {{ fill: #e8830a; stroke: #8a4d06; stroke-width: 1; }}
    .kite-exploded .label {{ font-size: 12px; fill: var(--text-main); }}
    .kite-exploded .layer-label {{ font-size: 14px; fill: var(--text-main); font-weight: 700; }}
    .kite-exploded .layer-sublabel {{ font-size: 11px; fill: var(--text-muted); }}
  </style>
  <g class="kite-exploded">
{BODY}
  </g>
</svg>'''

standalone_target = Path(__file__).resolve().parent / "kite-exploded.svg"
standalone_target.write_text(STANDALONE_SVG)
print(f"wrote {standalone_target}")

inline_target = Path(__file__).resolve().parent / "kite-exploded-inline.svg"
inline_target.write_text(INLINE_SVG)
print(f"wrote {inline_target} (paste into docs/kite-comparison.html by hand)")
