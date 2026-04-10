// ═══════════════════════════════════════════════════════════════
// VINDSNURR — Master Parameters
// ═══════════════════════════════════════════════════════════════
// Shared geometry constants for the 14-vertex hexagonal rotor.
// Include this file at the top of any hub or jig file with:
//   include <vindsnurr_params.scad>
//
// All dimensions in millimetres.
// Rotor: 1000mm diameter · 20mm aluminium shaft · 10mm rods
// ═══════════════════════════════════════════════════════════════

// ── Rotor geometry ─────────────────────────────────────────────
ROTOR_DIAMETER   = 1000.0;   // mm — overall rotor diameter
RING_RADIUS      = 500.0;    // mm — horizontal distance shaft → U or L node
RING_LAT_DEG     = 20.0;     // degrees — latitude of U/L rings on sphere
SPHERE_R         = 532.09;   // mm — sphere radius (computed)
RING_HEIGHT      = 181.99;   // mm — vertical distance equator → U or L ring
APEX_HEIGHT      = 532.09;   // mm — vertical distance equator → T or B apex
ROTOR_HEIGHT     = 1064.2;   // mm — total T to B height

// ── Rod lengths (cut list) ─────────────────────────────────────
F1_LENGTH = 610.4;   // mm — fan rods T→U and B→L  (12 rods, one batch)
F3_LENGTH = 500.0;   // mm — ring rods U→U and L→L (12 rods, one batch)
F5_LENGTH = 446.6;   // mm — belt rods U↔L         (12 rods, cut 1 first)

// ── Hardware ───────────────────────────────────────────────────
SHAFT_OD         = 20.0;    // mm — aluminium shaft outer diameter
SHAFT_BORE       = 20.5;    // mm — clearance bore through hub (shaft + 0.5mm)

ROD_OD           = 10.0;    // mm — strut/rod outer diameter
ROD_TOL          = 0.3;     // mm — socket clearance (slip fit for bonding)
ROD_DEPTH        = 28.0;    // mm — socket depth into hub body

// Bearing: 6204-2RS (standard, widely available, suits 20mm shaft)
//   Inner diameter  = 20mm  (matches SHAFT_OD)
//   Outer diameter  = 47mm
//   Height          = 14mm
//   Load rating     = 11.2 kN static
BEARING_ID       = 20.0;    // mm
BEARING_OD       = 47.0;    // mm
BEARING_H        = 14.0;    // mm
BEARING_TOL      = 0.1;     // mm — press-fit tolerance (tight)

// Alternative lighter bearing: 6004-2RS
//   ID=20mm  OD=42mm  H=12mm — lighter, lower load rating
//   Suitable for prototype testing. Change BEARING_OD=42, BEARING_H=12.

// ── Hub body ───────────────────────────────────────────────────
APEX_HUB_R       = 28.0;    // mm — apex hub sphere body radius
RING_HUB_R       = 22.0;    // mm — ring hub sphere body radius
HUB_WALL         = 4.0;     // mm — minimum wall / collar thickness

// ── Hub counts ─────────────────────────────────────────────────
APEX_HUB_COUNT   = 2;    // T and B — same geometry, mount 30° apart on shaft
RING_HUB_COUNT   = 12;   // U1–U6 and L1–L6 — same geometry, different orientation

// ── Hub angles (degrees) — for reference and quality check ─────
// Apex hub (T or B):
APEX_ADJ_ANGLE   = 48.36;   // T→U1 vs T→U2 (neighbouring rods)
APEX_SKIP_ANGLE  = 90.37;   // T→U1 vs T→U3 (one apart)
APEX_OPP_ANGLE   = 110.00;  // T→U1 vs T→U4 (opposite)

// Ring hub (U or L) — all pairwise angles:
RING_T_TO_RING   = 65.82;   // U1→T  vs U1→U2  (fan rod vs ring rod)
RING_T_TO_BELT   = 110.16;  // U1→T  vs U1→L1  (fan rod vs belt rod)
RING_RING_RING   = 120.00;  // U1→U2 vs U1→U6  (ring rod vs ring rod)
RING_RING_BELT_N = 55.96;   // U1→U2 vs U1→L1  (ring rod vs near belt rod)
RING_RING_BELT_F = 114.19;  // U1→U2 vs U1→L6  (ring rod vs far belt rod)
RING_BELT_BELT   = 68.08;   // U1→L1 vs U1→L6  (belt rod vs belt rod)

// ── Node coordinates (mm) ──────────────────────────────────────
// Origin = rotor geometric centre (shaft midpoint, equatorial plane)
// Y-axis = vertical (up). T at top, B at bottom.
//
// T  = [    0,   +532.09,      0   ]
// B  = [    0,   -532.09,      0   ]
// U1 = [    0,   +181.99,  +500.00 ]
// U2 = [+433.01, +181.99,  +250.00 ]
// U3 = [+433.01, +181.99,  -250.00 ]
// U4 = [    0,   +181.99,  -500.00 ]
// U5 = [-433.01, +181.99,  -250.00 ]
// U6 = [-433.01, +181.99,  +250.00 ]
// L1 = [+250.00, -181.99,  +433.01 ]
// L2 = [+500.00, -181.99,      0   ]
// L3 = [+250.00, -181.99,  -433.01 ]
// L4 = [-250.00, -181.99,  -433.01 ]
// L5 = [-500.00, -181.99,      0   ]
// L6 = [-250.00, -181.99,  +433.01 ]
