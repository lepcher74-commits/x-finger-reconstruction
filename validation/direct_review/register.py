import struct,json
import numpy as np
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import binary_erosion
from scipy.spatial import cKDTree
from scipy.optimize import differential_evolution
root=Path('/workspace/scratch/e079da7851b6'); out=root/'repo/validation/direct_review'
b=(root/'latest_review/work/reproduction/parts/P04_green.stl').read_bytes();n=struct.unpack_from('<I',b,80)[0]
tri=np.array([struct.unpack_from('<12f',b,84+50*i)[3:] for i in range(n)]).reshape(-1,3,3)[:,:,:2];tri[:,:,1]*=-1
origin=tri.reshape(-1,2).min(0);tri-=origin
canvas=Image.new('1',(300,260));dr=ImageDraw.Draw(canvas)
for t in tri:dr.polygon([tuple(p*1.8+5) for p in t],fill=1)
m=np.array(canvas);yy,xx=np.where(m&~binary_erosion(m));src=(np.column_stack([xx,yy])-5)/1.8;src=src[::2];center=src.mean(0);src-=center
im=Image.open(root/'upload/image(20261013-085334).png').convert('RGB');a=np.array(im).astype(float);mask=(a[:,:,1]>100)&(a[:,:,1]>a[:,:,0]*1.5)&(a[:,:,1]>a[:,:,2]*1.5);y,x=np.where(mask&~binary_erosion(mask));dst=np.column_stack([x,y]);tree=cKDTree(dst)
def transform(p,pars):
 s,ang,tx,ty=pars;c=np.cos(ang);v=np.sin(ang);return s*p@np.array([[c,v],[-v,c]])+np.array([tx,ty])
def fun(pars):
 q=transform(src,pars);e=tree.query(q)[0];f=cKDTree(q).query(dst)[0];return np.mean(np.minimum(e,15)**2)+np.mean(np.minimum(f,15)**2)
r=differential_evolution(fun,[(.3,.8),(-.6,.6),(55,100),(125,155)],seed=42,popsize=12,maxiter=90,tol=1e-6)
q=transform(src,r.x);errs=tree.query(q)[0];report={'method':'Robust symmetric silhouette fit, uniform scale + rotation + translation. Green drawing may be occluded; NOT engineering acceptance.','scale_pixels_per_model_unit':float(r.x[0]),'rotation_degrees':float(np.degrees(r.x[1])),'translation':r.x[2:].tolist(),'model_center_before_transform':(origin+center).tolist(),'mean_outline_error_px':float(errs.mean()),'p95_outline_error_px':float(np.percentile(errs,95)),'physical_scale_confirmed':False}
(out/'registration.json').write_text(json.dumps(report,indent=2))
base=im.resize((im.width*4,im.height*4));d=ImageDraw.Draw(base)
for p in q:d.ellipse((p[0]*4-2,p[1]*4-2,p[0]*4+2,p[1]*4+2),fill=(220,20,70))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23)
page=Image.new('RGB',(1596,840),'white');page.paste(base,(0,60));d=ImageDraw.Draw(page);d.text((25,15),'Красный контур — существующая P04; цветная заливка — ваш новый разрез',font=font,fill='black');d.text((25,805),'Совмещение предварительное. Форма P04 не изменялась. Это не готовая 3D-сборка.',font=font,fill='black');page.save(out/'section_overlay.png');print(json.dumps(report))
