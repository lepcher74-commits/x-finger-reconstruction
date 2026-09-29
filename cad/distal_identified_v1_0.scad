// X-Finger distal identified geometry v1.0
// IDENTIFIED_GEOMETRY from two mirrored CAD views.
// Absolute scale is intentionally parameterized.

datum = 20.0; // mm placeholder for |P0P1|; ESTIMATED until calibration

r01 = 1.0000;
r12 = 0.3668;
r23 = 0.4290;
r34 = 0.6728;

// Reference turning geometry reconstructed from normalized upper-view landmarks.
// This file is a kinematic skeleton, not a manufacturing part.

P0 = [0,0];
P1 = [datum,0];

// approximate signed turn angles derived from the identified view
a12 = -28.0;
a23 = -10.0;
a34 =  6.0;

function v2(L,a) = [L*cos(a), L*sin(a)];

P2 = P1 + v2(datum*r12,a12);
P3 = P2 + v2(datum*r23,a12+a23);
P4 = P3 + v2(datum*r34,a12+a23+a34);

module joint(p,d=2.0,h=1.2) {
    translate([p[0],p[1],0]) cylinder(d=d,h=h,$fn=40);
}

module link(a,b,w=4,h=1.2) {
    hull() {
        translate([a[0],a[1],0]) cylinder(d=w,h=h,$fn=40);
        translate([b[0],b[1],0]) cylinder(d=w,h=h,$fn=40);
    }
}

link(P0,P1);
link(P1,P2);
link(P2,P3);
link(P3,P4);

joint(P0); joint(P1); joint(P2); joint(P3); joint(P4);
