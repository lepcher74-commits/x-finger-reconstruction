$fn=40;
// X-Finger Reconstruction — CAD v1.0 functional-candidate
// Research prototype. NOT clinically validated.
// Primary linkage geometry: IDENTIFIED ratios.
// Distal geometry: IDENTIFIED ratios scaled through common CAD render.
// Distal motion law: ESTIMATED.

hole_d=1.8;
drive_w=4.0;
drive_t=1.0;
pivot_w=8.0;
pivot_t=1.6;
rail_w=5.0;
rail_t=1.0;
distal_w=4.5;
distal_t=1.0;

A=[0.0000,2.5000];
B=[0.0000,-2.5000];
C=[48.1084,2.5000];
D=[51.9970,-7.4454];
M=[50.0527,-2.4727];
E=[80.9892,-4.4559];
P0=[80.9892,-4.4559];
P1=[107.8547,-6.1782];
P2=[117.9287,-6.8240];
P3=[129.9678,-7.5958];
P4=[147.7287,-8.7343];

module capsule2d(a,b,w){
  hull(){ translate(a) circle(d=w); translate(b) circle(d=w); }
}
module link(a,b,w,t,holes=[]){
  linear_extrude(height=t,center=true)
  difference(){
    capsule2d(a,b,w);
    for(h=holes) translate(h) circle(d=hole_d);
  }
}
module input_bracket(){ link(A,B,7,1.4,[A,B]); }
module upper_drive(){ link(A,C,drive_w,drive_t,[A,C]); }
module lower_drive(){ link(B,D,drive_w,drive_t,[B,D]); }
module pivot_block(){ link(C,D,pivot_w,pivot_t,[C,D]); }
module main_phalanx(){ link(M,E,rail_w,rail_t,[]); }
module distal01(){ link(P0,P1,distal_w,distal_t,[P0,P1]); }
module distal12(){ link(P1,P2,distal_w,distal_t,[P1,P2]); }
module distal23(){ link(P2,P3,distal_w,distal_t,[P2,P3]); }
module fingertip(){ link(P3,P4,5.2,1.4,[P3]); }

part="assembly";
if(part=="input_bracket") input_bracket();
if(part=="upper_drive") upper_drive();
if(part=="lower_drive") lower_drive();
if(part=="pivot_block") pivot_block();
if(part=="main_phalanx") main_phalanx();
if(part=="distal01") distal01();
if(part=="distal12") distal12();
if(part=="distal23") distal23();
if(part=="fingertip") fingertip();

if(part=="assembly"){
  translate([0,0,0]) input_bracket();
  translate([0,0,1.5]) upper_drive();
  translate([0,0,-1.5]) lower_drive();
  translate([0,0,0]) pivot_block();
  translate([0,0,3.0]) main_phalanx();
  translate([0,0,2.0]) distal01();
  translate([0,0,1.0]) distal12();
  translate([0,0,0.0]) distal23();
  translate([0,0,-1.0]) fingertip();
}
