from pathlib import Path
import numpy as np,json,math,cadquery as cq
from PIL import Image
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from shapely.geometry import Polygon
from shapely.ops import unary_union
D=Path(__file__).resolve().parent
im=np.array(Image.open(D/'contour_reference.png').convert('RGB'))
pink=(im[:,:,0]>120)&(im[:,:,0]<210)&(im[:,:,1]<120)&(im[:,:,2]>90)
border=pink&~ndi.binary_erosion(pink);yy,xx=np.where(border);tree=cKDTree(np.c_[xx,yy])
shape=cq.importers.importStep(str(D/'parts/P06_pink.step')).val();vv,ff=shape.tessellate(.2);v=np.array([[p.x,p.y] for p in vv]);pol=unary_union([Polygon(v[list(t)]) for t in ff if Polygon(v[list(t)]).area>1e-7]);out=np.array(pol.exterior.coords)
# Pink through-hole is the registration datum; target is a perspective screenshot.
center=np.array([1103.,-453.]);target=np.array([143.,221.]);
def R(a):return np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
def objective(z):
 s,a=z;p=(out-center)@R(a).T*s+target;select=(p[:,0]>118)&(p[:,0]<945)&(p[:,1]>160)&(p[:,1]<285);dist=tree.query(p[select])[0];return np.mean(np.minimum(dist,35)**2) if len(dist)>10 else 1e4
fit=minimize(objective,[1.95,3.16],method='Nelder-Mead');scale,angle=fit.x
print('registration',scale,angle,'rms',np.sqrt(fit.fun),flush=True)
# Digitize the upper/lower red lines and close at the green attachment.
red=(im[:,:,0]>200)&(im[:,:,1]<105)&(im[:,:,2]<70)
upper=[];lower=[]
for x in range(168,798,5):
 ys=np.where(red[:,x])[0];ys=ys[ys>240]
 if len(ys):upper.append([x,float(ys.min()+1)]);lower.append([x,float(ys.max()-1)])
# End points are the explicitly marked contour corners.
points=np.array([[166,266]]+upper+[[807,263],[800,314]]+lower[::-1]+[[114,303]],float)
def inv(p):return (np.array(p)-target)@R(angle)/scale+center
xy=inv(points);outline=Polygon(xy).buffer(0)
def prism(p,z0,z1):return cq.Workplane('XY').polyline(list(p.exterior.coords)[:-1]).close().extrude(z1-z0).translate((0,0,z0)).val()
old=cq.importers.importStep(str(D/'parts/P07_dark_blue.step')).val()
# Preserve the entire two-hole curved end beyond the marked span. Overlap joins the patch.
keep=Polygon(inv([[-2000,-1000],[170,-1000],[170,2000],[-2000,2000]]))
kept=old.intersect(prism(keep,-200,200))
w=13.366908204933452
body=prism(outline,-68-w/2,-68+w/2)
# Thin transverse end continues into the green seat in the same direction.
tabpoly=outline.intersection(Polygon(inv([[792,-1000],[820,-1000],[820,2000],[792,2000]])))
tab=prism(tabpoly,-68-w/2,27.0)
new=kept.fuse(body).fuse(tab).clean()
print('new',new.isValid(),len(new.Solids()),flush=True)
assert new.isValid() and len(new.Solids())==1
cq.exporters.export(new,str(D/'parts/P07_dark_blue.step'));cq.exporters.export(new,str(D/'parts/P07_dark_blue.stl'),tolerance=.15,angularTolerance=.12)
# Accommodate the marked tongue in the keyed green seat, maintaining the rigid connection.
green=cq.importers.importStep(str(D/'parts/P04_green.step')).val();green=green.cut(new).clean();assert green.isValid() and len(green.Solids())==1
cq.exporters.export(green,str(D/'parts/P04_green.step'));cq.exporters.export(green,str(D/'parts/P04_green.stl'),tolerance=.15,angularTolerance=.12)
(D/'contour_change.json').write_text(json.dumps({'image_scale':scale,'angle':angle,'fit_rms_pixels':float(np.sqrt(fit.fun)),'red_contour_xy':xy.tolist(),'method':'approximate planar registration of perspective reference to pink rod; red contour digitized; two-hole end preserved'},indent=2))
