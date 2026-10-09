import base64
from pathlib import Path
import cv2


def create_editor(source, output):
    target = Path(output)
    if target.exists():
        raise ValueError("El editor ya existe; elige otro --output")
    cap = cv2.VideoCapture(source)
    try:
        ok, frame = cap.read()
    finally:
        cap.release()
    if not ok:
        raise ValueError("No se pudo leer el primer fotograma")
    height = round(frame.shape[0] * 960 / frame.shape[1])
    frame = cv2.resize(frame, (960, height))
    ok, jpeg = cv2.imencode(".jpg", frame)
    if not ok:
        raise ValueError("No se pudo generar la imagen del editor")
    encoded = base64.b64encode(jpeg).decode("ascii")
    document = r'''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Configurar zonas · Café Analytics</title>
<style>body{font:16px system-ui;background:#101a20;color:#e9efef;max-width:1100px;margin:30px auto;padding:20px}canvas{width:100%;height:auto;cursor:crosshair;border-radius:12px}button,input,select{font:inherit;padding:10px;border:1px solid #546772;border-radius:6px;margin:6px;background:#20333d;color:white}button{cursor:pointer}#status{color:#a8f0ca}pre{white-space:pre-wrap}p{line-height:1.5}</style>
<h1>Dibuja dónde quieres medir.</h1><p>Haz clic en los vértices de una zona convexa, en orden. Pulsa “Guardar zona”. Para el acceso, cambia a línea y marca dos extremos. La flecha indica entrada. Usa una cámara fija.</p>
<label>Modo <select id="mode"><option value="zone">Zona</option><option value="gate">Línea de acceso</option></select></label>
<label>Nombre <input id="name" value="barra" maxlength="50"></label>
<button id="undo">Deshacer punto</button><button id="save">Guardar zona / línea</button><button id="reverse">Invertir entrada</button><button id="reset">Borrar todo</button>
<canvas id="canvas"></canvas><p id="status" role="status"></p>
<label>Punto de seguimiento <select id="anchor"><option value="bottom_center">Centro inferior (pies)</option><option value="center">Centro del cuerpo (vista cenital)</option></select></label>
<button id="download">Descargar zonas.json</button><pre id="list"></pre>
<p>En una línea de izquierda a derecha, entrada apunta hacia abajo inicialmente. Invierte si hace falta. Las zonas pueden superponerse: una persona aportará tiempo a cada zona que la contenga.</p>
<script>
const canvas=document.getElementById('canvas'), ctx=canvas.getContext('2d'), img=new Image();
const mode=document.getElementById('mode'), nameInput=document.getElementById('name'), status=document.getElementById('status');
let points=[], zones=[], gates=[], direction='negative_to_positive';
function draw(){ctx.drawImage(img,0,0,canvas.width,canvas.height);ctx.lineWidth=3;ctx.font='18px sans-serif';
function shape(p,closed,color,label){ctx.strokeStyle=color;ctx.fillStyle=color;ctx.beginPath();p.forEach((v,i)=>{let x=v[0]*canvas.width,y=v[1]*canvas.height;i?ctx.lineTo(x,y):ctx.moveTo(x,y)});if(closed)ctx.closePath();ctx.stroke();p.forEach(v=>{ctx.beginPath();ctx.arc(v[0]*canvas.width,v[1]*canvas.height,5,0,Math.PI*2);ctx.fill()});if(p.length&&label)ctx.fillText(label,p[0][0]*canvas.width+7,p[0][1]*canvas.height-7)}
zones.forEach(z=>shape(z.polygon,true,'#93f2c5',z.name));gates.forEach(g=>{shape(g.points,false,'#ffe085',g.name);const a=g.points[0].map((x,i)=>x*[canvas.width,canvas.height][i]),b=g.points[1].map((x,i)=>x*[canvas.width,canvas.height][i]);let dx=b[0]-a[0],dy=b[1]-a[1],norm=Math.hypot(dx,dy),sign=g.in_direction==='negative_to_positive'?1:-1;let x=(a[0]+b[0])/2,y=(a[1]+b[1])/2,ex=x-dy/norm*35*sign,ey=y+dx/norm*35*sign;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(ex,ey);ctx.stroke();ctx.fillText('IN',ex,ey)});
shape(points,false,'#fff','');document.getElementById('list').textContent=zones.map(z=>'Zona: '+z.name).concat(gates.map(g=>'Acceso: '+g.name)).join('\n');status.textContent=points.length+' puntos · '+zones.length+' zonas · '+gates.length+' accesos';}
img.onload=()=>{canvas.width=img.width;canvas.height=img.height;draw()};img.src='data:image/jpeg;base64,__IMAGE__';
canvas.onclick=e=>{if(mode.value==='gate'&&points.length>=2)return;let r=canvas.getBoundingClientRect();points.push([(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height]);draw()};
mode.onchange=()=>{points=[];draw()};document.getElementById('undo').onclick=()=>{points.pop();draw()};
function convex(p){let signs=[];for(let i=0;i<p.length;i++){let a=p[i],b=p[(i+1)%p.length],c=p[(i+2)%p.length];let v=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]);if(Math.abs(v)>1e-8)signs.push(Math.sign(v))}return signs.length>=3&&signs.every(s=>s===signs[0])}
document.getElementById('save').onclick=()=>{let name=nameInput.value.trim();let entries=mode.value==='zone'?zones:gates;if(!name||entries.some(z=>z.name===name)){status.textContent='Usa un nombre único y no vacío';return}if(mode.value==='zone'){if(points.length<3||!convex(points)){status.textContent='Se requieren 3 o más puntos de un polígono convexo, en orden';return}zones.push({name,polygon:points})}else{if(points.length!==2||Math.hypot(points[1][0]-points[0][0],points[1][1]-points[0][1])<0.01){status.textContent='Marca 2 puntos distintos y separados';return}gates.push({name,points,in_direction:direction,hysteresis:0.012})}points=[];draw()};
document.getElementById('reverse').onclick=()=>{direction=direction==='negative_to_positive'?'positive_to_negative':'negative_to_positive';if(gates.length)gates[gates.length-1].in_direction=direction;draw()};
document.getElementById('reset').onclick=()=>{points=[];zones=[];gates=[];draw()};
document.getElementById('download').onclick=()=>{if(!zones.length){status.textContent='Guarda al menos una zona';return}const config={anchor:document.getElementById('anchor').value,zones,gates};const url=URL.createObjectURL(new Blob([JSON.stringify(config,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='zonas.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
</script></html>'''
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(document.replace("__IMAGE__", encoded), encoding="utf-8")
    print(f"Abre en tu navegador: {target.resolve()}")
