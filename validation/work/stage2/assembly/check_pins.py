from pathlib import Path
import cadquery as cq,json,numpy as np,math
D=Path(__file__).resolve().parent;motion=json.loads((D/'motion.json').read_text());models=json.loads((D/'viewer_data.json').read_text())['models'];shapes={p.name[:3]:cq.importers.importStep(str(p)).val() for p in (D/'parts').glob('*.step')}
# Cylindrical shanks are reconstructed from the exact displayed/exported mesh bounds.
pins={};parent={}
for m in models:
 if m['id'][0]!='J':continue
 v=np.array(m['v']);lo=v.min(0);hi=v.max(0);c=(lo+hi)/2;z0,z1=(-29.4,29.4) if m['id']=='J3' else (lo[2],hi[2]);pins[m['id']]=cq.Solid.makeCylinder(4.8,z1-z0,cq.Vector(c[0],c[1],z0));parent[m['id']]=m['parent']
def move(s,id,f):
 t=f['transforms'][id];return s.rotate((0,0,0),(0,0,1),math.degrees(t['angle'])).translate((*t['translation'],0))
errors=[]
for i in range(len(motion)):
 f=motion[i];bodies={id:move(s,id,f) for id,s in shapes.items()};boxes={id:s.BoundingBox() for id,s in bodies.items()}
 for jid,pin in pins.items():
  pin=move(pin,parent[jid],f);a=pin.BoundingBox()
  for id,s in bodies.items():
   b=boxes[id]
   if any(getattr(a,k+'max')<getattr(b,k+'min') or getattr(b,k+'max')<getattr(a,k+'min') for k in 'xyz'):continue
   common=pin.intersect(s);vol=common.Volume() if common.Solids() else 0
   if vol>.01:errors.append({'frame':i,'pair':[jid,id],'volume':vol})
 if i%15==0:print('pins',i,'errors',len(errors),flush=True)
(D/'pin_checks.json').write_text(json.dumps({'frames':len(motion),'collisions':errors},indent=2));print('pins done',len(errors),flush=True)
