from pathlib import Path
import json,cadquery as cq,numpy as np
from PIL import Image
from shapely.geometry import Polygon
from shapely.ops import unary_union
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=Path(__file__).resolve().parent;data=json.loads((D/'contour_change.json').read_text());s=cq.importers.importStep(str(D/'parts/P07_dark_blue.step')).val();v,f=s.tessellate(.2);v=np.array([[p.x,p.y] for p in v]);p=unary_union([Polygon(v[list(t)]) for t in f if Polygon(v[list(t)]).area>1e-8]);xy=np.array(p.exterior.coords);a=data['angle'];R=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]]);uv=(xy-[1103,-453])@R.T*data['image_scale']+[143,221]
fig,ax=plt.subplots(figsize=(12,6));ax.imshow(Image.open(D/'contour_reference.png'));ax.plot(uv[:,0],uv[:,1],color='#09bbc8',lw=1.5,label='Новый контур CAD');ax.set_xlim(90,900);ax.set_ylim(360,150);ax.axis('off');ax.legend(loc='lower left');ax.set_title('Новый контур тяги поверх разметки пользователя');fig.tight_layout();fig.savefig(D/'contour_comparison.png',dpi=150)
