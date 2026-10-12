from pathlib import Path
import cadquery as cq,json,numpy as np,math
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parent
motion=json.loads((D/'motion.json').read_text());params=json.loads((D/'assembly_parameters.json').read_text());files=sorted((D/'parts').glob('*.step'));shapes={f.name[:3]:cq.importers.importStep(str(f)).val() for f in files}
colors=['#34383d','#4775bd','#ee961e','#73b820','#8737aa','#b94f96','#27109b','#a4a7ac','#efca14'];names=['Чёрная','Синяя','Оранжевая','Зелёная','Фиолетовая','Розовая','Тёмно-синяя','Серая','Жёлтая']
# Canonical initial hole centers, shared with the kinematic solver.
data=json.loads((D.parent/'parts_2d_v1/geometry.json').read_text());holes={p['id']:np.array([h['center'] for h in p['holes']])@np.array(p['R'])+p['t'] for p in data['parts']}
pairs=[('P01',0,'P02',0),('P02',1,'P03',0),('P03',1,'P05',0),('P05',1,'P01',2),('P01',1,'P04',0),('P06',0,'P09',0),('P07',0,'P08',0),('P07',1,'P08',1)]
for a,i,b,j in pairs:holes[a][i]=holes[b][j]=(holes[a][i]+holes[b][j])/2
pins={};pinparent={}
for k,(a,i,b,j) in enumerate(pairs):
 x,y=holes[a][i]*[1,-1];z0,z1=(-47,47) if k<5 else ((-77,-34) if k==5 else (-77,-41));z0,z1=(-29.4,29.4) if k==2 else (z0,z1);pin=cq.Solid.makeCylinder(4.8,z1-z0,cq.Vector(x,y,z0));pins['J'+str(k+1)]=pin;pinparent['J'+str(k+1)]=a
models=[]
def mesh(s):
 v,f=s.tessellate(.25,.15);return {'v':np.round([[p.x,p.y,p.z] for p in v],4).tolist(),'f':[list(t) for t in f]}
for i,(id,s) in enumerate(shapes.items()):
 m=dict(id=id,parent=id,name=names[i],color=colors[i],**mesh(s))
 if id in ['P01','P09']:
  limit=0 if id=='P01' else -49.541314704899094
  box=cq.Workplane('XY').box(2000,2000,500,centered=(False,False,False)).translate((0,-1500,limit)).val();cut=s.cut(box)
  m['section']=mesh(cut)
 models.append(m)
for id,s in pins.items():models.append(dict(id=id,parent=pinparent[id],name='Ось '+id,color='#cbd0d5',**mesh(s)))
# Export colored assembled STEP with individual objects and eight axes.
for index,label in [(0,'open'),(len(motion)-1,'folded')]:
 ass=cq.Assembly(name='finger_'+label)
 for m in models:
  s=shapes.get(m['id'],pins.get(m['id']));t=motion[index]['transforms'][m['parent']];s=s.rotate((0,0,0),(0,0,1),math.degrees(t['angle'])).translate((*t['translation'],0));rgb=tuple(int(m['color'][j:j+2],16)/255 for j in (1,3,5));ass.add(s,name=m['id']+'_'+params.get(m['id'],{}).get('name','pin'),color=cq.Color(*rgb))
 ass.save(str(D/('assembly_'+label+'.step')))
(D/'viewer_data.json').write_text(json.dumps({'models':models,'motion':motion},separators=(',',':')))
# Verify coaxial constraints and rigid two-pin gray/dark-blue attachment for every pose.
maxerr=0
for f in motion:
 for a,i,b,j in pairs:
  def pos(id,k):
   t=f['transforms'][id];q=t['angle'];R=np.array([[math.cos(q),-math.sin(q)],[math.sin(q),math.cos(q)]]);return (holes[id][k]*[1,-1])@R.T+t['translation']
  maxerr=max(maxerr,float(np.linalg.norm(pos(a,i)-pos(b,j))))
(D/'joint_checks.json').write_text(json.dumps({'max_coaxial_error':maxerr,'frames':len(motion),'pairs':pairs,'pin_radius':4.8,'hole_radius':5.3,'gray_darkblue':'two shared axes and identical rigid motion'},indent=2))
# Raster preview and GIF: true triangulated CAD geometry, cutaway solely for visibility.
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';font=ImageFont.truetype(fontpath,22);small=ImageFont.truetype(fontpath,16)
prepared=[]
for m in models:
 mm=m if m['id']=='P01' else m.get('section',m);prepared.append((m,np.array(mm['v']),np.array(mm['f'])))
yaw=-.3;pitch=.48
Ry=np.array([[np.cos(yaw),0,np.sin(yaw)],[0,1,0],[-np.sin(yaw),0,np.cos(yaw)]]);Rx=np.array([[1,0,0],[0,np.cos(pitch),-np.sin(pitch)],[0,np.sin(pitch),np.cos(pitch)]]);R=Rx@Ry
center=np.array([805,-600,15]);scale=.98
frames=[]
for idx in np.linspace(0,len(motion)-1,38).astype(int):
 f=motion[idx];triangles=[]
 for m,v,faces in prepared:
  t=f['transforms'][m['parent']];a=t['angle'];r=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]]);v=v.copy();v[:,:2]=v[:,:2]@r.T+t['translation'];v=(v-center)@R.T;tri=v[faces];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-12);shade=.6+.4*np.abs(norm@np.array([.2,.4,.89]));rgb=np.array([int(m['color'][i:i+2],16) for i in [1,3,5]])
  for j,tt in enumerate(tri):triangles.append((tt[:,2].mean(),tt[:,:2],tuple((rgb*shade[j]).astype(int))))
 im=Image.new('RGB',(1200,730),'#f6f8fc');draw=ImageDraw.Draw(im)
 for depth,pts,col in sorted(triangles,key=lambda t:t[0]):draw.polygon([(600+x*scale,365-y*scale) for x,y in pts],fill=col)
 draw.text((25,18),'3D-сборка • чёрный корпус показан полностью',font=font,fill='#202a36')
 draw.text((25,53),f"Основная фаланга: {abs(f['body_deg']):.1f}°   Концевая: {abs(f['tip_deg']):.1f}°",font=small,fill='#39475c')
 draw.text((25,665),'Жёлтый корпус показан в разрезе; чёрный корпус — с обеими стенками.',font=small,fill='#39475c')
 draw.text((25,692),'Условный масштаб. Показан расчётный ход до прежнего 2D-упора.',font=small,fill='#39475c')
 frames.append(im)
 if idx==0:im.save(D/'assembly_preview.png')
 if idx%10==0:print('render',idx,flush=True)
frames=frames+[frames[-1]]*8+frames[-2:0:-1]+[frames[0]]*5
frames[0].save(D/'assembly_motion_3d.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False)
print('render done; joint error',maxerr,flush=True)
