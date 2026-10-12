"""Integrate the v5 shells P10/P11 into the full V4 interactive viewer.

This does NOT modify the V4 viewer or geometry: it reuses
`validation/work/stage2/assembly/viewer_data.json` (V4 models + 74-frame motion)
and appends the two new shells, rigidly parented to P04.  Outputs in
validation/v5/: standalone HTML, motion GIF (both directions), full assembly
STEP (open + folded) and the extended viewer data.
"""
from pathlib import Path
import json, math
import numpy as np
import cadquery as cq
from PIL import Image, ImageDraw, ImageFont

D = Path(__file__).resolve().parent
A = D.parent / 'work' / 'stage2' / 'assembly'

GRAY = '#96989d'   # P10 upper shell  (150,152,157)
BLUE = '#3c6ebe'   # P11 lower shell  (60,110,190)

v4 = json.loads((A / 'viewer_data.json').read_text())
motion = v4['motion']


def mesh(solid):
    v, f = solid.tessellate(0.25, 0.15)
    return {'v': np.round([[p.x, p.y, p.z] for p in v], 4).tolist(),
            'f': [list(t) for t in f]}


shell_solids = {}
for tag, name, color in (('P10', 'Верхняя оболочка P10 (серая)', GRAY),
                         ('P11', 'Нижняя оболочка P11 (синяя)', BLUE)):
    solid = cq.importers.importStep(str(D / f'{tag}_'
                                        f'{"gray_upper" if tag == "P10" else "blue_lower"}.step')).val()
    shell_solids[tag] = solid
    v4['models'].append(dict(id=tag, parent='P04', name=name, color=color,
                             **mesh(solid)))

(D / 'viewer_data_v5.json').write_text(
    json.dumps(v4, separators=(',', ':')))

# ---------------------------------------------------------------------------
# Standalone HTML: same viewer as V4, with the two shells added.
# ---------------------------------------------------------------------------
template = '''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Объёмная модель пальца · V5</title><style>*{box-sizing:border-box}body{margin:0;background:#f3f6fb;color:#202d40;font:15px system-ui}header{padding:18px 24px;background:white;border-bottom:1px solid #dce2ec}h1{font-size:22px;margin:0 0 6px}p{margin:4px 0;color:#596a82}main{display:grid;grid-template-columns:1fr 235px;height:calc(100vh - 94px)}canvas{width:100%;height:100%;touch-action:none;cursor:grab}aside{padding:18px;background:white;overflow:auto}button{padding:9px 12px;border:1px solid #c4d2e7;border-radius:6px;background:#eef3fb;color:#22395c;cursor:pointer;margin:3px}input[type=range]{width:100%}label{display:block;margin:12px 0}small{display:block;line-height:1.5;color:#69768a}#value{font-variant-numeric:tabular-nums;margin:12px 0}#parts label{margin:8px 0}.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin:0 6px}@media(max-width:700px){main{grid-template-columns:1fr;height:auto}canvas{height:60vh}aside{height:auto}}</style><header><h1>Механический палец · 3D-сборка V5</h1><p>Вращайте мышью, масштабируйте колесом. Модель работает без интернета.</p></header><main><canvas id="c"></canvas><aside><button id="play">Пауза</button><button id="reset">Исходный вид</button><input id="slider" type="range" min="0" max="73" step="1" value="0"><div id="value"></div><label><input id="section" type="checkbox"> Разрез корпусов</label><label><input id="pins" type="checkbox" checked> Показать оси</label><button id="side">Сбоку</button><button id="top">Сверху</button><div id="parts"></div><small>Серая деталь движется внутри жёлтой и жёстко связана двумя осями с тёмно-синей. Разрез меняет только отображение.<br><br>Новые оболочки: верхняя серая P10 на ножке и нижняя синяя P11 со стенками, обе жёстко следуют P04 (зелёной).<br><br>Условный масштаб. Проверка пересечений — в 74 дискретных положениях. Прочность и производственные допуски не рассчитаны.</small></aside></main><script>
const data=DATA;const canvas=document.querySelector('#c'),ctx=canvas.getContext('2d'),slider=document.querySelector('#slider'),value=document.querySelector('#value');let index=0,playing=true,dir=1,yaw=-.3,pitch=.48,zoom=1,drag=null,last=0;const visible={};
for(const m of data.models){visible[m.id]=true;for(const item of [m,m.section].filter(Boolean)){item.vertices=item.v;item.faces=item.f;}if(m.id[0]=='P'){let l=document.createElement('label');l.innerHTML=`<input type="checkbox" checked><span class="dot" style="background:${m.color}"></span>${m.name}`;l.querySelector('input').onchange=e=>{visible[m.id]=e.target.checked;draw()};document.querySelector('#parts').append(l);}}
slider.max=data.motion.length-1;const play=document.querySelector('#play');play.onclick=()=>{playing=!playing;play.textContent=playing?'Пауза':'Пуск'};slider.oninput=()=>{index=+slider.value;playing=false;play.textContent='Пуск';draw()};document.querySelector('#section').onchange=draw;document.querySelector('#pins').onchange=draw;document.querySelector('#reset').onclick=()=>{yaw=-.3;pitch=.48;zoom=1;draw()};document.querySelector('#side').onclick=()=>{yaw=0;pitch=0;draw()};document.querySelector('#top').onclick=()=>{yaw=0;pitch=Math.PI/2;draw()};
canvas.onpointerdown=e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId)};canvas.onpointermove=e=>{if(drag){yaw+=(e.clientX-drag[0])*.007;pitch+=(e.clientY-drag[1])*.007;drag=[e.clientX,e.clientY];draw()}};canvas.onpointerup=()=>drag=null;canvas.onwheel=e=>{e.preventDefault();zoom=Math.max(.3,Math.min(4,zoom*Math.exp(-e.deltaY*.001)));draw()};
function draw(){let w=canvas.clientWidth,h=canvas.clientHeight;if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}ctx.fillStyle='#f3f6fb';ctx.fillRect(0,0,w,h);let f=data.motion[index],triangles=[],s=Math.min(w/1150,h/680)*zoom,cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);for(const m of data.models){if(!visible[m.id]||(m.id[0]=='J'&&!document.querySelector('#pins').checked))continue;const mesh=document.querySelector('#section').checked&&m.section?m.section:m,t=f.transforms[m.parent],ca=Math.cos(t.angle),sa=Math.sin(t.angle);let v=mesh.vertices.map(p=>{let x=p[0]*ca-p[1]*sa+t.translation[0]-805,y=p[0]*sa+p[1]*ca+t.translation[1]+600,z=p[2]-15;let X=x*cy+z*sy,Z=-x*sy+z*cy;return [X,y*cp-Z*sp,y*sp+Z*cp]});const rgb=[1,3,5].map(i=>parseInt(m.color.slice(i,i+2),16));for(const face of mesh.faces){let p=face.map(i=>v[i]),u=p[1].map((a,i)=>a-p[0][i]),b=p[2].map((a,i)=>a-p[0][i]),n=[u[1]*b[2]-u[2]*b[1],u[2]*b[0]-u[0]*b[2],u[0]*b[1]-u[1]*b[0]],len=Math.hypot(...n)||1,shade=.6+.4*Math.abs((n[0]*.2+n[1]*.4+n[2]*.89)/len);triangles.push({p,d:(p[0][2]+p[1][2]+p[2][2])/3,c:`rgb(${rgb.map(a=>Math.round(a*shade)).join(',')})`});}}triangles.sort((a,b)=>a.d-b.d);for(const t of triangles){ctx.beginPath();t.p.forEach((p,i)=>{let x=w/2+p[0]*s,y=h/2-p[1]*s;i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.closePath();ctx.fillStyle=t.c;ctx.fill();}value.innerHTML=`Основная: ${Math.abs(f.body_deg).toFixed(1)}°<br>Концевая: ${Math.abs(f.tip_deg).toFixed(1)}°`;slider.value=index;}
function tick(now){if(playing&&now-last>110){index+=dir;if(index>=data.motion.length-1){index=data.motion.length-1;dir=-1}if(index<=0){index=0;dir=1}draw();last=now;}requestAnimationFrame(tick)}window.onresize=draw;draw();requestAnimationFrame(tick);
</script></html>'''
(D / 'assembly_viewer_v5.html').write_text(
    template.replace('DATA', (D / 'viewer_data_v5.json').read_text()))


# ---------------------------------------------------------------------------
# Motion GIF with the shells, ping-pong loop (auto fold + unfold).
# ---------------------------------------------------------------------------
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
prepared = []
for m in v4['models']:
    mm = m if m['id'] == 'P01' else m.get('section', m)
    prepared.append((m, np.array(mm['v']), np.array(mm['f'])))
yaw, pitch = -.3, .48
Ry = np.array([[np.cos(yaw), 0, np.sin(yaw)], [0, 1, 0], [-np.sin(yaw), 0, np.cos(yaw)]])
Rx = np.array([[1, 0, 0], [0, np.cos(pitch), -np.sin(pitch)], [0, np.sin(pitch), np.cos(pitch)]])
R = Rx @ Ry
center = np.array([805, -600, 15]); scale = .98
frames = []
for idx in np.linspace(0, len(motion) - 1, 38).astype(int):
    f = motion[idx]; triangles = []
    for m, v, faces in prepared:
        t = f['transforms'][m['parent']]; a = t['angle']
        r = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        v = v.copy(); v[:, :2] = v[:, :2] @ r.T + t['translation']; v = (v - center) @ R.T
        tri = v[faces]
        norm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        norm /= np.maximum(np.linalg.norm(norm, axis=1)[:, None], 1e-12)
        shade = .6 + .4 * np.abs(norm @ np.array([.2, .4, .89]))
        rgb = np.array([int(m['color'][i:i + 2], 16) for i in [1, 3, 5]])
        for j, tt in enumerate(tri):
            triangles.append((tt[:, 2].mean(), tt[:, :2],
                              tuple((rgb * shade[j]).astype(int))))
    im = Image.new('RGB', (1200, 730), '#f6f8fc'); draw = ImageDraw.Draw(im)
    for depth, pts, col in sorted(triangles, key=lambda t: t[0]):
        draw.polygon([(600 + x * scale, 365 - y * scale) for x, y in pts], fill=col)
    draw.text((25, 18), '3D-сборка V5 • P10/P11 жёстко следуют P04', font=font, fill='#202a36')
    draw.text((25, 53), f"Основная фаланга: {abs(f['body_deg']):.1f}°   "
                        f"Концевая: {abs(f['tip_deg']):.1f}°", font=small, fill='#39475c')
    draw.text((25, 665), 'Верхняя серая P10 и нижняя синяя P11 — новые оболочки.',
              font=small, fill='#39475c')
    draw.text((25, 692), 'Условный масштаб. Анимация сгибание/разгибание, 74 положения.',
              font=small, fill='#39475c')
    frames.append(im)
    if idx == 0:
        im.save(D / 'assembly_v5_preview.png')
    if idx % 10 == 0:
        print('render', idx, flush=True)
frames = frames + [frames[-1]] * 8 + frames[-2:0:-1] + [frames[0]] * 5
frames[0].save(D / 'assembly_motion_v5.gif', save_all=True,
               append_images=frames[1:], duration=100, loop=0, optimize=False)
print('gif done', flush=True)


# ---------------------------------------------------------------------------
# Full assembly STEP (open + folded) = frozen V4 assembly + the two shells.
# ---------------------------------------------------------------------------
def add_shells(src, dst, index):
    v4shape = cq.importers.importStep(str(src)).val()
    ass = cq.Assembly(name='assembly_v5')
    ass.add(v4shape, name='V4_assembly', color=cq.Color(0.85, 0.85, 0.85))
    tr = motion[index]['transforms']['P04']
    a = math.degrees(tr['angle'])
    for tag, s in shell_solids.items():
        ss = s.rotate((0, 0, 0), (0, 0, 1), a).translate((tr['translation'][0],
                                                         tr['translation'][1], 0.0))
        col = cq.Color(150 / 255, 152 / 255, 157 / 255) if tag == 'P10' \
            else cq.Color(60 / 255, 110 / 255, 190 / 255)
        ass.add(ss, name=tag, color=col)
    ass.save(str(dst))


add_shells(A / 'assembly_open.step', D / 'assembly_v5_open.step', 0)
add_shells(A / 'assembly_folded.step', D / 'assembly_v5_folded.step', len(motion) - 1)
print('assembly STEP done', flush=True)
