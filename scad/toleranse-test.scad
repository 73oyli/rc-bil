// TOLERANSE-TESTPLATE (print forst, mål med skyvelaere, juster i bil-print.scad)
// 90 x 70 x 8 mm. Alle hull er gjennomgaaende der ikke annet er sagt.
// Bruk: print flat, mål hullene, oppdater fit_clear / insert_clear / pivot_clear.

plate_L = 96;
plate_W = 76;
plate_t = 8;

difference() {
    cube([plate_L, plate_W, plate_t]);

    // --- M3 klaringshull (3,2 / 3,4 / 3,6) ---
    for (i = [0:2]) {
        d = 3.2 + i * 0.2;
        translate([14 + i * 18, 14, 0]) cylinder(d = d, h = plate_t + 2, $fn = 24);
    }

    // --- M3 varmepress-insert (4,0 / 4,2 / 4,4), 6 mm dyp blindhull ---
    for (i = [0:2]) {
        d = 4.0 + i * 0.2;
        translate([68 + i * 0, 14 + i * 16, 0])
            cylinder(d = d, h = 6, $fn = 28);
    }

    // --- M4 pivot (4,2 / 4,4) ---
    for (i = [0:1]) {
        d = 4.2 + i * 0.2;
        translate([14 + i * 18, 44, 0]) cylinder(d = d, h = plate_t + 2, $fn = 24);
    }

    // --- M6 kingpin (6,0 / 6,2) ---
    for (i = [0:1]) {
        d = 6.0 + i * 0.2;
        translate([52 + i * 18, 44, 0]) cylinder(d = d, h = plate_t + 2, $fn = 28);
    }

    // --- 608-lager (22,0 / 22,1 / 22,2) ---
    for (i = [0:2]) {
        d = 22.0 + i * 0.1;
        translate([14 + i * 26, 62, 0]) cylinder(d = d, h = plate_t + 2, $fn = 40);
    }
}

// etiketter (heves 0,4 mm)
module label(txt, x, y) {
    translate([x, y, plate_t])
        linear_extrude(0.4) text(txt, size = 5, font = "Liberation Sans");
}
