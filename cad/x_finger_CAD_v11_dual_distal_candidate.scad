$fn=40;
// X-Finger Reconstruction — CAD v1.1 dual distal topology candidate
// Research reverse-engineering model. NOT clinically validated.
// H1 and H3 are both retained until video-based distal motion selects one.

hole_d=1.8;
shaft_d=1.4;
head_d=3.0;
head_h=1.2;
washer_d=3.2;
washer_t=0.3;

A=[0.0000,2.5000]; B=[0.0000,-2.5000]; C=[48.1100,2.5000]; D=[51.9951,-7.4483]; M=[50.0525,-2.4741]; E=[80.9882,-4.4701];
Q0=[80.9882,-4.4701]; Q1=[107.8524,-6.2034]; Q2=[115.9871,-12.1804]; Q3=[126.9630,-17.1863]; Q4=[144.3114,-21.1565];

module capsule2d(a,b,w) {
  hull() { translate(a) circle(d=w); translate(b) circle(d=w); }
}
module link(a,b,w,t,holes=[]) {
  linear_extrude(height=t,center=true)
  difference() {
    capsule2d(a,b,w);
    for(h=holes) translate(h) circle(d=hole_d);
  }
}
module screw_envelope(p,z0,z1) {
  translate([p[0],p[1],(z0+z1)/2]) cylinder(d=shaft_d,h=abs(z1-z0),center=true);
  translate([p[0],p[1],max(z0,z1)+head_h/2]) cylinder(d=head_d,h=head_h,center=true);
}
module washer(p,z) {
  translate([p[0],p[1],z]) linear_extrude(height=washer_t,center=true)
  difference() { circle(d=washer_d); circle(d=hole_d); }
}

module primary() {
  translate([0,0,0]) link(A,B,7,1.4,[A,B]);
  translate([0,0,1.9]) link(A,C,4,1,[A,C]);
  translate([0,0,-1.9]) link(B,D,4,1,[B,D]);
  translate([0,0,0]) link(C,D,8,1.6,[C,D]);
  translate([0,0,3.5]) link(M,E,5,1,[]);
  translate([0,0,-3.5]) link(M,E,5,1,[]);
}

module distal_H1() {
  translate([0,0,3.5]) link(Q0,Q1,5,1,[Q0,Q1]);
  translate([0,0,1.9]) link(Q0,Q2,4,1,[Q0,Q2]);
  translate([0,0,0]) link(Q2,Q3,4,1,[Q2,Q3]);
  translate([0,0,-1.9]) link(Q1,Q3,4,1,[Q1,Q3]);
  translate([0,0,-3.5]) link(Q3,Q4,5,1.4,[Q3]);
}

module distal_H3() {
  translate([0,0,3.5]) link(Q0,Q2,5,1,[Q0,Q2]);
  translate([0,0,1.9]) link(Q0,Q1,4,1,[Q0,Q1]);
  translate([0,0,0]) link(Q1,Q3,4,1,[Q1,Q3]);
  translate([0,0,-1.9]) link(Q2,Q3,4,1,[Q2,Q3]);
  translate([0,0,-3.5]) link(Q3,Q4,5,1.4,[Q3]);
}

module fasteners() {
  for(p=[A,B,C,D,Q0,Q1,Q2,Q3])
    screw_envelope(p,-4.2,4.2);
  for(p=[C,D,Q2,Q3]) {
    washer(p,1.15);
    washer(p,-1.15);
  }
}

part="assembly_H1";
if(part=="primary") primary();
if(part=="distal_H1") distal_H1();
if(part=="distal_H3") distal_H3();
if(part=="fasteners") fasteners();
if(part=="assembly_H1") { primary(); distal_H1(); fasteners(); }
if(part=="assembly_H3") { primary(); distal_H3(); fasteners(); }
