// X-Finger reconstruction — KIN-ID v1.3 normalized primary-stage skeleton
// NOT manufacturing geometry. Units are normalized by AB.

AB = 1.0000;
AC = 9.6217;
BD = 10.4463;
CD = 2.1357;

pivot_d = 0.20;
bar_w = 0.30;
bar_t = 0.20;

// Simple review-only skeleton. Exact included angle is not frozen here.
A=[0, AB/2, 0];
B=[0,-AB/2, 0];
C=[AC, 1.4, 0.3];
D=[BD,-1.4,-0.3];

module pivot(p){
  translate(p) cylinder(h=bar_t*2,d=pivot_d,center=true,$fn=32);
}

module bar(p0,p1,w=bar_w,t=bar_t){
  hull(){
    translate(p0) cylinder(h=t,d=w,center=true,$fn=24);
    translate(p1) cylinder(h=t,d=w,center=true,$fn=24);
  }
}

bar(A,C);
bar(B,D);
bar(A,B,w=0.45);
bar(C,D,w=0.45);
pivot(A); pivot(B); pivot(C); pivot(D);
