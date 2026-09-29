// X-Finger CAD Prototype v0.3
// Parametric research reconstruction.
// CONFIRMED hardware values are separated from ESTIMATED geometry.

// ---------- confidence classes ----------
// CONFIRMED: M1.4 fastener family; proximal 5L (small 4L), distal 2L.
// ESTIMATED: all plate geometry below until KIN-ID metric calibration.

$fn = 48;

// ----- estimated prototype seed -----
hole_pitch = 5.0;       // mm, ESTIMATED
hole_d     = 1.6;       // mm, ESTIMATED clearance seed for M1.4
bar_w      = 6.5;       // mm, ESTIMATED
plate_t    = 1.2;       // mm, ESTIMATED
ab         = 10.0;      // mm, ESTIMATED
branch_l   = 35.0;      // mm, ESTIMATED
phalanx_l  = 34.0;      // mm, ESTIMATED
distal_l   = 18.0;      // mm, ESTIMATED
z_gap      = 6.0;       // mm, ESTIMATED layer separation
input_deg  = -18;
distal_deg = -28;

// ----- helpers -----
module capsule2d(len, w) {
    hull() {
        translate([0,0]) circle(d=w);
        translate([len,0]) circle(d=w);
    }
}

module indexed_bar(len, w, pitch, n_holes, d) {
    linear_extrude(height=plate_t)
    difference() {
        capsule2d(len,w);
        for(i=[1:n_holes])
            translate([i*pitch,0]) circle(d=d);
    }
}

module plain_bar(len,w) {
    linear_extrude(height=plate_t) capsule2d(len,w);
}

module pivot_pin(h=8,d=1.4) {
    cylinder(h=h,d=d,center=true);
}

// ----- assembly -----
module xfinger_seed() {
    // rotating input bracket represented as a transverse bar
    rotate([0,0,input_deg])
    translate([0,-ab/2,0])
        rotate([0,0,90]) plain_bar(ab,bar_w);

    // upper branch
    rotate([0,0,input_deg])
    translate([0,ab/2,z_gap/2])
        indexed_bar(branch_l,bar_w,hole_pitch,5,hole_d);

    // lower branch
    rotate([0,0,input_deg])
    translate([0,-ab/2,-z_gap/2])
        indexed_bar(branch_l,bar_w,hole_pitch,5,hole_d);

    // primary phalanx seed
    rotate([0,0,input_deg])
    translate([branch_l,0,0])
        plain_bar(phalanx_l,bar_w+2);

    // distal seed
    rotate([0,0,input_deg])
    translate([branch_l+phalanx_l,0,0])
    rotate([0,0,distal_deg])
        plain_bar(distal_l,bar_w+1);
}

xfinger_seed();
