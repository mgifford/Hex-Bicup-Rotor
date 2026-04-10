# VINDSNURR — Hexagonal Bicupola Wind Rotor

**Project:** HBR-6-14V · Rev 1.1  
**Rotor:** 1000mm diameter · 20mm aluminium shaft · 10mm rods

## What this project is

A 14-vertex, 36-edge, fully triangulated hexagonal wind rotor frame for a Savonius-style drag wind turbine. The geometry is derived from a hexagonal bicupola-like layered form (not a standard named solid).

- **Status:** Design-phase. 3D print files exist; no physical prototype yet.
- **Core files:** OpenSCAD `.scad` files in `3d/`. Export each to STL for printing.
- **Docs:** HTML visualizations in `docs/`.

## File structure

| File | Purpose |
|------|---------|
| `3d/vindsnurr_params.scad` | Shared parameters/constants — include in other files |
| `3d/hub_apex.scad` | Hub T and Hub B (top/bottom apex, degree 6) |
| `3d/hub_ring.scad` | Hub U1–U6 and L1–L6 (outer ring, degree 5) |
| `3d/hub_test_jig.scad` | Print-first test jig for socket fit and angles |
| `INSTRUCTIONS.md` | Full geometry specification and build document |
| `README.md` | Print procedure and hardware BOM |
| `AGENTS.md` | Consistency rules for AI agents and contributors |
| `ACCESSIBILITY.md` | Accessibility policy for HTML files |
| `docs/` | Interactive HTML visualizations, theory, and geometry comparison |

## Key geometry facts

- **14 vertices:** T, U1–U6, L1–L6, B
- **36 edges:** 6 top fan + 6 upper ring + 12 belt + 6 lower ring + 6 bottom fan
- **24 triangular faces** — fully triangulated, no quads
- **2 hub designs:** apex (degree 6, with bearing seat) and ring (degree 5)
- **3 rod lengths:** F1/F2 fan=610.4mm, F3/F4 ring=500.0mm, F5 belt=446.6mm
- Hub B mounts **30° rotated** from Hub T on the shaft

## OpenSCAD workflow

1. Open `.scad` file → press **F6** to render → **File → Export → Export as STL**
2. Increase `$fn` from 64 to 128 in each file before exporting final STL
3. All shared parameters are in `vindsnurr_params.scad`

## Critical notes

- Print `hub_test_jig.scad` **first** to calibrate `rod_tol` and `bearing_tol`
- Belt connectivity (U↔L) is the most error-prone assembly step — verify before bonding
- T does NOT connect to L nodes; B does NOT connect to U nodes (fabric only, not structural stays)
- U and L ring hubs are the same physical part — L hubs flip 180° during assembly
- Bearing: 6204-2RS (20mm ID, 47mm OD, 14mm H) — one per apex hub
