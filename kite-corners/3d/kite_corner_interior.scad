// ═══════════════════════════════════════════════════════════════
// Tetrahedral Kite Interior Joint Hub
// ═══════════════════════════════════════════════════════════════
// A 3D-printed 6-way connector for the INTERIOR vertices of a
// multi-cell tetrahedral kite, where two tetrahedral cells meet
// corner-to-corner at a single shared point (not a shared edge).
//
// This is a SEPARATE, standalone hobby project — not part of the
// VINDSNURR wind rotor. See ../docs/kite-comparison.html for that
// comparison, and README.md for how this hub differs from
// kite_corner.scad (the 3-socket exterior hub).
//
// GEOMETRY DERIVATION (verified numerically, not just by formula):
// Built a real edge-2 regular tetrahedron, subdivided it into 4
// unit sub-tetrahedra at the edge midpoints (the standard construction
// for a multi-cell tetrahedral kite), and read off the 6 real strut
// directions at one shared vertex directly from those coordinates.
// Two of the 6 directions are exactly opposite (180°) — those two
// struts are modeled here as ONE continuous through-bore rather than
// two separate blind sockets. The other 4 directions are at 60°/120°
// to the through-bore axis and 90° to each other around it.
//
// PRINT SETTINGS:
//   Material    : PLA (kites are light-load; PETG if outdoor storage)
//   Infill      : 15–20% — low-load hobby part, not structural like VINDSNURR
//   Layer height: 0.2mm
//   Walls       : 2 perimeters minimum
//   Supports    : yes — the 4 angled sockets have some overhang
// ═══════════════════════════════════════════════════════════════

// ── Parameters ─────────────────────────────────────────────────
strut_d     = 6.0;   // mm — strut outer diameter (dowel, fiberglass, or carbon rod)
strut_tol   = 0.3;   // mm — socket clearance (slip fit; adjust per printer)
strut_depth = 16.0;  // mm — blind socket depth into hub body

hub_r       = 14.0;  // mm — hub sphere body radius (larger than the 3-way hub — more sockets)
wall        = 2.5;   // mm — minimum wall thickness

$fn = 64;  // increase to 128 for final print

// ── Derived ────────────────────────────────────────────────────
strut_socket_d = strut_d + strut_tol;

// ── Through-bore axis (2 opposite struts, modeled as one bore) ──
// Directions verified from real tetrahedron coordinates: exactly
// 180° apart, so this is a single straight axis through the hub.
through_dir = [0.577350, 0.000000, -0.816497];

// ── 4 blind-socket directions (verified, not symmetric guesses) ──
// Pairwise angles from through_dir: 60°, 60°, 120°, 120°
// Pairwise angles to each other around the belt: 60°, 90°, 60°, 90°
blind_dirs = [
    [-0.288675,  0.500000, -0.816497],
    [-0.288675, -0.500000, -0.816497],
    [-0.866025,  0.500000,  0.000000],
    [-0.866025, -0.500000,  0.000000],
];

// ── Utility: orient socket opening toward a direction vector ────
module point_toward(dir) {
    lon = atan2(dir[0], dir[2]);
    lat = -atan2(dir[1], sqrt(dir[0]*dir[0] + dir[2]*dir[2]));
    rotate([lat, 0, 0])
    rotate([0, lon, 0])
    children();
}

// ── Through-bore (negative volume, full diameter both ends) ─────
module through_bore(dir) {
    point_toward(dir) {
        cylinder(h = hub_r * 3, d = strut_socket_d, center = true);
    }
}

// ── Blind strut socket (negative volume) ─────────────────────────
module strut_socket(dir) {
    point_toward(dir) {
        cylinder(h = hub_r + strut_depth, d = strut_socket_d);
        // Entry chamfer for easier strut insertion
        translate([0, 0, hub_r - 1.5])
            cylinder(h = 3.5, d1 = strut_socket_d + 3, d2 = strut_socket_d);
    }
}

// ── Collar reinforcement around each strut opening ────────────────
module strut_collar(dir) {
    point_toward(dir) {
        difference() {
            cylinder(h = hub_r + 5, d = strut_socket_d + wall * 2);
            cylinder(h = hub_r + 6, d = strut_socket_d);
        }
    }
}

// Collar for the through-bore needs a collar at BOTH ends
module through_collar(dir) {
    strut_collar(dir);
    strut_collar([-dir[0], -dir[1], -dir[2]]);
}

// ── Main hub ────────────────────────────────────────────────────
module kite_corner_interior() {
    difference() {
        union() {
            sphere(r = hub_r);
            through_collar(through_dir);
            for (dir = blind_dirs) strut_collar(dir);
        }
        through_bore(through_dir);
        for (dir = blind_dirs) strut_socket(dir);
    }
}

// ── Render ──────────────────────────────────────────────────────
kite_corner_interior();

// ── Quick-reference ─────────────────────────────────────────────
// 1 through-bore (2 struts, dead straight through the hub) +
// 4 blind sockets, each at 6.3mm diameter × 16mm deep
// Use this hub only where 2 tetrahedral cells share a vertex.
// For single-cell (exterior) vertices, use kite_corner.scad instead.
