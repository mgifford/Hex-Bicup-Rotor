# AGENTS.md — Contributor and AI Agent Guidelines

This file tells human contributors and AI coding agents how to keep the
VINDSNURR project consistent. The geometry, hardware numbers, and visual
representations must stay in agreement across all file types.

---

## 1. The single source of truth

**`3d/vindsnurr_params.scad` is the canonical source for all geometry.**

Every dimension, angle, rod length, coordinate, and hardware specification
originates there. Before changing any number anywhere in the project, check
whether it is defined in `vindsnurr_params.scad` first.

| What | Canonical location | Derived / display copies |
|---|---|---|
| Node coordinates (T, U1–U6, L1–L6, B) | `vindsnurr_params.scad` comments | `INSTRUCTIONS.md` §2, `README.md` geometry ref, `docs/viz.html` JS |
| Rod lengths (F1/F2, F3/F4, F5) | `vindsnurr_params.scad` `F1_LENGTH` etc. | `README.md` cut list, `INSTRUCTIONS.md` §5, `docs/theory.html` power table |
| Shaft/bearing hardware | `vindsnurr_params.scad` `SHAFT_OD`, `BEARING_*` | `README.md` BOM, `hub_apex.scad` local copy, `docs/support-frame.html` §6 |
| Hub socket angles | `vindsnurr_params.scad` `RING_*` and `APEX_*` constants | `hub_apex.scad`, `hub_ring.scad` comments, `INSTRUCTIONS.md` §4 |
| Rotor diameter / height | `vindsnurr_params.scad` `ROTOR_DIAMETER`, `ROTOR_HEIGHT` | `README.md`, `docs/theory.html` power estimates, `docs/support-frame.html` load table |

---

## 2. Known parameter duplication (current tech debt)

`hub_apex.scad` and `hub_ring.scad` each declare their own local parameter
block instead of using `include <vindsnurr_params.scad>`. This is intentional
for now — it makes each file self-contained for printing without needing the
full library. The consequence is that **any change to shared parameters must be
applied in three places**:

1. `3d/vindsnurr_params.scad`
2. `3d/hub_apex.scad` (local copy)
3. `3d/hub_ring.scad` (local copy)

And then propagated to documentation — see §3 below.

If this duplication is ever resolved by switching to `include`, remove this
section and update the file table in §1.

---

## 3. Propagating a geometry change

If any core dimension changes (rod diameter, hub radius, bearing spec, rotor
size, node coordinates), touch all of the following:

**SCAD files**
- [ ] `3d/vindsnurr_params.scad` — update the constant
- [ ] `3d/hub_apex.scad` — update local copy if duplicated
- [ ] `3d/hub_ring.scad` — update local copy if duplicated
- [ ] `3d/hub_test_jig.scad` — update if shaft bore or rod socket affected

**Markdown documentation**
- [ ] `README.md` — rod cut list table, hardware BOM table
- [ ] `INSTRUCTIONS.md` — §2 node coordinates, §5 rod families, §4 hub angles
- [ ] `docs/theory.html` — power estimate table (uses `ROTOR_HEIGHT`, `ROTOR_DIAMETER`)
- [ ] `docs/support-frame.html` — shaft dimensions table, load estimates

**HTML pages** — these are the hardest to keep current; see §4
- [ ] `docs/viz.html` — JS vertex coordinates (search for `phi`, `R = 210`, `buildVerts`)
- [ ] `docs/step-by-step.html` — SVG diagrams with hardcoded hub and rod geometry
- [ ] `docs/site.css` / `docs/site.js` — shared nav: if a page is added or renamed, update the `<nav>` block in **all seven HTML files** (index, viz, step-by-step, theory, geometry-comparison, generator, support-frame)

**Comparison and theory docs** — update if the change affects the comparison claims
- [ ] `docs/geometry-comparison.html` — vertex/edge/face counts, rod length count
- [ ] `docs/theory.html` — RPM estimates, power output table

---

## 4. Rules for the HTML visualizations

The canvas in `docs/viz.html` and the SVG diagrams in `docs/step-by-step.html`
are **display representations**. They use scaled or simplified geometry, not
millimetre dimensions. Rules:

### Topology must match SCAD exactly
- 14 vertices: T, U1–U6, L1–L6, B — no more, no fewer
- 36 edges in the five families: top fan (6), upper ring (6), belt (12),
  lower ring (6), bottom fan (6)
- 24 triangular faces — no quads
- U ring at phase 0°, L ring at phase 30° (30° stagger)
- Sails: T–U1–L1, T–U3–L3, T–U5–L5 (upper); B–L1–U2, B–L3–U4, B–L5–U6 (lower)
- Belt connectivity: each Ui connects to L(i) and L(i−1 mod 6)

### Colour coding is shared across all files
Changing a colour in one place means changing it everywhere. Current palette:

| Element | Colour |
|---|---|
| Shaft / apex nodes | `#2c2c2a` (near-black) |
| Upper ring nodes (U) | `#534ab7` (indigo) |
| Lower ring nodes (L) | `#0f6e56` (teal-green) |
| Upper sails (T fan) | `rgba(133,183,235,0.80)` (sky blue) |
| Lower sails (B fan) | `rgba(93,202,165,0.80)` (sage green) |
| Structural stays | solid dark, depth-faded |
| Plastic sail edges | dashed, upper blue `#378add`, lower green `#1d9e75` |

### `docs/viz.html` vertex coordinates
The JS builds vertices from two parameters:
- `phi = 20 * Math.PI / 180` — ring latitude (matches `RING_LAT_DEG = 20.0` in params)
- `R = 210` — display radius in canvas pixels (not a physical dimension)

If `RING_LAT_DEG` changes in the SCAD params, update `phi` in the JS.
The display radius `R` is purely for screen layout and should not change with
physical rotor dimensions.

### SVG diagrams in `docs/step-by-step.html`
These are hand-authored schematic diagrams, not rendered from SCAD. They show
topology and assembly sequence, not precise geometry. When updating:
- Node labels must match the canonical vertex names (T, U1–U6, L1–L6, B)
- Edge connections must match the topology table above
- Sail shading must use the shared colour palette

---

## 5. Rules for OpenSCAD files

- **Do not hardcode geometry that is already in `vindsnurr_params.scad`.**
  If a hub file currently has a local copy of a parameter, mark it with a
  comment: `// SYNC: also in vindsnurr_params.scad`.
- Rod direction vectors (`rod_dirs`) in `hub_apex.scad` and `hub_ring.scad`
  are derived from the node coordinates. If coordinates change, the unit
  vectors must be recomputed — they are not automatically updated.
- `$fn = 64` is the working value. Final-print STLs use `$fn = 128`.
  Do not commit files with `$fn = 128` as the default.
- `rod_tol` and `bearing_tol` are print-calibration values. They are expected
  to vary per printer. The canonical values in `vindsnurr_params.scad` are
  starting points, not fixed specs.

---

## 6. Rules for documentation

### What must be accurate (match SCAD)
- All numbers in `README.md` — rod lengths, hardware specs, quantities
- All numbers in `INSTRUCTIONS.md` — node coordinates, hub angles, rod lengths
- The vertex/edge/face counts in `docs/geometry-comparison.html`

### What is intentionally approximate
- Power output estimates in `docs/theory.html` — these are first-order, Cp=0.20 baseline
- RPM estimates — derived from λ≈1 assumption, not measured
- The geometry comparison in `docs/geometry-comparison.html` — explicitly theoretical

### Validation disclaimer
All documents describing performance (Cp, cut-in speed, torque smoothing,
comparison with icosahedron geometry) must carry the disclaimer that no
physical prototype has been tested. Do not soften or remove that disclaimer
without a corresponding prototype test result to cite.

---

## 7. What to check before any commit

1. Do the vertex count (14), edge count (36), and face count (24) appear
   consistently wherever they are mentioned?
2. Do the three rod lengths (610.4 mm, 500.0 mm, 446.6 mm) match across
   the SCAD params file, README cut list, and INSTRUCTIONS §5?
3. Do the bearing specs (6204-2RS, 20mm ID, 47mm OD, 14mm H) match across
   SCAD params, README BOM, and INSTRUCTIONS §8?
4. Do the HTML files still render correctly in both light and dark mode?
5. Does any new performance claim carry the "untested / theoretical" caveat?

---

## 8. File roles — quick reference

| File | Role | Authoritative for |
|---|---|---|
| `3d/vindsnurr_params.scad` | Geometry library | All dimensions and angles |
| `3d/hub_apex.scad` | Printable hub | Apex hub geometry (local copy) |
| `3d/hub_ring.scad` | Printable hub | Ring hub geometry (local copy) |
| `3d/hub_test_jig.scad` | Calibration print | Tolerance testing |
| `INSTRUCTIONS.md` | Design specification | Geometry rationale and build sequence |
| `README.md` | Builder reference | Hardware BOM, print settings, cut list |
| `ACCESSIBILITY.md` | Accessibility policy | HTML file a11y requirements |
| `docs/index.html` | Site homepage | Navigation hub, project overview |
| `docs/viz.html` | Interactive viz | Topology display (canvas, JS) |
| `docs/step-by-step.html` | Assembly guide | Build sequence (SVG diagrams) |
| `docs/theory.html` | Aerodynamic theory | Savonius physics, performance estimates |
| `docs/geometry-comparison.html` | Design rationale | Icosahedron vs bicupola comparison |
| `docs/generator.html` | Generator guide | Generator selection, drive options, power expectations |
| `docs/support-frame.html` | Structural guide | Frame design, bearing hardware, shaft coupling, load estimates |
| `docs/site.css` | Shared stylesheet | Colour tokens, nav, prose, dark/light |
| `docs/site.js` | Shared script | Theme toggle, current-page nav marking |
| `CLAUDE.md` | AI context | Project overview for AI sessions |
| `AGENTS.md` | Contribution rules | Consistency and alignment rules (this file) |
