# VINDSNURR — 3D Print Files

Hexagonal Bicupola Wind Rotor · HBR-6-14V · Rev 1.1  
**Rotor: 1000mm diameter · 20mm aluminium shaft · 10mm rods**

---

## Files in this package

| File | Purpose | Print? |
|------|---------|--------|
| `vindsnurr_params.scad` | Shared parameters and geometry constants | No — library |
| `hub_apex.scad` | Hub T and Hub B (top and bottom apexes) | Yes — print 2 |
| `hub_ring.scad` | Hub U1–U6 and L1–L6 (outer ring nodes) | Yes — print 12 |
| `hub_test_jig.scad` | Socket fit and angle verification | **Print first** |
| `README.md` | This file | No |

---

## Software required

**OpenSCAD** (free) — https://openscad.org  
Open any `.scad` file → press **F6** to render → **File → Export → Export as STL**  
Increase `$fn` from 64 to 128 in each file before exporting final STL for smoother curves.

---

## Hardware to source before printing

| Item | Specification | Qty | Notes |
|------|---------------|-----|-------|
| Shaft | Aluminium round tube, **20mm OD** | 1 | Length = 1064mm rotor height + 300mm overhang each end = ~1665mm minimum |
| Bearings | **6204-2RS** — 20mm ID, 47mm OD, 14mm H | 2 | One per apex hub. Standard size, widely available. |
| Strut rods | Fiberglass or carbon tube, **10mm OD** | 36 | Cut to lengths below |
| Sail fabric | Ripstop nylon, ~1.5m² total | 6 panels | |
| Set screws | M4 × 8mm socket head | 4 | To lock T and B hubs on shaft |
| Epoxy | Structural two-part epoxy | 1 tube | For bonding rods into sockets |

---

## Rod cut list

| Family | Length | Qty | Connects | Cut strategy |
|--------|--------|-----|----------|--------------|
| F1/F2 — Fan rods | **610.4 mm** | 12 | T→U (6 rods) and B→L (6 rods) | One batch |
| F3/F4 — Ring rods | **500.0 mm** | 12 | U ring (6) and L ring (6) | One batch |
| F5 — Belt rods | **446.6 mm** | 12 | U↔L diagonal belt | **Cut one first, test, then cut eleven more** |

**Total: 36 rods.**

---

## Hub summary

| Hub | File | Qty to print | Notes |
|-----|------|-------------|-------|
| Apex (T and B) | `hub_apex.scad` | 2 | Identical geometry. Mount B rotated 30° on shaft. |
| Ring (U1–U6 and L1–L6) | `hub_ring.scad` | 12 | Identical geometry. L hubs flip 180° during assembly. |

**Only 2 hub designs total.** U and L ring hubs are the same part — confirmed by exact angle calculation.

---

## Step-by-step print procedure

### 1. Print the test jig first

Open `hub_test_jig.scad` and print. Three pieces come out:

**Piece A — Rod socket + shaft bore test**
- Insert a short offcut of your 10mm rod into the socket.
  - Too tight → increase `rod_tol` (currently 0.3mm)
  - Too loose → decrease `rod_tol`
  - Correct → slides in with light finger pressure, no wobble
- Insert your 20mm shaft through the shaft bore hole.
  - Should slide through cleanly without binding or rattling.

**Piece B — 120° angle jig**
- Insert two rod offcuts. They should spread apart at 120° (ring rod spacing).

**Piece C — 68° angle jig**
- Insert two rod offcuts. They should spread apart at 68° (belt rod spacing).

Update `rod_tol` in `hub_apex.scad` and `hub_ring.scad` before continuing.

---

### 2. Print one ring hub

Open `hub_ring.scad`, export STL, print one hub.  
Test-fit short rod offcuts into all five sockets. All five should accept rods without binding or cracking the hub.

---

### 3. Print one apex hub

Open `hub_apex.scad`, export STL, print one hub.

**Press-fit the bearing:**
- Use a vice with flat pads — do not hammer.
- The 6204-2RS bearing (20mm ID, 47mm OD) presses into the bearing seat.
- The bearing should seat firmly and not rattle.
- If too loose: reduce `bearing_tol` from 0.1mm to 0.05mm and reprint.
- If it will not seat: increase `bearing_tol` to 0.15mm and reprint.

Slide the 20mm shaft through the seated bearing to verify fit.

---

### 4. Print the full set

Once both single-unit tests pass:
- Print **12× ring hub** (`hub_ring.scad`)
- Print **2× apex hub** (`hub_apex.scad`)

Print settings for all production hubs:

| Setting | Value |
|---------|-------|
| Material | PETG (outdoor use) or PLA (indoor prototype) |
| Infill | 40% minimum — gyroid or honeycomb pattern |
| Layer height | 0.2mm |
| Wall perimeters | 4 minimum |
| Orientation — apex hub | Shaft axis vertical, bearing seat face up |
| Orientation — ring hub | Socket 0 (orientation flat notch) pointing up |
| Supports | Required on all hubs — rod sockets have overhangs |
| Bed adhesion | Brim recommended for apex hubs |

---

## Assembly orientation

### Apex hubs

**Hub T (top):**  
All six rod sockets point downward and outward toward U1–U6.  
Bearing presses into the top face seat.  
Shaft passes through from below.

**Hub B (bottom):**  
Identical physical hub to T.  
Mount on shaft **rotated 30°** relative to Hub T.  
This aligns B's sockets with L1–L6, which sit 30° offset from U1–U6.  
Mark the correct rotation angle on the shaft with a marker before fixing.

**Fixing hubs on shaft:**  
Drill a 3.3mm hole radially through the shaft collar after printing.  
Tap M4. File a flat on the shaft at each hub position.  
Insert M4 × 8mm set screw to lock.

---

### Ring hubs

**U hubs (upper ring — socket 0 points UP toward T):**
- Socket 0 (marked with orientation notch): fan rod → T
- Socket 1: ring rod → next U hub clockwise
- Socket 2: ring rod → next U hub counter-clockwise
- Socket 3: belt rod → L node clockwise of this U
- Socket 4: belt rod → L node counter-clockwise

**L hubs (lower ring — flip hub so socket 0 points DOWN toward B):**  
Same physical part. Flip 180° around the socket 1–2 axis during assembly.  
Socket 0 (fan rod) then points downward toward B.  
Belt sockets 3 and 4 point upward toward the U ring.

---

## Belt connectivity table

Verify this before bonding any rods. It is the most error-prone step.

| U hub | Belt → L (socket 3) | Belt → L (socket 4) |
|-------|---------------------|---------------------|
| U1 | L1 | L6 |
| U2 | L2 | L1 |
| U3 | L3 | L2 |
| U4 | L4 | L3 |
| U5 | L5 | L4 |
| U6 | L6 | L5 |

Each L hub receives exactly two belt rods from above. If any L hub has one or three, the belt connectivity is wrong.

---

## Bearing specification

**Standard choice for this rotor: 6204-2RS**

| Property | Value |
|----------|-------|
| Inner diameter | 20mm (matches shaft) |
| Outer diameter | 47mm (matches bearing seat in hub_apex.scad) |
| Height | 14mm |
| Static load rating | 11.2 kN |
| Type | Deep groove ball bearing, double-sealed |

Fits 2 per rotor (one in Hub T, one in Hub B).  
Source from any bearing supplier. SKF, NSK, FAG are reliable brands.  
Budget Chinese bearings are acceptable for a prototype — replace for permanent installation.

**Lighter alternative: 6004-2RS** — ID=20mm, OD=42mm, H=12mm  
Lower load rating. If using this, change `bearing_od = 42` and `bearing_h = 12` in `hub_apex.scad`.

---

## Geometry reference

Origin = rotor geometric centre (shaft midpoint at equatorial plane).  
Y-axis = vertical (up). T is at top, B is at bottom.

```
Node     X (mm)     Y (mm)      Z (mm)
T           0      +532.09        0
B           0      -532.09        0
U1          0      +181.99     +500.00
U2      +433.01    +181.99     +250.00
U3      +433.01    +181.99     -250.00
U4          0      +181.99     -500.00
U5      -433.01    +181.99     -250.00
U6      -433.01    +181.99     +250.00
L1      +250.00    -181.99     +433.01
L2      +500.00    -181.99         0
L3      +250.00    -181.99     -433.01
L4      -250.00    -181.99     -433.01
L5      -500.00    -181.99         0
L6      -250.00    -181.99     +433.01
```

---

## Adjusting dimensions

All key values are at the top of each `.scad` file.

To change shaft diameter: update `shaft_d` and `shaft_bore` in `hub_apex.scad` and the test jig. Also update `bearing_id`, `bearing_od`, `bearing_h` to match the correct bearing for the new shaft size.

To change rod diameter: update `rod_d` in all three files.

To change rotor size: recalculate node coordinates and rod lengths from the geometry (see `vindsnurr_params.scad`), then re-derive `rod_dirs` vectors in both hub files.

---

Open source · MIT licence · Rev 1.1
