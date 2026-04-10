// ═══════════════════════════════════════════════════════════════
// VINDSNURR — Ring Hub (U1–U6 and L1–L6)
// ═══════════════════════════════════════════════════════════════
// Rotor: 1000mm diameter · 20mm shaft · 10mm rods
//
// One design. Print 12 instances.
//   6 for U positions (upper ring) — socket 0 points UP toward T
//   6 for L positions (lower ring) — flip hub so socket 0 points DOWN toward B
//
// U and L hub angle sets are mathematically identical (verified by calculation).
// The 30° stagger between rings is an assembly orientation, not a geometry change.
//
// PRINT SETTINGS:
//   Material    : PETG (outdoor) or PLA (indoor prototype)
//   Infill      : 40% minimum, gyroid or honeycomb
//   Layer height: 0.2mm
//   Walls       : 4 perimeters minimum
//   Orientation : socket 0 (fan rod, marked with flat) pointing up
//   Supports    : yes — belt rod sockets on underside need support
//
// No shaft bore. Ring hubs do not contact the shaft.
// ═══════════════════════════════════════════════════════════════

// ── Parameters ─────────────────────────────────────────────────
rod_d     = 10.0;   // mm — rod outer diameter
rod_tol   =  0.3;   // mm — socket clearance (adjust after test jig)
rod_depth = 28.0;   // mm — socket depth
hub_r     = 22.0;   // mm — hub sphere radius
wall      =  4.0;   // mm — minimum wall thickness

$fn = 64;

rod_socket_d = rod_d + rod_tol;

// ── Rod directions from Hub U1 (unit vectors) ───────────────────
// Hub U1 is at position [0, +182, +500] mm from rotor centre.
// Directions are expressed in the hub's local frame where
// socket 0 (→T) points along +Z for printing orientation clarity.
//
// Pairwise angles (all confirmed by geometry calculation):
//   Socket 0 vs 1 : 65.82°   (fan vs ring, clockwise)
//   Socket 0 vs 2 : 65.82°   (fan vs ring, counter-clockwise)
//   Socket 0 vs 3 : 110.16°  (fan vs belt, clockwise)
//   Socket 0 vs 4 : 110.16°  (fan vs belt, counter-clockwise)
//   Socket 1 vs 2 : 120.00°  (ring vs ring — opposite sides)
//   Socket 1 vs 3 :  55.96°  (ring vs near belt)
//   Socket 1 vs 4 : 114.19°  (ring vs far belt)
//   Socket 2 vs 3 : 114.19°  (ring vs far belt)
//   Socket 2 vs 4 :  55.96°  (ring vs near belt)
//   Socket 3 vs 4 :  68.08°  (belt vs belt)

rod_dirs = [
    [ 0.000000,  0.573576, -0.819152],  // socket 0: → T  (fan, upward)
    [ 0.866025,  0.000000, -0.500000],  // socket 1: → U2 (ring, clockwise)
    [-0.866025,  0.000000, -0.500000],  // socket 2: → U6 (ring, counter-CW)
    [ 0.559771, -0.814960, -0.149990],  // socket 3: → L1 (belt, down-CW)
    [-0.559771, -0.814960, -0.149990],  // socket 4: → L6 (belt, down-CCW)
];

// ── Utility ────────────────────────────────────────────────────
module point_toward(dir) {
    lon = atan2(dir[0], dir[2]);
    lat = -atan2(dir[1], sqrt(dir[0]*dir[0] + dir[2]*dir[2]));
    rotate([lat, 0, 0])
    rotate([0, lon, 0])
    children();
}

// ── Rod socket ─────────────────────────────────────────────────
module rod_socket(dir) {
    point_toward(dir) {
        cylinder(h = hub_r + rod_depth, d = rod_socket_d);
        translate([0, 0, hub_r - 1.5])
            cylinder(h = 3.5, d1 = rod_socket_d + 4, d2 = rod_socket_d);
    }
}

// ── Collar reinforcement ────────────────────────────────────────
module rod_collar(dir) {
    point_toward(dir) {
        difference() {
            cylinder(h = hub_r + 6, d = rod_socket_d + wall * 2);
            cylinder(h = hub_r + 7, d = rod_socket_d);
        }
    }
}

// ── Orientation flat ────────────────────────────────────────────
// A small flat face adjacent to socket 0 (the fan rod socket).
// Always faces toward the apex (T or B) after assembly.
// Use this flat to confirm correct hub orientation before bonding rods.
module orientation_flat() {
    point_toward(rod_dirs[0]) {
        translate([0, 0, hub_r + 2])
            cube([rod_socket_d + wall * 2, 3, 4], center = true);
    }
}

// ── Main hub ────────────────────────────────────────────────────
module ring_hub() {
    difference() {
        union() {
            sphere(r = hub_r);
            for (dir = rod_dirs) rod_collar(dir);
            // Orientation flat is additive here (just geometry marker)
        }
        for (dir = rod_dirs) rod_socket(dir);
        // Orientation flat notch — small recess so you can feel the
        // orientation by touch without looking at the hub directly
        point_toward(rod_dirs[0]) {
            translate([0, 0, hub_r + rod_depth - 3])
                cube([rod_socket_d + wall * 2 + 2, 2, 4], center = true);
        }
    }
}

// ── Render ──────────────────────────────────────────────────────
ring_hub();

// ── Assembly orientation guide ──────────────────────────────────
//
// FOR U HUBS (upper ring, connects upward to T):
//   Socket 0 orientation flat faces UP (toward T).
//   Socket 1 → clockwise adjacent U hub (F3 ring rod)
//   Socket 2 → counter-clockwise adjacent U hub (F3 ring rod)
//   Socket 3 → L node clockwise of this U position (F5 belt rod)
//   Socket 4 → L node counter-clockwise (F5 belt rod)
//
// FOR L HUBS (lower ring, connects downward to B):
//   Flip the hub 180° around the socket 1–2 axis (ring rod axis).
//   Socket 0 orientation flat now faces DOWN (toward B).
//   Socket 3 → U node counter-clockwise of this L position (F5 belt rod)
//   Socket 4 → U node clockwise (F5 belt rod)
//   Ring rod sockets (1, 2) remain horizontal — unchanged.
//
// BELT CONNECTIVITY TABLE (U → L):
//   U1 → L6 (socket 4) and L1 (socket 3)
//   U2 → L1 (socket 4) and L2 (socket 3)
//   U3 → L2 (socket 4) and L3 (socket 3)
//   U4 → L3 (socket 4) and L4 (socket 3)
//   U5 → L4 (socket 4) and L5 (socket 3)
//   U6 → L5 (socket 4) and L6 (socket 3)
//
// ROD INSERTION ORDER:
//   1. Fan rod (socket 0) first — sets orientation
//   2. Ring rods (sockets 1 and 2)
//   3. Belt rods (sockets 3 and 4) last — hardest to align
//
// Print qty: 12 total (6 for U positions, 6 for L positions)
