$fn=36;
// X-Finger Reconstruction — CAD v0.5 / KIN-ID v1.5
// Research prototype. Not clinically validated.

hole_d=1.8;
bar_w=4.0;
drive_t=1.0;
input_t=1.4;
pivot_t=1.6;
rail_t=1.0;

A=[0.0000,2.5000];
B=[0.0000,-2.5000];
C=[48.1100,2.5000];
D=[51.9951,-7.4483];
M=[50.0525,-2.4741];
E=[81.0525,-4.4741];

module capsule2d(p0,p1,w){
    hull(){
        translate(p0) circle(d=w);
        translate(p1) circle(d=w);
    }
}
module bar(p0,p1,w,t,holes=[]){
    linear_extrude(height=t,center=true)
    difference(){
        capsule2d(p0,p1,w);
        for(h=holes) translate(h) circle(d=hole_d);
    }
}
module input_bracket(){ bar(A,B,7.0,input_t,[A,B]); }
module upper_drive(){
    hs=[for(i=[1:7]) A+(C-A)*(i/8)];
    bar(A,C,bar_w,drive_t,concat([A,C],hs));
}
module lower_drive(){
    hs=[for(i=[1:7]) B+(D-B)*(i/8)];
    bar(B,D,bar_w,drive_t,concat([B,D],hs));
}
module pivot_block(){ bar(C,D,8.0,pivot_t,[C,D]); }
module outer_rail(){ bar(M,E,4.5,rail_t,[]); }

part = "assembly"; // input_bracket | upper_drive | lower_drive | pivot_block | outer_rail | assembly

if(part=="input_bracket") input_bracket();
if(part=="upper_drive") upper_drive();
if(part=="lower_drive") lower_drive();
if(part=="pivot_block") pivot_block();
if(part=="outer_rail") outer_rail();

if(part=="assembly"){
    translate([0,0,0]) input_bracket();
    translate([0,0,1.5]) upper_drive();
    translate([0,0,-1.5]) lower_drive();
    translate([0,0,0]) pivot_block();
    translate([0,0,3.0]) outer_rail();
    translate([0,0,-3.0]) outer_rail();
}
