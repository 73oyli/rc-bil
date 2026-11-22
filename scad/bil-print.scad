// 4WD FPV-bil - FULLT 3D-PRINTBART CHASSIS (PETG/ASA/TPU)
// Erstatter aluminiumsrammen. Mål i mm. X = kjøreretning, Y = bredde, Z = opp.
// Materialer: PETG/ASA til chassis+braketter, PA-CF eller ASA til armer/spindler,
// TPU 95A til dekk og bump-stop. Kun skruer, lager og aksler er metall.

// ================= PARAMETERE =================
/* [Chassis] */
frame_L     = 380;
frame_W     = 200;
plate_t     = 4;     // bunplate
rail_t      = 5;     // sidevegg
rail_h      = 26;    // sidevegg-hoyde
rib_n       = 6;     // antall ribber per side

/* [Hjul] */
wheel_D     = 100;
wheel_W     = 32;
wheelbase   = 300;
track       = 210;
tire_t      = 7;     // dekktjukkelse (TPU)

/* [Hjuloppheng] */
arm_len     = 55;
arm_t       = 8;     // armtykkelse
pivot_d     = 4.2;   // M4 pinneskrue
hub_d       = 8;     // lager/aksel

/* [Styring] */
steer_angle = 0;     // [-30:30:1]
camber_angle = 0;    // [-10:10:0.5]
toe_angle   = 0;     // [-5:5:0.5]

/* [Fjaering] */
susp_travel = 0;     // [0:20:1]
bump_stop   = 15;    // [8:20:1]

/* [Visning] */
view = "assembly";   // [assembly, layout, parts, chassis, tray, arm, knuckle, mount, servo, gimbal, hub, tire, bump]
show_bolts = true;   // [true, false]

// ================= HJELPERE =================
function ackermann_outer(inner) = atan(1 / (1 / tan(inner) + track / wheelbase));

module rounded_plate(L, Wd, t) {
    // plate med avrundede hjoerner (printes flatt)
    hull() {
        for (x = [-L/2 + 12, L/2 - 12])
            for (y = [-Wd/2 + 12, Wd/2 - 12])
                translate([x, y, t/2]) cylinder(d=24, h=t, center=true, $fn=32);
    }
}

/* [Toleranser] */
fit_clear    = 0.20;   // [0.10:0.40:0.05] klaring M3-skruer
insert_clear = 0.20;   // [0.00:0.40:0.05] klaring M3 varmepress-insert
pivot_clear  = 0.35;   // [0.20:0.50:0.05] klaring M4 pivot (bevegelig)

module m3_hole(h=12) { cylinder(d = 3.0 + fit_clear, h=h, center=true, $fn=20); }
module insert_hole(h=8) { cylinder(d = 4.0 + insert_clear, h=h, center=true, $fn=20); }
module pivot_hole(h=12) { cylinder(d = 4.0 + pivot_clear, h=h, center=true, $fn=24); }

// ================= CHASSIS =================
module rib() {
    // trekantribbe som printes staende (ingen support)
    linear_extrude(height = 4, center = true)
        polygon(points=[[0,0],[26,0],[0,22]]);
}

module chassis() {
    difference() {
        union() {
            rounded_plate(frame_L, frame_W, plate_t);
            // sidevegger
            for (sy = [-1, 1])
                translate([0, sy * (frame_W/2 - rail_t/2), plate_t + rail_h/2])
                    cube([frame_L, rail_t, rail_h], center=true);
            // ribber
            for (i = [0:rib_n-1])
                for (sy = [-1, 1]) {
                    x = -frame_L/2 + 40 + i * (frame_L - 80) / (rib_n - 1);
                    translate([x, sy * (frame_W/2 - rail_t - 2), plate_t + 1])
                        rotate([90, 0, 90]) rib();
                }
            // motorbaerebroer ut til hver side (printes som del av chassis)
            for (sx = [-1, 1])
                for (sy = [-1, 1])
                    translate([sx * wheelbase/2, sy * (track/2 - 26), plate_t / 2 + 1])
                        cube([46, 40, plate_t], center=true);
        }
        // hull: batterifeste, FC, servo, gimbal
        for (x = [-60, -20, 20, 60])
            for (y = [-30, 30])
                translate([x, y, 0]) insert_hole(plate_t + 4);
        // akselgjennomforinger
        for (sx = [-1, 1])
            for (sy = [-1, 1])
                translate([sx * wheelbase/2, sy * (track/2 - 26), 0])
                    cylinder(d=10, h=plate_t + 4, center=true, $fn=24);
        // vektbesparelse i platen
        for (x = [-120, -80, -40, 40, 80, 120])
            translate([x, 0, 0]) cylinder(d=18, h=plate_t + 2, center=true, $fn=24);
    }
}

// ================= BATTERTRAY =================
module battery_tray() {
    difference() {
        union() {
            cube([170, 120, 4], center=true);
            for (sy = [-1, 1])
                translate([0, sy * 56, 14]) cube([170, 5, 28], center=true);
        }
        // stroppespalter
        for (x = [-55, 55]) translate([x, 0, 0]) cube([12, 130, 6], center=true);
        for (x = [-70, 70]) translate([x, 0, 0]) m3_hole(8);
    }
}

// ================= BAEREARM =================
module suspension_arm() {
    difference() {
        hull() {
            cylinder(d = 16, h = arm_t, center=true);
            translate([arm_len, 0, 0]) cylinder(d = 16, h = arm_t, center=true);
        }
        // utsparinger
        for (x = [18, arm_len - 18])
            translate([x, 0, 0]) cylinder(d = 9, h = arm_t + 2, center=true, $fn=20);
        // pivot og nav
        translate([0, 0, 0]) pivot_hole(arm_t + 2);
        translate([arm_len, 0, 0]) cylinder(d = hub_d, h = arm_t + 2, center=true, $fn=24);
    }
}

// ================= SPINDEL / NAV =================
module knuckle() {
    difference() {
        union() {
            translate([0, 0, 0]) cylinder(d = 34, h = 22, center=true, $fn=36);
            translate([-6, -22, 0]) cube([12, 26, 14], center=true);  // styrearm
            translate([0, 24, 0]) cylinder(d = 18, h = 14, center=true, $fn=28); // demperfeste
        }
        // kingpin (M6)
        cylinder(d = 6.2, h = 30, center=true, $fn=24);
        // motorflens 4xM3
        for (p = [[-12.5,-12.5],[12.5,-12.5],[-12.5,12.5],[12.5,12.5]])
            translate([p[0], p[1], 0]) m3_hole(30);
        // senterhull for motoraksel
        cylinder(d = 14, h = 30, center=true, $fn=28);
        // demperfeste M3
        translate([0, 24, 0]) rotate([90,0,0]) m3_hole(20);
        // styrearm M3
        translate([-6, -30, 0]) rotate([0,90,0]) m3_hole(16);
    }
}

// ================= MOTORFESTE (utrigger) =================
module motor_mount() {
    difference() {
        union() {
            translate([0, 0, 0]) cube([44, 44, 8], center=true);
            translate([0, 0, 0]) cylinder(d = 54, h = 8, center=true, $fn=40);
        }
        for (p = [[-12.5,-12.5],[12.5,-12.5],[-12.5,12.5],[12.5,12.5]])
            translate([p[0], p[1], 0]) m3_hole(16);
        cylinder(d = 14, h = 16, center=true, $fn=28);
        for (x = [-15, 15]) translate([x, 0, 0]) cylinder(d = 6, h = 16, center=true, $fn=20);
    }
}

// ================= SERVOHOLDER =================
module servo_mount() {
    difference() {
        union() {
            cube([62, 26, 4], center=true);
            for (sx = [-1, 1]) translate([sx * 26, 0, 18]) cube([6, 26, 36], center=true);
        }
        translate([0, 0, 4]) cube([42, 22, 42], center=true);   // servo
        for (sx = [-1, 1]) translate([sx * 18, 0, 20]) m3_hole(30);
        for (sx = [-1, 1]) translate([sx * 26, 0, 8]) m3_hole(10);
    }
}

// ================= GIMBAL =================
module gimbal() {
    // mast
    difference() {
        cylinder(d = 14, h = 70, center=true, $fn=28);
        cylinder(d = 6, h = 72, center=true, $fn=20);
    }
    // pan-servo brakett
    translate([0, 0, 40]) difference() {
        cube([46, 22, 4], center=true);
        for (sx = [-1, 1]) translate([sx * 16, 0, 0]) m3_hole(8);
    }
    // tilt-brakett
    translate([0, 0, 55]) difference() {
        cube([8, 44, 36], center=true);
        translate([0, 0, 0]) rotate([90, 0, 0]) cylinder(d = 5.5, h = 46, center=true, $fn=20);
        for (sy = [-1, 1]) translate([0, sy * 14, 0]) rotate([90,0,0]) m3_hole(20);
    }
}

// ================= HJUL (print) =================
module wheel_nav() {
    rotate([90, 0, 0]) {
        difference() {
            cylinder(d = 44, h = wheel_W + 6, center=true, $fn=40);
            cylinder(d = 14, h = wheel_W + 8, center=true, $fn=28);
            for (p = [[-12.5,-12.5],[12.5,-12.5],[-12.5,12.5],[12.5,12.5]])
                translate([p[0], p[1], 0]) m3_hole(wheel_W + 10);
        }
    }
}

module tire() {
    rotate([90, 0, 0]) difference() {
        cylinder(d = wheel_D, h = wheel_W, center=true, $fn=64);
        cylinder(d = wheel_D - 2 * tire_t, h = wheel_W + 2, center=true, $fn=64);
    }
}

module wheel() {
    tire();
    wheel_nav();
}

// ================= SKRUER (visning) =================
module bolt(p, d=4, h=12) {
    if (show_bolts) translate(p) cylinder(d=d, h=h, center=true, $fn=16);
}

module suspension_corner(sx, sy) {
    x = sx * wheelbase / 2;
    y = sy * track / 2;
    t = min(susp_travel, bump_stop);
    piv_z = plate_t / 2 + 1;
    dz0 = wheel_D / 2 - piv_z;
    dz = dz0 + t;
    dx = sqrt(max(0.01, arm_len*arm_len - dz*dz));
    hub_x = x - sx * (arm_len - dx);
    hub_z = wheel_D / 2 + t;

    // arm (rotert 90 grader om X for aa ligge i kjoreretningen)
    translate([x - sx * arm_len, y, piv_z])
        rotate([0, 0, sx > 0 ? 0 : 180])
        suspension_arm();

    // spindel + nav
    translate([hub_x, y, hub_z]) {
        knuckle();
        wheel();
    }

    // demper (enkel sylinder som visning; kjop fjaer/demper)
    translate([x - sx * 20, y, plate_t + 10])
        rotate([0, 90, 0]) cylinder(d = 8, h = 60, center=true, $fn=20);
}

// ================= VISNINGER =================
module assembly() {
    chassis();
    translate([0, 0, plate_t + 2]) battery_tray();
    translate([60, 0, plate_t + 20]) servo_mount();
    translate([-40, 0, plate_t + 8]) rotate([0, 0, 0]) gimbal();

    for (sx = [-1, 1]) for (sy = [-1, 1]) suspension_corner(sx, sy);

    // motorer (visning som sylindre)
    for (sx = [-1, 1]) for (sy = [-1, 1])
        translate([sx * wheelbase/2, sy * (track/2 - 26), plate_t + 20])
            cylinder(d = 44, h = 16, center=true, $fn=40);

    // bolter (eksempler)
    if (show_bolts)
        for (sx = [-1, 1]) for (sy = [-1, 1]) {
            translate([sx * wheelbase/2, sy * (track/2 - 26), plate_t])
                bolt([0, 0, 0]);
        }
}

module layout() {
    // Printplate: 256 x 256 (Bambu A1)
    translate([-100, -100, 0]) chassis_flat();
    translate([110, -110, 0]) rotate([0, 0, 0]) flat(battery_tray(), 170, 120);
    translate([110, 0, 0]) flat(servo_mount(), 62, 40);
    translate([110, 60, 0]) flat(gimbal(), 50, 50);
    for (i = [0:3]) translate([-100 + i * 60, 90, 0]) flat(arm_flat(), 70, 20);
    for (i = [0:1]) translate([-100 + i * 60, 130, 0]) flat(knuckle_flat(), 40, 40);
    for (i = [0:3]) translate([110 + (i % 2) * 60, 130 + (i / 2) * 60, 0]) flat(motor_mount(), 56, 56);
}

module chassis_flat() { rotate([0, 0, 0]) chassis(); }
module flat(m, L, Wd) { m(); }
module arm_flat() { rotate([90, 0, 0]) suspension_arm(); }
module knuckle_flat() { knuckle(); }

if (view == "assembly") assembly();
if (view == "layout") layout();
if (view == "parts") {
    translate([0, 0, 0]) chassis();
    translate([0, 260, 0]) battery_tray();
    translate([250, 0, 0]) suspension_arm();
    translate([250, 100, 0]) knuckle();
    translate([250, 200, 0]) motor_mount();
}

// Enkeltdeler (for STL-eksport og printestimater)
if (view == "chassis")  chassis();
if (view == "tray")     battery_tray();
if (view == "arm")      rotate([90, 0, 0]) suspension_arm();
if (view == "knuckle")  knuckle();
if (view == "mount")    motor_mount();
if (view == "servo")    servo_mount();
if (view == "gimbal")   gimbal();
if (view == "hub")      wheel_nav();
if (view == "tire")     tire();
if (view == "bump")     cylinder(d = 14, h = bump_stop, center = false);

$fn = 48;
