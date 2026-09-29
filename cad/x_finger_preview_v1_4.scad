$fn=28;

// X-Finger reconstruction — KIN-ID v1.4 preview assembly
// WARNING: research reconstruction. Metric values include bounded estimates.

P = 5.0;
bar_w = 4.0;
plate_t = 1.0;
hole_d = 1.8;
z_sep = 3.0;

A=[0,  2.5];
B=[0, -2.5];
C=[48.11, 2.5];
D=[51.995,-7.448];
M=[(C[0]+D[0])/2,(C[1]+D[1])/2];
E=[M[0]+31, M[1]-2];
F=[E[0]+17, E[1]-10];
T=[F[0]+15, F[1]-7];

module capsule2d(p0,p1,w){
    hull(){
        translate(p0) circle(d=w);
        translate(p1) circle(d=w);
    }
}

module plate_bar(p0,p1,w,t,z=0, holes=[]){
    translate([0,0,z-t/2])
    linear_extrude(height=t)
    difference(){
        capsule2d(p0,p1,w);
        for (h=holes) translate(h) circle(d=hole_d);
    }
}

module pivot_disc(p,d=bar_w*1.6,t=plate_t*1.6,z=0){
    translate([p[0],p[1],z-t/2])
    linear_extrude(height=t)
    difference(){ circle(d=d); circle(d=hole_d); }
}

upper_holes=[for(i=[1:7]) A + (C-A)*(i/8)];
lower_holes=[for(i=[1:7]) B + (D-B)*(i/8)];

plate_bar(A,C,bar_w,plate_t, z_sep/2, upper_holes);
plate_bar(B,D,bar_w,plate_t,-z_sep/2, lower_holes);

plate_bar(A,B,7.0,1.4,0,[A,B]);
plate_bar(C,D,8.0,1.6,0,[C,D]);

plate_bar(M,E,7.0,1.2,0,[]);
plate_bar([M[0],M[1]-3],[E[0],E[1]-3],4.5,1.0,-1.3,[]);

plate_bar(E,F,5.0,1.0,1.2,[E,F]);
plate_bar(F,T,6.0,1.4,0,[F,T]);

for(p=[A,B,C,D,E,F,T]) pivot_disc(p, d=4.2, t=1.8, z=0);
