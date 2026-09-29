// X-Finger CAD Prototype v0.4
// Normalized by master adjustment pitch P.
// Absolute millimetre scale is intentionally unresolved.

P = 5.0; // display scale only; NOT identified manufacturing pitch
bar_w = 1.30*P;
plate_t = 0.24*P;
hole_d = 0.32*P; // display-only seed
n_holes = 6;
row_sep = 2.15*P; // frame-derived apparent value; perspective-sensitive

module indexed_bar(n=n_holes, pitch=P, width=bar_w, thickness=plate_t) {
    difference() {
        hull() {
            translate([0,0,0]) cylinder(h=thickness, d=width, $fn=48);
            translate([(n-1)*pitch,0,0]) cylinder(h=thickness, d=width, $fn=48);
        }
        for (i=[0:n-1])
            translate([i*pitch,0,-0.1]) cylinder(h=thickness+0.2, d=hole_d, $fn=36);
    }
}

translate([0, row_sep/2,  plate_t]) indexed_bar();
translate([0,-row_sep/2, -plate_t]) indexed_bar();

// This file models the identified indexing relationship only.
// Do not use P=5.0 as a recovered X-Finger dimension.
