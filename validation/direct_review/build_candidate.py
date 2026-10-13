from pathlib import Path
import json,math
import numpy as np
import cadquery as cq
from PIL import Image
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
R=json.loads((D/'registration.json').read_text());s=R['scale_pixels_per_model_unit'];a=math.radians(R['rotation_degrees']);rot=np.array([[math.cos(a),math.sin(a)],[-math.sin(a),math.cos(a)]]);ctr=np.array(R['model_center_before_transform']);trans=np.array(R['translation'])
def point(x,y,z):
 q=(np.array([x,y])-trans)@rot.T/s+ctr
 return cq.Vector(float(q[0]),float(-q[1]),float(z/s))
t=1.5*s
# Cross-section envelopes digitized from supplied central section. Interior shape inferred from rear view.
upper_x=[49, 60,80,100,120,140,160,180,195,205,210]
upper_top=[92,91,88,84,80,75,69,63,57,52,49]
upper_edge=[93,96,100,103,106,107,106,101,91,75,53]
lower_x=[100,110,125,145,165,180,190,198,201]
lower_bottom=[165,166,165.5,165,164.5,164,163.5,163,163]
lower_edge=[122,123,125,127,131,137,144,153,162]
# Plan widths from top/bottom drawings, normalized longitudinally; green tab width sets plan scale approximately.
upper_w=[2,35,49,53,56,58,59,57,48,32,2]
lower_w=[32,47,52,55,56,53,44,27,2]
def wire(x,center,edge,w,upper):
 # y increases downward in source image. Elliptic arch, inner offset along local ellipse normal.
 pts=[];inner=[];h=abs(edge-center);sgn=-1 if upper else 1
 for theta in np.linspace(-math.pi/2,math.pi/2,25):
  z=w*math.sin(theta);y=edge+sgn*h*math.cos(theta)
  nz=math.sin(theta)/max(w,.1);ny=sgn*math.cos(theta)/max(h,.1);nn=math.hypot(nz,ny)
  pts.append(point(x,y,z));inner.append(point(x,y-t*ny/nn,z-t*nz/nn))
 return cq.Wire.makePolygon(pts+inner[::-1]+[pts[0]])
def shell(xs,cs,es,ws,upper):return cq.Solid.makeLoft([wire(*args,upper) for args in zip(xs,cs,es,ws)],ruled=True)
gray=shell(upper_x,upper_top,upper_edge,upper_w,True);blue=shell(lower_x,lower_bottom,lower_edge,lower_w,False)
def prism(poly,halfwidth):
 w=cq.Wire.makePolygon([point(x,y,-halfwidth) for x,y in poly]+[point(*poly[0],-halfwidth)])
 return cq.Solid.extrudeLinear(w,[],cq.Vector(0,0,2*halfwidth/s))
# Central stem profile from supplied longitudinal drawing; actual P04 intersection checked below.
stem=prism([(70,88),(109,80),(101,103),(100,136),(90,119),(62,124),(69,113),(72,104)],14)
gray=gray.fuse(stem).clean()
# Rear saddle follows inclined P04 area; avoid closing whole phalanx cavity.
wall=prism([(98,122),(105,124),(111,166),(104,166)],14)
blue=blue.fuse(wall).clean()
p04=cq.importers.importStep(str(ROOT/'latest_review/work/stage2/assembly/parts/P04_green.step')).val()
report={'status':'VISUAL_CANDIDATE_NOT_VALIDATED','thickness':'1.5 model units, physical mm unresolved','assumptions':['Cross-view registration approximate; cross-section interpolation inferred from rear view','Loft thickness normal within each section only; longitudinal normal thickness not verified','Stem and lower saddle preliminary; no motion validation yet'],'parts':{}}
for name,obj in [('P04_green',p04),('P10_gray_upper',gray),('P11_blue_lower',blue)]:
 cq.exporters.export(obj,str(D/(name+'.step')));cq.exporters.export(obj,str(D/(name+'.stl')),tolerance=.5,angularTolerance=.2)
 report['parts'][name]={'valid':obj.isValid(),'solids':len(obj.Solids()),'volume':obj.Volume()}
 if name!='P04_green':report['parts'][name].update(distance_to_p04=obj.distance(p04),intersection_with_p04=obj.intersect(p04).Volume())
assy=cq.Assembly();assy.add(p04,name='P04',color=cq.Color(.4,.75,.1));assy.add(gray,name='Upper',color=cq.Color(.5,.48,.46));assy.add(blue,name='Lower',color=cq.Color(0,.6,.8));assy.save(str(D/'socket_candidate.step'))
(D/'candidate_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
