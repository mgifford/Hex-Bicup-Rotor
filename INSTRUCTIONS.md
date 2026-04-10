# Hexagonal Bicupola-Derived Wind Rotor — Build Document

**Status:** Design-phase reference. Not yet validated by physical prototype.  
**Geometry source:** 14-vertex rotor graph developed through iterative diagram work in this session.  
**Document version:** 1.0  

---

## 1. Geometry Diagnosis

### Plain language description

The rotor is a vertically oriented, approximately spherical open-frame structure. A central shaft runs from top to bottom. Two apex nodes — T at the top and B at the bottom — are mounted on the shaft. Between them sit two hexagonal rings of six nodes each. The upper ring (U1–U6) is closer to T. The lower ring (L1–L6) is closer to B. The lower ring is rotated 30 degrees relative to the upper ring. This stagger produces the triangulated middle belt and gives each sail its diagonal geometry.

The frame is fully triangulated. Every face is a triangle. There are no quadrilateral faces.

### Formal description

This geometry is derived from a hexagonal bicupola-like layered form. It is not a standard Johnson solid or Archimedean solid. The label "bicupola-like" describes the layered structure only — two hexagonal caps connected by a staggered triangulated belt.

**Key properties:**

- 6-fold rotational symmetry (C6v approximately)
- The 30° stagger between U and L rings breaks perfect top-bottom mirror symmetry but the alternating sail pattern restores effective rotational and aerodynamic balance
- Approximately spherical when projected; both rings sit at equal latitudes above and below the equatorial plane
- Vertical rotation axis (the shaft)
- Complete triangulation: 24 triangular faces, no open quads

### What is certain

- 14 vertices, 36 edges, 24 triangular faces
- T connects only to U nodes. B connects only to L nodes.
- Each U node connects to exactly two adjacent L nodes (belt edges)
- No structural stays from T directly to L, or from B directly to U. Those edges exist only as sail fabric edges.

### What is inferred

- Equal ring radii top and bottom (symmetric bicupola form). A physical build could use slightly different radii without breaking the graph topology.
- Rings placed at equal latitudes. Exact placement depends on the shaft length and ring diameter selected.

### What is uncertain

- Optimal ring diameter-to-height ratio for the target wind speed range
- Generator coupling details (addressed separately in section 8)
- Whether the rotor needs a fixed stator or free-spinning mount

---

## 2. Point Model

### Node sets

| Label | Description | Count |
|-------|-------------|-------|
| T | Top apex. Shaft top mount. Connects to all U nodes. | 1 |
| U1–U6 | Upper ring. Phase 0°. Sits between T and the middle belt. | 6 |
| L1–L6 | Lower ring. Phase 30° offset. Sits between the middle belt and B. | 6 |
| B | Bottom apex. Shaft bottom mount. Connects to all L nodes. | 1 |

**Total vertices: 14**

### Labeling convention

Nodes numbered clockwise viewed from above, starting from an arbitrary reference direction.

- U ring: U1 at 0°, U2 at 60°, U3 at 120°, U4 at 180°, U5 at 240°, U6 at 300°
- L ring: L1 at 30°, L2 at 90°, L3 at 150°, L4 at 210°, L5 at 270°, L6 at 330°

L1 sits in the horizontal plane between U1 and U2. L2 sits between U2 and U3. And so on.

### Physical interpretation

Each node is a physical hub. T and B are shaft-mounted hubs. U and L nodes are outer ring hubs, connected to each other and to the apexes by rods. The shaft passes through T and B and extends beyond both for bearing and generator mounting.

---

## 3. Node-Edge Graph

### Edge families

| Family | Description | Count |
|--------|-------------|-------|
| Top fan | T–U1, T–U2, T–U3, T–U4, T–U5, T–U6 | 6 |
| Upper ring | U1–U2, U2–U3, U3–U4, U4–U5, U5–U6, U6–U1 | 6 |
| Belt | Each U connects to two adjacent L nodes (see table) | 12 |
| Lower ring | L1–L2, L2–L3, L3–L4, L4–L5, L5–L6, L6–L1 | 6 |
| Bottom fan | B–L1, B–L2, B–L3, B–L4, B–L5, B–L6 | 6 |

**Total edges: 36**

### Belt edge table

| Upper node | Connects to |
|------------|-------------|
| U1 | L6, L1 |
| U2 | L1, L2 |
| U3 | L2, L3 |
| U4 | L3, L4 |
| U5 | L4, L5 |
| U6 | L5, L6 |

### Face families

| Family | Triangles | Count |
|--------|-----------|-------|
| Upper cap | T–Ui–U(i+1) for i = 1..6 | 6 |
| Upper belt | Ui–Li–L(i−1) for i = 1..6 (downward-pointing triangles) | 6 |
| Lower belt | Ui–U(i+1)–Li for i = 1..6 (upward-pointing triangles) | 6 |
| Lower cap | B–Li–L(i+1) for i = 1..6 | 6 |

**Total faces: 24** — all triangular.

### Which graph version to use

- **Conceptual understanding:** The 5-family edge list above is sufficient.
- **First prototype:** The belt edge table is the critical reference. The fan edges are simple; the belt connectivity is where assembly errors occur.
- **Full structural check:** Use the complete 36-edge list with node coordinates to verify no rod lengths are unintentionally unequal.

---

## 4. Minimal Hub Family Count

The hub type is determined by the number and angles of rods connecting into it.

### Hub families

**Hub T — Top apex**  
- Degree: 6 (connects to U1 through U6)  
- Instances: 1  
- Rods: 6 top fan rods, all at equal angles (60° apart in the horizontal plane, angled downward)  
- Notes: Shaft passes through this hub. Requires a central bore for the shaft. No mirrored version needed — it is symmetric about the shaft axis.

**Hub B — Bottom apex**  
- Degree: 6 (connects to L1 through L6)  
- Instances: 1  
- Rods: 6 bottom fan rods, all at equal angles (60° apart, angled upward)  
- Notes: Identical degree to Hub T but the rod angles differ because L ring is offset 30° from U ring. Hub B is a rotated version of Hub T, not a mirror. If the shaft mount is symmetric, T and B can share the same hub design rotated 30°.  
- **This is the first opportunity to reduce hub families: T and B may be the same physical hub type, mounted at different rotational orientations.**

**Hub U — Upper ring nodes**  
- Degree: 5 (connects to: T, the two adjacent U nodes, and two adjacent L nodes)  
- Instances: 6  
- Rods: 1 top fan rod (upward toward T) + 2 upper ring rods (horizontal, ±60°) + 2 belt rods (downward toward L ring)  
- Notes: All six U hubs are identical by the 6-fold symmetry. One hub design, six instances.

**Hub L — Lower ring nodes**  
- Degree: 5 (connects to: B, the two adjacent L nodes, and two adjacent U nodes)  
- Instances: 6  
- Rods: 1 bottom fan rod (downward toward B) + 2 lower ring rods (horizontal, ±60°) + 2 belt rods (upward toward U ring)  
- Notes: All six L hubs are identical by symmetry. The rod angles at L differ from those at U because the belt rods arrive from slightly different directions. Whether Hub L can reuse Hub U depends on whether the angular geometry is close enough to tolerate in fabrication. This must be verified with actual coordinates before committing to a single hub design.

### Summary

| Hub type | Instances | Degree | Notes |
|----------|-----------|--------|-------|
| Apex (T/B) | 2 | 6 | Likely reusable if mount is symmetric |
| Upper ring (U) | 6 | 5 | One design, six instances |
| Lower ring (L) | 6 | 5 | May share design with U — verify angles |

**Minimum hub families: 2** (apex and ring), if U and L hub angles are close enough.  
**Conservative hub families: 3** (apex-T, apex-B, ring) if T and B cannot share a design, plus a potential 4th if U and L ring angles differ enough to require separate designs.

### Tradeoff

Fewer hub types reduce fabrication complexity but require tighter angular tolerance. For a first prototype, fabricate all three families separately and test fit before committing to consolidation.

---

## 5. Rod and Strut Families

### Symbolic definitions

Let:
- `r` = outer ring radius (horizontal distance from shaft axis to any U or L node)
- `h` = vertical distance from equatorial plane to T or B apex
- `d` = vertical distance from equatorial plane to the U or L ring

These are design variables. Choose `r`, `h`, and `d` to target a desired overall diameter and height.

### Rod families

**Family F1 — Top fan rods (T to U nodes)**  
- Count: 6  
- Length (symbolic): `sqrt(r² + (h − d)²)`  
- All six are equal by symmetry.  
- These are the longest rods in the structure if h is large relative to r.

**Family F2 — Bottom fan rods (B to L nodes)**  
- Count: 6  
- Length (symbolic): `sqrt(r² + (h − d)²)`  
- Equal to F1 if the geometry is symmetric top-to-bottom (equal ring radii, equal latitude placement). This is the default assumption.  
- **If F1 = F2, these can be cut from a single stock length. This is a significant fabrication simplification.**

**Family F3 — Upper ring rods (U to adjacent U)**  
- Count: 6  
- Length (symbolic): `r` (chord length of a regular hexagon with circumradius r equals r exactly)  
- All six equal.

**Family F4 — Lower ring rods (L to adjacent L)**  
- Count: 6  
- Length (symbolic): `r` (same reasoning as F3)  
- Equal to F3. **F3 and F4 are the same length — one stock cut.**

**Family F5 — Belt rods (U to adjacent L)**  
- Count: 12  
- Length (symbolic): `sqrt(r² · (1 − cos60°·cos30° − sin60°·sin30°·cos(angle)) + (2d)²)` — or more practically, computed from the actual 3D coordinates of adjacent U and L nodes.  
- All 12 are equal by the 6-fold symmetry and the regular stagger.  
- Belt rods are likely shorter than fan rods and longer than ring rods, but this must be verified with actual coordinates. Do not assume without calculation.

### Summary

| Family | Rods | Equal to | Stock cuts needed |
|--------|------|----------|-------------------|
| F1 — Top fan | 6 | F2 | 1 length |
| F2 — Bottom fan | 6 | F1 | (same as F1) |
| F3 — Upper ring | 6 | F4 | 1 length |
| F4 — Lower ring | 6 | F3 | (same as F3) |
| F5 — Belt | 12 | — | 1 length |

**Minimum distinct rod lengths: 3** (fan, ring, belt), assuming symmetric geometry.  
**Total rods: 36**

### Practical note

For a first prototype, cut F1/F2 together, F3/F4 together, and F5 separately. Label each bundle before assembly. Belt rod length is the most sensitive to geometric error — cut one, dry-fit it between a U and L node before cutting all twelve.

---

## 6. Sail Logic

### Sail geometry

Each sail is a single triangular panel. The triangle spans diagonally from one apex to one upper ring node and one lower ring node. This diagonal span is not a structural stay — it is the plastic edge of the sail fabric only.

**Upper sails (from T):**  
T–U1–L1, T–U3–L3, T–U5–L5  
Three sails, every other sector, attached to T.

**Lower sails (from B):**  
B–L1–U2, B–L3–U4, B–L5–U6  
Three sails, the alternating sectors, attached to B.

### Why single triangles, not paired panels

The original build logic used paired adjacent triangles to form a pocket. For this rotor, the diagonal span of each sail already creates a pocket-like geometry because the sail fabric billows under wind pressure. The physical fabric is not flat — it curves between the three corner nodes. This produces drag capture without requiring explicit pocket seaming between two triangles.

If testing shows insufficient drag, the sail can be extended to cover the adjacent belt triangle as well, forming a true two-triangle pocket. This is a design iteration decision, not a geometry decision.

### Alternating pattern and aerodynamic logic

Upper sails (blue in the visualization) occupy sectors 1, 3, 5.  
Lower sails (green) occupy sectors 2, 4, 6.  
Open frame sectors alternate with sailed sectors all the way around.

This is a drag-based Savonius-style rotor. Wind pressure on the concave face of each sail drives that face away from the wind source. The open frame sectors on the return sweep present much lower drag area. The alternating upper/lower pattern means that at any rotation angle, approximately half the sailed faces are in the power stroke and half are returning, producing smoother torque than a single-sided design.

### Rotation direction

With wind arriving from the front, the rotor spins counter-clockwise when viewed from above. This is the direction in which open sail faces retreat from the wind source. If the generator produces reversed polarity in testing, reverse the output leads rather than the rotor geometry.

### Sectors to leave open

All six unsailed sectors remain open frame. This is intentional — they reduce return drag on the back stroke. Do not add sails to these sectors without testing the effect on rotation speed and balance.

### Tradeoffs

| Factor | Current design | Alternative |
|--------|---------------|-------------|
| Drag capture | Moderate — 6 single-triangle sails | Higher — 6 two-triangle pocket sails |
| Return drag | Low — open alternating sectors | Slightly higher with pocket sails |
| Rotational balance | Good — 3-fold symmetry each hemisphere | Maintained with paired pockets |
| Build complexity | Low — simple triangle panels | Higher — pocket seaming required |
| Starting torque in low wind | Lower — less sail area | Higher with pocket sails |

Start with single-triangle sails. Add paired pockets only if starting torque is insufficient.

### Sail placement is inferred from wind-rotor principles

The alternating sail pattern is a proposed prototype strategy based on Savonius rotor logic applied to this geometry. It has not been validated by wind tunnel testing or CFD analysis.

---

## 7. Build Sequence

### Stage 1 — Point model and graph validation

1. Print or draw the node-edge diagram with all 14 nodes labeled T, U1–U6, L1–L6, B.
2. Verify the belt connectivity table: each U node connects to two L nodes.
3. Confirm no T-to-L or B-to-U stays exist in the diagram.
4. Identify the three rod families (fan, ring, belt) and mark them with different colors on the diagram.
5. Count: 36 edges total. If your count differs, find the error before proceeding.

**Failure point:** Incorrect belt connectivity is the most common error. Double-check U1–L6 and U1–L1 before U2–L1 and U2–L2 and so on around the ring.

### Stage 2 — Hub prototyping

1. Decide on hub fabrication method: 3D printing is recommended for prototyping.
2. Design Hub U first (degree 5). It has the most complex angular geometry.
3. Print one Hub U and one Hub L. Test whether they are interchangeable before committing to six of each.
4. Design Apex Hub (degree 6) with central shaft bore.
5. Print one T hub and one B hub. Test whether they are interchangeable (rotated 30°).
6. Do not print all hubs until single-instance tests pass.

**Failure point:** Hub angle errors compound across the frame. A 2° error at each hub produces visible distortion by the time you close the ring. Verify angles from actual 3D coordinates before finalizing hub geometry.

### Stage 3 — Rod cutting

1. Choose a target outer diameter (ring radius `r`) and overall height.
2. Calculate the three rod lengths from the formulas in Section 5 using your chosen `r`, `h`, and `d` values.
3. Cut one rod of each family. Dry-fit each against the corresponding hub before cutting the full set.
4. Cut fan rods (F1/F2) as a single batch — 12 identical rods.
5. Cut ring rods (F3/F4) as a single batch — 12 identical rods.
6. Cut one belt rod (F5), test fit, then cut the remaining 11.

**Failure point:** Belt rod length is the most sensitive. A small error in `d` (vertical ring placement) changes all 12 belt rods. Measure twice, cut one, test before cutting all.

### Stage 4 — Dry-fit frame assembly

Recommended assembly order:

1. Mount T hub on shaft (top position, temporary). Do not fix permanently yet.
2. Attach all six top fan rods to T hub.
3. Attach U ring hubs to the fan rod ends.
4. Connect upper ring rods between adjacent U hubs (close the U hexagon).
5. Attach belt rods from each U hub downward to the L hub positions.
6. Attach L ring hubs to the belt rod ends.
7. Connect lower ring rods between adjacent L hubs (close the L hexagon).
8. Attach bottom fan rods from each L hub downward to B hub position.
9. Mount B hub on shaft at the bottom.
10. Check for twist, sag, and symmetry. Adjust before fixing any joints.

**Failure point:** If the U hexagon does not close cleanly (ring rod length error), do not force it. Recheck F3 rod length.

### Stage 5 — Shaft and bearing integration

1. Select shaft diameter based on load. For a prototype, 20–25mm steel or aluminium tube is adequate.
2. The shaft must extend beyond both T and B by enough to mount bearings and the generator.
3. Mount a bearing at the top of the support structure to carry radial load.
4. Mount a bearing at the bottom to carry both radial and axial (thrust) load.
5. The generator mounts below B on the shaft extension, or above T if top-drive is preferred.
6. The rotor frame (T hub through B hub) rotates with the shaft. The shaft rotates inside fixed bearings.
7. Alternatively, the shaft is fixed and the rotor rotates around it — in this case the hub bores must accommodate a rotating sleeve or bearing at T and B. This is mechanically simpler for the generator mount.

**Key decision:** Rotating shaft (shaft turns with rotor, bearings are in the support structure) versus fixed shaft (shaft is stationary, rotor rotates around it). Rotating shaft is simpler to build. Fixed shaft is easier to connect to a generator.

**Failure point:** Bearing alignment. If T and B bearings are not coaxial, the rotor will wobble under load. Use a jig or a lathe to ensure alignment before fixing bearing housings.

### Stage 6 — Sail mockup in paper or light fabric

1. Cut six triangular panels from paper or lightweight fabric.
2. Pin or tape three upper sails to: T–U1–L1, T–U3–L3, T–U5–L5.
3. Pin or tape three lower sails to: B–L1–U2, B–L3–U4, B–L5–U6.
4. Spin the rotor by hand. Observe whether sails billow in the correct direction.
5. Check that open sectors are fully open and not partially blocked by sail edges.
6. Observe rotational balance. Add small weights to any sector that drops when the rotor is stopped.

**Failure point:** Sail panels attached at the wrong nodes. The diagonal edge of each sail (T to L, or B to U) is fabric only — it must not be attached to a stay. If you find yourself attaching a sail corner to a node it should not reach, recheck the sail mapping.

### Stage 7 — Sail material installation

1. Select sail material (see Section 8).
2. Cut panels to fit the triangular face, adding 20–30mm hem allowance on all edges.
3. Hem all edges. Reinforce corners with webbing or grommets.
4. Attach sails using stainless lacing cord or nylon zip ties through grommets at each corner node.
5. Tension each sail evenly. Over-tensioning flattens the billow and reduces drag capture.
6. Seal any hem gaps against water ingress if the rotor will be exposed to rain.

### Stage 8 — Balancing and tuning

1. Mount the rotor on the shaft in its operating orientation.
2. Allow it to find its natural rest position. The heavy sector will sink.
3. Add small balancing weights (stainless nuts or lead sheet) to the light sectors until the rotor rests at any position without rotating under gravity alone.
4. Test in low wind first. Observe:
   - Starting wind speed (cut-in speed)
   - Direction of rotation (confirm counter-clockwise from above)
   - Any wobble or vibration
5. If cut-in speed is too high, consider adding paired pocket sails to increase drag area (see Section 6).
6. If vibration occurs at speed, recheck bearing alignment and rotational balance.

---

## 8. Materials and Fabrication

### Minimum viable prototype

| Component | Material | Notes |
|-----------|----------|-------|
| Rods / struts | Fiberglass tube or rod, 8–12mm diameter | Lightweight, stiff, easily cut with a pipe cutter or angle grinder. Carbon fibre is stiffer but more expensive and requires dust precautions when cutting. |
| Hubs | PLA or PETG 3D printed | PLA is sufficient for indoor or sheltered testing. PETG handles moisture better for outdoor use. Print at 40%+ infill for hub strength. |
| Sail material | Ripstop nylon, 40–70 gsm | Lightweight, available in multiple colours, holds shape under wind pressure, easily hemmed and grommeted. Spinnaker cloth is an alternative. |
| Fasteners | Nylon zip ties and stainless M3/M4 screws | Zip ties for prototyping speed. Screw fasteners for anything expected to last more than a few test sessions. |
| Shaft | Steel or aluminium round tube, 20–25mm OD | Steel for rigidity; aluminium if weight is a constraint. Must be straight to within 1mm over full length. |
| Bearings | Flanged radial ball bearings, ID matching shaft OD | One at top (radial load only), one at bottom (radial + axial). Standard 6200-series bearings are adequate for prototype loads. |
| Generator | Permanent magnet DC motor used as generator, or purpose-built axial flux generator | A salvaged treadmill motor (typically 90–180V DC, permanent magnet) works well for proof-of-concept. |
| Support structure | Steel angle iron or aluminium extrusion | Must be rigid enough to hold bearing housings coaxial under rotor load. |

### Durable outdoor version

| Component | Material | Upgrade reason |
|-----------|----------|----------------|
| Rods | Carbon fibre tube, epoxy-bonded end plugs | Higher stiffness-to-weight, better fatigue resistance |
| Hubs | Machined aluminium or glass-filled nylon | Weather resistance, precision angles, long-term durability |
| Sail material | Dacron sailcloth or UV-stabilised polyester | UV resistance, longer outdoor lifespan than ripstop nylon |
| Fasteners | Stainless A4 grade throughout | Corrosion resistance in outdoor exposure |
| Shaft | Cold-drawn steel, ground finish, 25mm OD | Consistent diameter for bearing fit |
| Bearings | Sealed stainless or ceramic-coated bearings | Weather resistance, reduced maintenance |
| Generator | Purpose-built axial flux permanent magnet alternator | Higher efficiency, lower cut-in speed, designed for the target RPM range |

### Notes on generator selection

A Savonius-style drag rotor turns relatively slowly compared to lift-based propeller turbines. Expect tip-speed ratios below 1.0. This means the generator must be selected for low RPM operation or a step-up gearbox must be used. Direct-drive axial flux generators wound for low RPM (50–200 RPM) are the most practical choice for a small prototype. Avoid generators designed for high-speed operation without a gearbox — they will not produce useful voltage at typical rotor speeds.

---

## 9. What Changed from the Original Build Logic

### What still applies

- Start from the point geometry first — done. The 14-vertex graph is the foundation.
- Define the node-edge graph before discussing materials — done. Sections 2 and 3 precede materials.
- Separate geometry, structure, sail placement, and shaft — done across sections 1–6.
- Use a minimal hub family count — target is 2–3 families. See Section 4.
- Group rods by repeated length families — 3 families, 36 rods. See Section 5.
- Prefer buildable approximation over pure theory — the symmetric bicupola geometry is a practical approximation, not a mathematically exact solid.
- Distinguish shape inspiration from functional surfaces — the geometry is bicupola-like in form; the sail logic is derived from Savonius rotor principles applied to this specific graph.

### What changed

- **Sail geometry:** The original build logic assumed paired adjacent triangles forming a pocket. This rotor uses single diagonal triangles. The diagonal sail edge (T–L or B–U) is fabric only, not a stay. This is a departure from the paired-pocket approach and should be tested before assuming it captures sufficient drag.

- **Shaft specification:** The original logic did not detail shaft and bearing infrastructure for power generation. This document adds a full shaft, bearing, and generator section because the rotor is intended to draw power, not just demonstrate rotation.

- **Sail count:** Six sails total (three upper, three lower) rather than a smaller paired set. The alternating upper/lower pattern is specific to this geometry's 30° stagger.

### What must be discarded

- Any assumption that the geometry is a standard named solid. It is not. Do not import construction logic from buckyballs, icosahedra, or classical bicupola without re-deriving it for this specific graph.
- Any assumption that T connects to L nodes via stays. It does not. T–L and B–U edges are sail fabric edges only.
- Any assumption that all hubs are the same. Apex hubs (degree 6) and ring hubs (degree 5) have different angular geometries.

---

## 10. Deliverables

### Build summary

The rotor is a 14-vertex, 36-edge, fully triangulated hexagonal frame with a vertical shaft through the top and bottom apex nodes. It carries six alternating triangular sails — three hanging from T into the middle belt, three rising from B into the middle belt — producing a Savonius-style drag differential that drives counter-clockwise rotation (viewed from above) in a front wind. The frame uses three distinct rod lengths and two to three hub families. Generator power is extracted from the rotating shaft below B or above T via a direct-drive low-RPM alternator or a step-up gearbox to a higher-speed generator.

### Bill of materials categories

1. Shaft (steel or aluminium tube, 1 piece, length = rotor height + bearing overhang top and bottom)
2. Apex hubs — T and B (2 units, degree-6, shaft-bored)
3. Upper ring hubs — U1–U6 (6 units, degree-5)
4. Lower ring hubs — L1–L6 (6 units, degree-5)
5. Fan rods — F1/F2 (12 units, all equal length)
6. Ring rods — F3/F4 (12 units, all equal length)
7. Belt rods — F5 (12 units, all equal length)
8. Sail panels (6 triangular panels, ripstop nylon or equivalent)
9. Sail attachment hardware (grommets, lacing cord or zip ties)
10. Bearings (2 units, matched to shaft OD)
11. Bearing housings or support structure
12. Generator unit
13. Electrical output wiring and rectifier (if AC generator used)
14. Balancing weights (small stainless hardware for fine balance)

### Next three diagrams or calculations needed

1. **Coordinate table:** Calculate exact 3D coordinates for all 14 nodes given chosen values of `r`, `h`, and `d`. Derive the three rod lengths (F1/F2, F3/F4, F5) numerically. This is the prerequisite for hub angle design and rod cutting.

2. **Hub angle diagram for Hub U:** Using the coordinate table, compute the exact angles between all five rods entering a U hub (one fan rod, two ring rods, two belt rods). This drives the 3D print geometry and is the most failure-prone fabrication step.

3. **Sail area and torque estimate:** Calculate the projected area of each sail triangle as a function of rotation angle. Sum across all six sails for a full rotation cycle. This gives a first-order estimate of torque at a given wind speed and identifies whether single-triangle sails are sufficient or whether paired-pocket sails are needed to reach the target cut-in speed.

---

*Document produced from the geometry developed in the rotor visualization session. All geometric claims are based on the 14-vertex graph as defined. Physical performance claims are first-order estimates and require prototype validation.*
