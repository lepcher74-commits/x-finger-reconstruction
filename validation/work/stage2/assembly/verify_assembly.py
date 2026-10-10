from pathlib import Path
import cadquery as cq, numpy as np,json,math,itertools
D=Path(__file__).resolve().parent
frames=json.loads((D/'motion.json').read_text());parts={p.name[:3]:cq.importers.importStep(str(p)).val() for p in (D/'parts').glob('*.step')}
def move(s,id,frame):
 t=frame['transforms'][id];a=t['angle'];x,y=t['translation'];return s.rotate((0,0,0),(0,0,1),math.degrees(a)).translate((x,y,0))
checks=[];maxvol=0;worst=None
for i,f in enumerate(frames):
 posed={id:move(s,id,f) for id,s in parts.items()};boxes={id:s.BoundingBox() for id,s in posed.items()}
 for a,b in itertools.combinations(sorted(posed),2):
  aa,bb=boxes[a],boxes[b]
  if any(getattr(aa,k+'max')<getattr(bb,k+'min') or getattr(bb,k+'max')<getattr(aa,k+'min') for k in 'xyz'):continue
  common=posed[a].intersect(posed[b]);vol=common.Volume() if common.Solids() else 0.
  if vol>maxvol:maxvol=vol;worst=[i,a,b]
  if vol>.001:checks.append({'frame':i,'input_deg':f['input_deg'],'pair':[a,b],'volume':vol})
 if i%10==0:print('check',i,'collisions',len(checks),'max',maxvol,flush=True)
(D/'collision_checks.json').write_text(json.dumps(dict(frames=len(frames),pairs_per_frame=36,threshold=.001,collisions=checks,max_overlap=maxvol,worst=worst),indent=2))
print('DONE',len(checks),maxvol,worst,flush=True)
