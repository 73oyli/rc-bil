// 4WD FPV-bil med hjuloppheng og styring – parametrisk (OpenSCAD)
// Aksavstand økt til 300 mm. Mål i mm.
// X = kjøreretning, Y = bredde, Z = opp.

// ---------------- hovedmål ----------------
/* [Hovedmål] */
wheel_D      = 100;     // [60:120]
wheel_W      = 32;      // [20:50]
wheelbase    = 300;     // [200:400]
track        = 210;     // [150:260]
tube         = 30;      // [20:40]
wall         = 2;       // [1:4]
plate_t      = 3;       // [2:6]
frame_L      = 380;     // [250:500]
frame_W      = 200;     // [140:260]
clearance    = 30;      // [10:60]
arm_len      = 50;      // [30:80]
shock_len    = 70;      // [40:100]
travel       = 20;      // [5:40]

/* [Styring] */
// Dra i skyveknappen: negativ = sving venstre, positiv = sving hoyre
steer_angle = 0;        // [-30:30:1]
show_steering = true;   // [true, false]

/* [Fjaering] */
// Fjaeringsvei: 0 = utslatt, 20 = sammenklemt
susp_travel = 0;        // [0:20:1]
// Bump-stop: maks innfjaering foer hardt stopp
bump_stop = 15;         // [8:20:1]

/* [Hjulvinkler] */
// Camber: negativ = toppen av hjulet heller innover (vanligst)
camber_angle = 0;       // [-10:10:0.5]
// Toe: positiv = toe-in paa bakhjulene
toe_angle = 0;          // [-5:5:0.5]

// Ackermann: cot(ytre) = cot(indref) + sporvidde/aksavstand
function ackermann_outer(inner) =
    atan(1 / (1 / tan(inner) + track / wheelbase));

// ---------------- ramme ----------------
module alu_tube(len) {
    difference() {
        cube([len, tube, tube], center=true);
        cube([len + 2, tube - 2 * wall, tube - 2 * wall], center=true);
    }
}

module frame() {
    z = clearance + tube / 2;
    for (y = [-track / 2 + tube / 2 + 8, track / 2 - tube / 2 - 8])
        translate([0, y, z]) alu_tube(frame_L);
    for (x = [-frame_L / 2 + tube / 2, 0, frame_L / 2 - tube / 2])
        translate([x, 0, z]) rotate([0, 0, 90]) alu_tube(frame_W - 2 * tube + 40);
    translate([0, 0, clearance + tube + plate_t / 2])
        cube([frame_L, frame_W, plate_t], center=true);
}

// ---------------- demper med fjaer og bump-stop ----------------
// Demperlegeme + spiralfjaer + progressiv bump-stop (TPU).
// t = aktuell innfjaering (mm). Bump-stoppen blir kortere naar t naermer seg bump_stop.
module damper(p1, p2, t) {
    v   = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]];
    L   = norm(v);
    ax  = [-v[1], v[0], 0];
    ang = acos(v[2] / L);
    translate(p1) rotate(a = ang, v = ax) {
        // demperlegeme
        cylinder(d = 10, h = L);
        // spiralfjaer (9 ringer)
        for (i = [0:8])
            translate([0, 0, L * (i + 0.6) / 9.2])
                rotate_extrude() translate([9, 0]) circle(r = 1.3);
        // bump-stop: hoeyde avtar med innfjaering
        bs = max(1.5, bump_stop - t);
        translate([0, 0, L * 0.16]) color([0.85, 0.1, 0.1]) cylinder(d = 14, h = bs);
    }
}

// ---------------- hjuloppheng (enkelt, visuelt) ----------------
module suspension_corner(sx, sy) {
    // sx = ±1 (foran/bak), sy = ±1 (venstre/høyre)
    x = sx * wheelbase / 2;
    y = sy * track / 2;

    // Fjaering: susp_travel = 0 (utslatt) .. bump_stop (hardt stopp).
    // Hjulsenteret loefter seg og vandrer litt innover paa buen.
    t   = min(susp_travel, bump_stop);
    piv_z = clearance + 10;
    dz0 = wheel_D / 2 - piv_z;                 // hoejde pivot->senter ved 0
    dz  = dz0 + t;
    dx  = sqrt(max(0.01, arm_len * arm_len - dz * dz));
    hub_x = x - sx * (arm_len - dx);
    hub_z = wheel_D / 2 + t;

    // baereearm: to stag fra ramme til hjulsenter
    for (dy = [-12, 12]) {
        hull() {
            translate([x - sx * arm_len, sy * (track / 2 - tube / 2), piv_z])
                sphere(d=8);
            translate([hub_x, y + dy, hub_z])
                sphere(d=8);
        }
    }
    // demper + fjaer + bump-stop
    damper(
        [x - sx * 20, sy * (track / 2 - tube / 2), clearance + tube + plate_t],
        [hub_x - sx * 5, sy * (track / 2 - 20), hub_z + 10],
        t
    );
    // Forhjul dreies om Z etter Ackermann.
    // steer_angle > 0 = sving hoyre (sett ovenfra, +X er framover).
    // Indre hjul = det som svinger mest.
    inner = abs(steer_angle);
    outer = ackermann_outer(inner);
    ang = (show_steering && sx > 0 && inner > 0.001)
        ? (steer_angle > 0
            ? (sy < 0 ? -inner : -outer)
            : (sy > 0 ?  inner :  outer))
        : 0;

    // Toe paa bakhjul: positiv = toe-in (forhjulene peker innover)
    toe   = (sx < 0) ? -sy * toe_angle : 0;
    // Camber: negativ verdi = toppen av hjulet heller innover
    camb  = -sy * camber_angle;

    translate([hub_x, y, hub_z])
        rotate([0, 0, ang + toe])
        rotate([camb, 0, 0])
        wheel();
}

// Hjul: sylinder har akse langs Z som standard.
// rotate([90,0,0]) roterer 90 grader om X -> akselen ligger langs Y (tverrskips).
// Resultat: hjulet ruller i X-retning (kjoreretning) - dette er RIKTIG.
module wheel() {
    rotate([90, 0, 0]) {
        // dekk (slitebane)
        difference() {
            cylinder(d=wheel_D, h=wheel_W, center=true);
            cylinder(d=wheel_D - 14, h=wheel_W + 2, center=true);
        }
        // nav / motorklokke
        cylinder(d=44, h=wheel_W + 6, center=true);
    }
}

// ---------------- styring (foraksel) ----------------
module steering() {
    z = clearance + 20;
    // servo sentralt foran
    translate([wheelbase / 2 - 45, 0, clearance + tube + plate_t + 20])
        cube([40, 20, 38], center=true);
    // styrestag ut til hver side
    for (sy = [-1, 1])
        hull() {
            translate([wheelbase / 2 - 45, sy * 12, z])
                sphere(d=6);
            translate([wheelbase / 2 + 10, sy * (track / 2 - 30), z])
                sphere(d=6);
        }
    // spindler
    for (sy = [-1, 1])
        translate([wheelbase / 2 + 10, sy * (track / 2 - 30), z])
            cylinder(d=12, h=40, center=true);
}

// ---------------- pan/tilt-gimbal for FPV-kamera ----------------
module gimbal() {
    x = wheelbase / 2 + 30;
    zb = clearance + tube + plate_t;
    // mast
    translate([x, 0, zb + 30]) cylinder(d=8, h=60);
    // pan-servo
    translate([x, 0, zb + 65]) cube([23, 12, 23], center=true);
    // tilt-brakett
    translate([x + 8, 0, zb + 85]) cube([6, 30, 20], center=true);
    // tilt-servo
    translate([x + 14, 0, zb + 90]) cube([23, 12, 23], center=true);
    // kamera
    translate([x + 30, 0, zb + 90]) cube([25, 25, 25], center=true);
}

// ---------------- komponenter ----------------
module battery() {
    for (y = [-batt_w / 2 - 2, batt_w / 2 + 2])
        translate([0, y, clearance + tube + plate_t + 25])
            cube([150, 50, 50], center=true);
}
batt_w = 50;

module fc() { translate([40, 0, clearance + tube + plate_t + 3]) cube([30.5, 30.5, 4], center=true); }
module escs() {
    for (x = [-110, 110]) for (y = [-60, 60])
        translate([x, y, clearance + tube + plate_t + 6])
            cube([40, 24, 12], center=true);
}

// ---------------- montering ----------------
frame();
for (sx = [-1, 1]) for (sy = [-1, 1]) suspension_corner(sx, sy);
steering();
gimbal();
battery();
fc();
escs();

$fn = 48;
