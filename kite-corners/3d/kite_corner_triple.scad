// ═══════════════════════════════════════════════════════════════
// Tetrahedral Kite Triple Joint Hub
// ═══════════════════════════════════════════════════════════════
// A 3D-printed 9-way connector for vertices where THREE tetrahedral
// cells meet at a single shared point. These only occur in kites with
// enough layers stacked — a 3-layer, 10-cell kite (the classic
// Instructables build) never produces one, but a 4-layer, 20-cell
// kite does (12 such vertices), and any larger multi-layer build
// (like Bell's own large kites, which had far more than 3 layers)
// will have many more.
//
// This is a SEPARATE, standalone hobby project — not part of the
// VINDSNURR wind rotor. See ../docs/kite-comparison.html for that
// comparison, and README.md for how this hub differs from
// kite_corner.scad (3-socket, 1 cell) and kite_corner_interior.scad
// (6-socket, 2 cells).
//
// GEOMETRY DERIVATION (verified numerically against real coordinates,
// not derived by formula or by extrapolating the 2-cell case):
// Built a 4-layer, 20-cell tetrahedral assembly (10 base + 6 + 3 + 1,
// each layer's base triangle anchored exactly to the layer below's
// apex points), found all 12 vertices where exactly 3 cells meet, and
// confirmed all 12 have IDENTICAL geometry (same angle set, just
// rotated in space) — so one hub design covers every 3-cell vertex.
//
// At a 3-cell vertex, 9 struts meet (3 cells × 3 struts each). They
// split cleanly into two symmetric groups:
//   - 6 struts lie exactly in one equatorial plane, evenly spaced
//     every 60° — these pair up into 3 straight through-bores.
//   - 3 struts point out of that plane at 35.264° from the
//     perpendicular axis, evenly spaced every 120°, each sitting
//     exactly between two of the in-plane struts — these are 3
//     separate blind sockets, all on the same side.
// This was confirmed by checking that a 120° rotation about the
// hub's central axis exactly maps each blind socket onto the next,
// and a 60° rotation exactly maps each in-plane through-bore end
// onto the next — genuine 3-fold rotational symmetry, not visual
// approximation.
//
// KNOWN LIMIT: kites with even more layers can produce vertices where
// 4 or more cells meet at one point (verified: a 4-cell vertex has 12
// struts forming 6 through-bores, no blind sockets). This hub does
// NOT cover that case — it is only for exactly 3 cells meeting. See
// README.md for which vertex types exist at which layer counts.
//
// PRINT SETTINGS:
//   Material    : PLA (kites are light-load; PETG if outdoor storage)
//   Infill      : 15–20% — low-load hobby part, not structural like VINDSNURR
//   Layer height: 0.2mm
//   Walls       : 2 perimeters minimum
//   Supports    : yes — the 3 angled sockets have some overhang
// ═══════════════════════════════════════════════════════════════

// ── Parameters ─────────────────────────────────────────────────
// Default preset: 6mm rod. For a 1m+ kite, switch to the lightweight
// 4mm-rod preset instead — see FLIGHT.md "Weight budget" for why, and
// kite_corner.scad's parameter comment for the override syntax:
//   openscad -D 'strut_d=4.0' -D 'hub_r=11.0' -D 'wall=2.0' -D 'strut_depth=12.0' ...
strut_d     = 6.0;   // mm — strut outer diameter (dowel, fiberglass, or carbon rod)
strut_tol   = 0.3;   // mm — socket clearance (slip fit; adjust per printer)
strut_depth = 16.0;  // mm — blind socket depth into hub body

hub_r       = 16.0;  // mm — hub sphere body radius (largest of the 3 hubs — 9 openings)
wall        = 2.5;   // mm — minimum wall thickness

$fn = 64;  // increase to 128 for final print

// ── Derived ────────────────────────────────────────────────────
strut_socket_d = strut_d + strut_tol;

// ── 3 through-bore axes (6 struts, 3 straight lines) ─────────────
// All 3 lie in the hub's equatorial plane (z=0 in this local frame),
// spaced 60° apart in azimuth (0°, 60°, 120° — each axis's own
// opposite end is another 180° around, so only 3 distinct axes are
// needed to cover all 6 in-plane struts).
through_dirs = [
    [ 1.000000,  0.000000, 0.000000],
    [ 0.500000,  0.866025, 0.000000],
    [-0.500000,  0.866025, 0.000000],
];

// ── 3 blind-socket directions (verified, not symmetric guesses) ──
// Polar angle 35.264° from +Z, spaced 120° apart in azimuth, each
// sitting exactly between two adjacent through-bore ends.
blind_dirs = [
    [ 0.000000, -0.577350, 0.816497],
    [-0.500000,  0.288675, 0.816497],
    [ 0.500000,  0.288675, 0.816497],
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

// Collar for a through-bore needs a collar at BOTH ends
module through_collar(dir) {
    strut_collar(dir);
    strut_collar([-dir[0], -dir[1], -dir[2]]);
}

// ── Main hub ────────────────────────────────────────────────────
module kite_corner_triple() {
    difference() {
        union() {
            sphere(r = hub_r);
            for (dir = through_dirs) through_collar(dir);
            for (dir = blind_dirs) strut_collar(dir);
        }
        for (dir = through_dirs) through_bore(dir);
        for (dir = blind_dirs) strut_socket(dir);
    }
}

// ── Render ──────────────────────────────────────────────────────
kite_corner_triple();

// ── Quick-reference ─────────────────────────────────────────────
// 3 through-bores (6 struts total, dead straight through the hub) +
// 3 blind sockets, each at 6.3mm diameter × 16mm deep
// Use this hub only where exactly 3 tetrahedral cells share a vertex.
// For 1-cell (exterior) vertices, use kite_corner.scad instead.
// For 2-cell vertices, use kite_corner_interior.scad instead.
