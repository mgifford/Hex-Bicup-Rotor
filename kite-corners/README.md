# Tetrahedral Kite Corners

**This is a separate hobby side-project, not part of the VINDSNURR wind rotor.**
It lives in this repository because it was inspired by the structural comparison
in [`../docs/kite-comparison.html`](../docs/kite-comparison.html), but the two
designs share nothing beyond "triangulated frames are rigid." Do not mix parts,
tolerances, or print settings between this directory and `../3d/`.

---

## What this is

3D-printed corner connectors for building
[Alexander Graham Bell's tetrahedral kite](https://en.wikipedia.org/wiki/Tetrahedral_kite)
out of rigid struts instead of the classic straws-and-knotted-string build.
Bell's tetrahedral cell research (starting in the late 1890s) scaled all the
way up to real piloted flight: his *Frost King* prototype had about 1,300
cells, and a *Cygnet*-series kite with roughly 3,393 cells carried a man to
about 51m (168ft) above Baddeck Bay, Nova Scotia, on 6 December 1907 — see
[Wikipedia: Man-lifting kite](https://en.wikipedia.org/wiki/Man-lifting_kite)
for the documented history. This design is a small-scale hobby homage to that
structural idea, not a reproduction of Bell's specific kites.

Reference builds this design is informed by:
- [Instructables: Tetrahedral Kite](https://www.instructables.com/Tetrahedral-Kite-1/) — a 10-cell straws/string/tissue-paper build
- [Western Engineering Outreach: Tetrahedral Flight](https://www.eng.uwo.ca/outreach/files/STEM-Home/Week-7/W7-Tetrahedral-Flight.pdf) — a simpler 4-cell classroom-activity build, with an explicit rule worth keeping in mind for any layout: *"Tetrahedrons may only be connected at the corners, not along the edges or the faces"*
- [Building the Kono-Bell Tetrahedral Kite](https://booksbrassandthebear.wordpress.com/2017/07/05/building-the-kono-bell-tetrahedral-kite/) — describes the recursive scaling method Bell himself used: 4 cells make a kite, then that whole kite becomes one "cell" in a group of 4 for the next size up

![Schematic diagram of the 10-cell tetrahedral kite from a front view and a 3/4 view, showing exterior joints in red at the outer tips and interior joints in blue where cells meet](kite-diagram.svg)

*Front view and 3/4 view of the classic 10-cell arrangement (6 base cells + 3
mid cells + 1 top cell). Red = exterior joint (3-socket hub), blue = interior
joint (6-socket hub). This is a schematic, not a precision engineering
drawing — but the vertex positions and which joints are exterior vs interior
were computed from real 3D coordinates (see "The two vertex types" below),
not drawn freehand.*

**Two hub designs, for two different vertex types:**

| Hub | File | Sockets | Use for |
|-----|------|---------|---------|
| Exterior corner | `3d/kite_corner.scad` | 3 | Vertices touched by only one tetrahedral cell (the tips of the outermost cells) |
| Interior joint | `3d/kite_corner_interior.scad` | 6 (1 through-bore + 4 blind) | Vertices where two cells meet corner-to-corner (any multi-cell kite has these) |

A single tetrahedral cell only needs the exterior hub (4 per cell). Any kite
built from more than one cell — like the classic 10-cell arrangement in the
Instructables build — needs interior hubs wherever two cells share a vertex.
See **Which hub goes where** below for how to tell them apart in your layout.

## Files

| File | Purpose |
|------|---------|
| `3d/kite_corner.scad` | Exterior corner hub — 3 sockets at 60° |
| `3d/kite_corner_interior.scad` | Interior joint hub — 6 sockets for two cells meeting at a point |
| `3d/validate_and_export.sh` | Renders both hubs to confirm they're clean manifold solids, then exports STL + 3MF |
| `3d/printable/` | Ready-to-print STL + 3MF output (committed to the repo) |
| `kite-diagram.svg` | Schematic diagram of the 10-cell kite, front + 3/4 view, joint types colour-coded |

## Just want to print? Skip OpenSCAD entirely

Ready-to-print **STL** and **3MF** files are already in
[`3d/printable/`](3d/printable/) — download the one(s) you need straight from
GitHub and load them into your slicer (Cura, PrusaSlicer, Bambu Studio,
Creality Print, etc. all read both formats natively). You don't need OpenSCAD
unless you want to change a dimension yourself.

## Software required (only if you're changing the design)

**OpenSCAD** (free) — https://openscad.org

```
cd kite-corners/3d
./validate_and_export.sh
```

Requires OpenSCAD on `PATH`. Exports land in `3d/printable/`. Re-run this
after any change to either `.scad` file and commit the result, so the
ready-to-print files always match the current source. If validation fails,
do not print the part — check the log printed to
`/tmp/kite_corner_validate_*.log` first.

Or manually: open a `.scad` file in OpenSCAD → **F6** to render → **File → Export**.
Increase `$fn` from 64 to 128 before exporting for final printing.

## The two vertex types — how the geometry was derived

A regular tetrahedron's faces are all equilateral triangles, so **the angle
between any two struts meeting at a vertex is 60°** — not arccos(1/3) ≈ 70.53°,
which is a different quantity (the *dihedral* angle between two faces sharing
an edge). This was verified numerically: built a real unit-edge tetrahedron
from coordinates and measured the actual angle between edges at a vertex,
rather than trusting the formula from memory. If you've read an earlier
version of this file or `kite_corner.scad`, it used the wrong (70.53°) angle —
that bug is fixed as of this version.

**Interior joints** were derived the same way: built a real edge-2 tetrahedron,
subdivided it at the edge midpoints into 4 unit sub-tetrahedra (the standard
construction for a multi-cell tetrahedral kite — cells meet only at shared
*vertices*, not shared edges, which is why it's light and why the classic
build "ties" cells together rather than doubling up struts). Reading off the
6 real strut directions at one shared vertex showed that **2 of the 6 are
exactly opposite (180°)** — so `kite_corner_interior.scad` models that pair as
one continuous through-bore, with the other 4 as separate blind sockets at
60°/120° to the bore axis.

## Which hub goes where

The diagram above shows one example layout — the 10-cell stack (6 base cells
+ 3 mid cells + 1 top cell, forming one large tetrahedron overall) from the
Instructables build:

- Every cell's **outward-facing tip** — the 3 corners of the whole assembly,
  plus the outer corners of the base layer that aren't shared with another
  cell — is an **exterior** vertex. Use `kite_corner.scad`.
- Every point where a **mid-layer cell's base corner rests on a base-layer
  cell's apex** (and where the top cell rests on the mid layer) is an
  **interior** vertex — two cells' struts meet there. Use
  `kite_corner_interior.scad`.

**This isn't the only valid layout.** Bell's own kites — and the recursive
"4 cells make a kite, then 4 kites make the next size up" method described in
the Kono-Bell build log linked above — use a different overall shape, but the
same joint rule applies at every scale: wherever exactly 2 cells meet at a
single shared corner, it's an interior vertex (6-socket hub), and every
untouched outer tip is an exterior vertex (3-socket hub). The joint angles
don't change with scale — only the strut length does, which is why both hub
files expose `strut_d`/`strut_depth` as parameters rather than hardcoding
one size.

Work out the exact hub count for your specific layout before printing — it
depends on how many cells you connect and exactly which vertices are shared.
When in doubt, dry-fit the whole frame with tape or string first, same as the
test-jig-first approach in the main VINDSNURR project.

## Assembly — building a cell and joining cells

The steps below follow the same build sequence as the
[Western Engineering Outreach activity](https://www.eng.uwo.ca/outreach/files/STEM-Home/Week-7/W7-Tetrahedral-Flight.pdf)
(single cell → 4-cell kite → cover → fly), adapted for rigid struts and
printed hubs instead of straws and thread.

### 1. Cut your struts

All struts in one cell must be the **same length** — pick a length (150–250mm
is a comfortable hobby size) and cut 6 struts of 6mm dowel, fiberglass, or
carbon rod to that length, with clean square-cut ends. Every strut in the
kite should be this same length unless you're deliberately mixing cell sizes.

### 2. Print a test piece first

Before printing a full set of hubs, print **one** exterior hub
(`kite_corner.scad`) and test-fit a strut in each of its 3 sockets:

- **Too tight** — increase `strut_tol` (default 0.3mm) and reprint
- **Too loose / wobbles** — decrease `strut_tol` and reprint
- **Correct** — strut slides in with light finger pressure, no wobble, no force needed

Once the fit is right, do the same check with one interior hub
(`kite_corner_interior.scad`) — it uses the same `strut_tol`, but confirm the
through-bore and the 4 blind sockets all take the strut the same way.

### 3. Build one tetrahedral cell

A single cell needs **4 exterior hubs and 6 struts**:

- Glue (or press-fit, if your tolerance is snug enough) 3 struts into 3
  sockets of one hub — this is one **base corner**.
- Do the same for 2 more hubs, so you have 3 hubs each holding 3 struts,
  radiating outward.
- Bring the 3 free strut ends together and join them with a 4th hub — this
  closes the triangular base and forms the **apex**.
- Check: you should now have a rigid 4-hub, 6-strut tetrahedron that doesn't
  flex or rack when you squeeze it. If it flexes, a strut is loose in its
  socket — re-glue that joint before continuing.

Cover 2 of the 4 faces with a lightweight sail material (ripstop nylon,
tissue paper, or plastic sheeting all work — this is a low-load hobby part,
so covering choice is about weight and looks, not strength). Leave the other
2 faces open, same as the reference builds.

### 4. Join cells at shared corners — never along an edge or face

This is the one rule to get right, confirmed independently by every
reference build linked above: **cells connect only by sharing a single
corner vertex.** Never glue two cells' struts side-by-side along a shared
edge, and never overlap their faces.

To join a second cell to the first:

- Pick one corner (hub) of the first cell to be a **shared vertex**.
- Build the second cell the same way as step 3, but instead of closing its
  last corner with a fresh exterior hub, close it into an
  **interior hub** (`kite_corner_interior.scad`) that is *also* one of the
  first cell's corners.
- In practice: replace the exterior hub at that one shared corner with an
  interior hub before you glue the struts in. Each cell contributes exactly
  3 struts to the shared hub. One strut from the first cell and one strut
  from the second cell happen to point in exactly opposite directions once
  both cells are in place — those two go in the interior hub's single
  through-bore (one from each end). The remaining 2 struts from each cell
  (4 total) go in the 4 separate blind sockets.
- Every other corner of both cells — the ones not shared — stays an
  **exterior** hub.

Repeat for however many cells your layout needs, replacing an exterior hub
with an interior hub every time two cells meet at a corner. See
**Which hub goes where** below for how the full 10-cell and recursive
4-cell-of-4-cells layouts break down.

### 5. Attach the flight line and fly

Tie (or loop through a small eyelet you print or drill into a hub) the
flight line to an outer corner of the completed frame — the reference builds
attach it at a corner between two covered faces, which tends to keep the
kite's covered side facing into the wind. Balance-test by hand in light wind
before committing to a long flight line; if the kite won't stay stable,
re-check the belt/edge connectivity against your layout diagram before
assuming the sail placement is wrong.

## Build size

| Structure | Exterior hubs | Interior hubs | Struts |
|-----------|---------------|----------------|--------|
| 1 tetrahedral cell (standalone) | 4 | 0 | 6 |
| Multi-cell kite | varies by layout — outward tips only | varies by layout — one per cell-to-cell contact point | 6 per cell |

## Parameters

Both files share the same parameter names:

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `strut_d` | 6.0mm | Strut outer diameter — sized for 6mm dowel, fiberglass, or carbon rod |
| `strut_tol` | 0.3mm | Socket clearance — adjust per printer until struts slide in with light finger pressure |
| `strut_depth` | 16.0mm | Blind socket depth |
| `hub_r` | 12.0mm (exterior) / 14.0mm (interior) | Hub sphere body radius |
| `wall` | 2.5mm | Minimum wall thickness |

This is a **low-load hobby part** — a kite's tether and wind loads are far
lighter than VINDSNURR's continuous rotational loads, so 15–20% infill and
2 wall perimeters in PLA are enough. No bearing, no shaft, no calibration jig
needed — just print a test piece first and check the strut fit.

## Print settings

| Setting | Value |
|---------|-------|
| Material | PLA (indoor kite), PETG if it'll live outdoors |
| Infill | 15–20% |
| Layer height | 0.2mm |
| Walls | 2 perimeters minimum |
| Supports | Exterior hub: not required. Interior hub: recommended for the 4 angled sockets. |

---

Open source · MIT licence (same as the parent repository)
