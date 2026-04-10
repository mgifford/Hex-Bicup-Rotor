// ═══════════════════════════════════════════════════════════════
// VINDSNURR — Hub Test Jig
// ═══════════════════════════════════════════════════════════════
// Print this BEFORE printing any production hubs.
//
// Three test pieces printed in one go:
//   A — Socket fit test: verifies rod_tol is correct for your printer
//   B — 120° angle jig: verifies ring rod spacing
//   C — 68° angle jig:  verifies belt rod spacing
//
// Also includes a shaft bore test to verify the 20mm shaft fits.
//
// PROCEDURE:
//   1. Print this file.
//   2. Insert a short offcut of your 10mm rod into piece A.
//      — Too tight: increase rod_tol (currently 0.3mm)
//      — Too loose: decrease rod_tol
//      — Correct: slides in with light finger pressure, no wobble
//   3. Insert two rod offcuts into piece B. Angle should be 120°.
//   4. Insert two rod offcuts into piece C. Angle should be 68°.
//   5. Insert the 20mm shaft into the shaft bore test in piece A.
//      — Should slide through without play.
//   6. Adjust rod_tol and shaft_bore in hub files if needed.
//   7. Only then print production hubs.
// ═══════════════════════════════════════════════════════════════

rod_d      = 10.0;
rod_tol    =  0.3;   // <-- adjust until rod fits correctly
rod_depth  = 28.0;
shaft_d    = 20.0;   // mm — shaft outer diameter
shaft_bore = 20.5;   // mm — bore in hub (shaft + 0.5mm clearance)
$fn        = 48;

rod_socket_d = rod_d + rod_tol;

// ── Piece A: Socket and shaft bore test ─────────────────────────
module socket_test() {
    difference() {
        cube([44, 30, rod_depth + 10]);

        // Rod socket
        translate([15, 15, 6])
            cylinder(h = rod_depth + 2, d = rod_socket_d);
        translate([15, 15, 4])
            cylinder(h = 4, d1 = rod_socket_d + 4, d2 = rod_socket_d);

        // Shaft bore test — vertical through the block
        translate([34, 15, 0])
            cylinder(h = rod_depth + 12, d = shaft_bore);
    }
    // Labels
    translate([1, 0, 0])
        linear_extrude(1.5)
            text("ROD", size = 4, halign = "left");
    translate([26, 0, 0])
        linear_extrude(1.5)
            text("SHAFT", size = 4, halign = "left");
}

// ── Piece B: 120° ring rod angle jig ────────────────────────────
module angle_jig(angle_deg, label) {
    a   = angle_deg;
    arm = 28;
    difference() {
        hull() {
            cylinder(h = 14, d = 22);
            translate([arm * cos(0),   arm * sin(0),   0]) cylinder(h = 14, d = 14);
            translate([arm * cos(a),   arm * sin(a),   0]) cylinder(h = 14, d = 14);
        }
        // Socket 1
        translate([arm * cos(0), arm * sin(0), 3])
            cylinder(h = rod_depth, d = rod_socket_d);
        // Socket 2
        translate([arm * cos(a), arm * sin(a), 3])
            cylinder(h = rod_depth, d = rod_socket_d);
        // Label recess
        translate([0, 4, 12])
            linear_extrude(3)
                text(label, size = 5, halign = "center", valign = "center");
    }
}

// ── Layout: all pieces side by side ─────────────────────────────
// Piece A — socket + shaft test
socket_test();

// Piece B — 120° ring rod angle
translate([52, 0, 0])
    angle_jig(120, "120");

// Piece C — 68° belt rod angle
translate([116, 0, 0])
    angle_jig(68.08, "68");
