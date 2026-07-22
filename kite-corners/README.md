# Tetrahedral Kite Corners

**This is a separate hobby side-project, not part of the VINDSNURR wind rotor.**
It lives in this repository because it was inspired by the structural comparison
in [`../docs/kite-comparison.html`](../docs/kite-comparison.html), but the two
designs share nothing beyond "triangulated frames are rigid." Do not mix parts,
tolerances, or print settings between this directory and `../3d/`.

---

## What this is

A 3D-printed 3-way corner connector for building
[Alexander Graham Bell's tetrahedral kite](https://en.wikipedia.org/wiki/Tetrahedral_kite)
(1899–1903) out of rigid struts instead of the classic straws-and-knotted-string
build — see [this Instructables tutorial](https://www.instructables.com/Tetrahedral-Kite-1/)
for the original hobbyist version this design replaces the joints of.

Every vertex of a tetrahedral cell is identical (3 struts meeting at the
tetrahedral vertex angle, ≈70.53°), so there is **one hub design** — print as
many as your kite needs.

## Files

| File | Purpose |
|------|---------|
| `kite_corner.scad` | The corner hub — parametric, one design for every vertex |
| `validate_and_export.sh` | Renders the hub to confirm it's a clean manifold solid, then exports STL + 3MF |

## Just want to print? Skip OpenSCAD entirely

A ready-to-print **STL** and **3MF** file is already in
[`printable/`](printable/) — download it straight from GitHub and load it into
your slicer (Cura, PrusaSlicer, Bambu Studio, Creality Print, etc. all read
both formats natively). You don't need OpenSCAD unless you want to change a
dimension yourself.

## Software required (only if you're changing the design)

**OpenSCAD** (free) — https://openscad.org

```
cd kite-corners
./validate_and_export.sh
```

Requires OpenSCAD on `PATH`. Exports land in `printable/`. Re-run this after
any change to `kite_corner.scad` and commit the result, so the ready-to-print
files always match the current source. If validation fails, do not print the
part — check the log printed to `/tmp/kite_corner_validate_*.log` first.

Or manually: open `kite_corner.scad` in OpenSCAD → **F6** to render → **File → Export**.
Increase `$fn` from 64 to 128 before exporting for final printing.

## Build size

| Structure | Hubs needed | Struts needed |
|-----------|-------------|----------------|
| 1 tetrahedral cell | 4 | 6 |
| 10-cell kite (the classic build: 6 base + 3 mid + 1 top) | one per vertex — shared vertices reuse the same hub design, just print enough for your layout | 6 per cell × 10 cells, minus shared edges |

Work out the exact hub/strut count for your layout before printing — it
depends on how many cells you connect and which vertices are shared.

## Parameters (`kite_corner.scad`)

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `strut_d` | 6.0mm | Strut outer diameter — sized for 6mm dowel, fiberglass, or carbon rod |
| `strut_tol` | 0.3mm | Socket clearance — adjust per printer until struts slide in with light finger pressure |
| `strut_depth` | 16.0mm | Socket depth |
| `hub_r` | 12.0mm | Hub sphere body radius |
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
| Supports | Not required — sockets open outward/downward, no overhangs |

---

Open source · MIT licence (same as the parent repository)
