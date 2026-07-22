// ═══════════════════════════════════════════════════════════════
// Tetrahedral Kite Corner Hub
// ═══════════════════════════════════════════════════════════════
// A 3D-printed 3-way corner connector for tetrahedral kite cells
// (Alexander Graham Bell's tetrahedral kite, 1899–1903).
//
// This is a SEPARATE, standalone hobby project — not part of the
// VINDSNURR wind rotor. It is only related by a shared structural
// idea (fully triangulated frames). See ../docs/kite-comparison.html
// for that comparison.
//
// One hub design. Every vertex of a tetrahedral kite cell is
// identical, so print this same part for every corner.
//
// A single tetrahedral cell needs 4 of these hubs and 6 struts.
// A multi-cell kite (e.g. the classic 10-cell arrangement described
// in README.md) uses the same 3-socket hub at every vertex — cells
// share a vertex by using one hub's sockets for struts belonging to
// different cells, same as the tied-string joints in a straw-built kite.
//
// PRINT SETTINGS:
//   Material    : PLA (kites are light-load; PETG if outdoor storage)
//   Infill      : 15–20% — this is a low-load hobby part, not structural like VINDSNURR
//   Layer height: 0.2mm
//   Walls       : 2 perimeters minimum
//   Supports    : not required — sockets open downward/outward, no overhangs
// ═══════════════════════════════════════════════════════════════

// ── Parameters ─────────────────────────────────────────────────
strut_d     = 6.0;   // mm — strut outer diameter (dowel, fiberglass, or carbon rod)
strut_tol   = 0.3;   // mm — socket clearance (slip fit; adjust per printer)
strut_depth = 16.0;  // mm — socket depth into hub body

hub_r       = 12.0;  // mm — hub sphere body radius
wall        = 2.5;   // mm — minimum wall thickness

$fn = 64;  // increase to 128 for final print

// ── Derived ────────────────────────────────────────────────────
strut_socket_d = strut_d + strut_tol;

// ── Rod directions from hub centre (unit vectors) ───────────────
// Three sockets symmetric about the vertical axis, spaced 120°
// apart in azimuth, tilted so every pair is at the tetrahedral
// vertex angle: arccos(1/3) ≈ 70.53°.
socket_dirs = [
    [ 0.666667,  0.000000, 0.745356],
    [-0.333333,  0.577350, 0.745356],
    [-0.333333, -0.577350, 0.745356],
];

// ── Utility: orient socket opening toward a direction vector ────
module point_toward(dir) {
    lon = atan2(dir[0], dir[2]);
    lat = -atan2(dir[1], sqrt(dir[0]*dir[0] + dir[2]*dir[2]));
    rotate([lat, 0, 0])
    rotate([0, lon, 0])
    children();
}

// ── Strut socket (negative volume — subtracted from hub) ────────
module strut_socket(dir) {
    point_toward(dir) {
        cylinder(h = hub_r + strut_depth, d = strut_socket_d);
        // Entry chamfer for easier strut insertion
        translate([0, 0, hub_r - 1.5])
            cylinder(h = 3.5, d1 = strut_socket_d + 3, d2 = strut_socket_d);
    }
}

// ── Collar reinforcement around each strut socket ────────────────
module strut_collar(dir) {
    point_toward(dir) {
        difference() {
            cylinder(h = hub_r + 5, d = strut_socket_d + wall * 2);
            cylinder(h = hub_r + 6, d = strut_socket_d);
        }
    }
}

// ── Main hub ────────────────────────────────────────────────────
module kite_corner() {
    difference() {
        union() {
            sphere(r = hub_r);
            for (dir = socket_dirs) strut_collar(dir);
        }
        for (dir = socket_dirs) strut_socket(dir);
    }
}

// ── Render ──────────────────────────────────────────────────────
kite_corner();

// ── Quick-reference ─────────────────────────────────────────────
// Strut sockets: 3, each at 6.3mm diameter × 16mm deep (adjust strut_tol if needed)
// Angle between any two sockets: 70.53° (tetrahedral vertex angle)
// Print qty: 4 per single tetrahedral cell (one per vertex)
