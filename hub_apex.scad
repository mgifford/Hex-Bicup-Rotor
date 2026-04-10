// ═══════════════════════════════════════════════════════════════
// VINDSNURR — Apex Hub (T and B)
// ═══════════════════════════════════════════════════════════════
// Rotor: 1000mm diameter · 20mm aluminium shaft · 10mm rods
// Bearing: 6204-2RS  ID=20mm  OD=47mm  H=14mm
//
// Hub T and Hub B are IDENTICAL geometry.
// Mount Hub B rotated 30° on the shaft relative to Hub T.
//
// PRINT SETTINGS:
//   Material    : PETG (outdoor) or PLA (indoor prototype)
//   Infill      : 40% minimum, gyroid or honeycomb
//   Layer height: 0.2mm
//   Walls       : 4 perimeters minimum
//   Orientation : shaft axis vertical, bearing seat face up
//   Supports    : yes — required for rod socket overhangs
//
// BEARING INSTALLATION:
//   Press 6204-2RS bearing into the bearing seat before mounting
//   hub on shaft. Use a vice with a flat pad — do not hammer.
//   The shaft slides through the bearing inner race.
//   Fix hub position on shaft with an M4 set screw through the
//   shaft collar (drill and tap after printing, file a flat on shaft).
// ═══════════════════════════════════════════════════════════════

// ── Parameters ─────────────────────────────────────────────────
shaft_d       = 20.0;   // mm — aluminium shaft OD
shaft_bore    = 20.5;   // mm — clearance bore (shaft + 0.5mm)

bearing_od    = 47.0;   // mm — 6204-2RS outer diameter
bearing_h     = 14.0;   // mm — 6204-2RS height
bearing_tol   =  0.1;   // mm — press-fit tolerance (reduce to 0.05 if loose)

rod_d         = 10.0;   // mm — rod outer diameter
rod_tol       =  0.3;   // mm — socket clearance (adjust after test jig)
rod_depth     = 28.0;   // mm — socket depth

hub_r         = 28.0;   // mm — hub sphere body radius
wall          =  4.0;   // mm — minimum wall thickness

$fn = 64;  // increase to 128 for final print

// ── Derived ────────────────────────────────────────────────────
rod_socket_d   = rod_d + rod_tol;
bearing_seat_d = bearing_od + bearing_tol;

// ── Rod directions from hub centre (unit vectors) ───────────────
// Computed from exact 1000mm rotor geometry.
// All six rods leave the apex angling downward and outward equally.
// Adjacent rod angle: 48.36° | Skip-one angle: 90.37° | Opposite: 110.00°
rod_dirs = [
    [ 0.000000, -0.573576,  0.819152],  // → U1
    [ 0.709406, -0.573576,  0.409576],  // → U2
    [ 0.709406, -0.573576, -0.409576],  // → U3
    [ 0.000000, -0.573576, -0.819152],  // → U4
    [-0.709406, -0.573576, -0.409576],  // → U5
    [-0.709406, -0.573576,  0.409576],  // → U6
];

// ── Utility: orient socket opening toward a direction vector ────
module point_toward(dir) {
    lon = atan2(dir[0], dir[2]);
    lat = -atan2(dir[1], sqrt(dir[0]*dir[0] + dir[2]*dir[2]));
    rotate([lat, 0, 0])
    rotate([0, lon, 0])
    children();
}

// ── Rod socket (negative volume — subtracted from hub) ──────────
module rod_socket(dir) {
    point_toward(dir) {
        cylinder(h = hub_r + rod_depth, d = rod_socket_d);
        // Entry chamfer for easier rod insertion
        translate([0, 0, hub_r - 1.5])
            cylinder(h = 3.5, d1 = rod_socket_d + 4, d2 = rod_socket_d);
    }
}

// ── Collar reinforcement around each rod socket ─────────────────
module rod_collar(dir) {
    point_toward(dir) {
        difference() {
            cylinder(h = hub_r + 8, d = rod_socket_d + wall * 2);
            cylinder(h = hub_r + 9, d = rod_socket_d);
        }
    }
}

// ── Bearing seat and shaft bore (negative volume) ───────────────
// Bearing seat is a stepped pocket on the top face.
// Shaft bore passes through the entire hub vertically.
module bearing_and_shaft() {
    // Full shaft bore
    cylinder(h = hub_r * 3, d = shaft_bore, center = true);

    // Bearing seat — recessed pocket on top (+Z) face
    // Bearing presses in from above; retaining lip is the hub body.
    translate([0, 0, hub_r - bearing_h])
        cylinder(h = bearing_h + 2, d = bearing_seat_d);

    // Optional second bearing seat on bottom face if stacking two bearings
    // (uncomment if using a duplex bearing arrangement)
    // mirror([0, 0, 1])
    //   translate([0, 0, hub_r - bearing_h])
    //     cylinder(h = bearing_h + 2, d = bearing_seat_d);
}

// ── Shaft collar (positive volume) ─────────────────────────────
// Cylindrical extension along the shaft axis for bearing registration
// and set-screw location.
module shaft_collar() {
    // Upper collar — bearing housing
    cylinder(h = hub_r + bearing_h + 2,
             d = bearing_seat_d + wall * 2);
    // Lower collar — shaft grip
    mirror([0, 0, 1])
        cylinder(h = hub_r * 0.5,
                 d = bearing_seat_d + wall * 2);
}

// ── Set screw boss ──────────────────────────────────────────────
// A flat-sided boss on the shaft collar for drilling/tapping M4.
// Drill radially through after printing. Tap M4.
// File a flat on the shaft at the hub position to prevent rotation.
module setscrew_boss() {
    translate([bearing_seat_d / 2 + wall, 0, hub_r * 0.3])
        rotate([0, 90, 0])
            cylinder(h = 10, d = 12);
}

// ── Main hub ────────────────────────────────────────────────────
module apex_hub() {
    difference() {
        union() {
            sphere(r = hub_r);
            shaft_collar();
            for (dir = rod_dirs) rod_collar(dir);
            setscrew_boss();
        }
        for (dir = rod_dirs) rod_socket(dir);
        bearing_and_shaft();
        // Flat on set screw boss for drill entry
        translate([bearing_seat_d / 2 + wall + 8, -6, hub_r * 0.3 - 6])
            cube([6, 12, 12]);
    }
}

// ── Render ──────────────────────────────────────────────────────
apex_hub();

// ── Quick-reference ─────────────────────────────────────────────
// Bearing  : 6204-2RS  ID=20  OD=47  H=14  (standard series)
// Shaft    : 20mm OD aluminium tube
// Set screw: M4 × 8mm socket head, radial through collar
// Rod sockets: 10.3mm diameter × 28mm deep (adjust rod_tol if needed)
// Print qty: 2 (Hub T and Hub B — same file, same print)
