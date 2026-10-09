"""Render business cards above the footage, optionally using tracked clips.

Requires ffmpeg with drawtext. Input sources and licenses are in SOURCES.md.
Business cards are authored examples, not model outputs. Optional ID boxes
are generated separately by render_showcase_tracking.py.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

SCENES = [
    ('CAFETERÍA', 'assets/marketing-cafe.mp4', [
        ('CLIENTE 04', '2 h sentado', 'Pedido registrado · 1 café'),
        ('BARISTA A', '12 cafés', 'Preparados en la última hora'),
        ('OCUPACIÓN', '8 de 10', 'Mesas ocupadas')]),
    ('RESTAURANTE / BAR', 'assets/business-demo.mp4', [
        ('MESA 07', '18 min', 'Desde que hizo su pedido'),
        ('BARRA', '24 bebidas', 'Preparadas en la última hora'),
        ('SERVICIO', '6 pedidos', 'Listos para entregar')]),
    ('TIENDA', 'assets/retail.mp4', [
        ('AFLUENCIA', '42 visitas', 'Durante la última hora'),
        ('CAJA', '3 min', 'Espera media del ejemplo'),
        ('VENTAS', '17 compras', 'Registradas en el ejemplo')]),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', default='/System/Library/Fonts/Supplemental/Arial.ttf')
    parser.add_argument('--bold-font', default='/System/Library/Fonts/Supplemental/Arial Bold.ttf')
    parser.add_argument('--output', default='docs/showcase')
    parser.add_argument('--tracking-dir', help='Directory from render_showcase_tracking.py')
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    for path in [args.font, args.bold_font] + [scene[1] for scene in SCENES]:
        if not Path(path).is_file():
            parser.error(f'Missing input: {path}')
    with tempfile.TemporaryDirectory(prefix='pulso-render-') as tmp:
        folder = Path(tmp)
        clips = []
        for number, (name, source, cards) in enumerate(SCENES):
            if args.tracking_dir:
                source = str(Path(args.tracking_dir) / f'{number}.mp4')
                if not Path(source).is_file():
                    parser.error(f'Missing tracked clip: {source}')
            filters = ['scale=1280:720:force_original_aspect_ratio=decrease',
                       'pad=1280:960:(ow-iw)/2:240:color=0x10291f', 'setsar=1', 'fps=30',
                       'drawbox=x=0:y=0:w=1280:h=82:color=0x10291f@0.96:t=fill']
            def text(value, x, y, size, color='white', bold=False, start=0):
                path = folder / f'text-{number}-{len(filters)}.txt'
                path.write_text(value, encoding='utf-8')
                font = args.bold_font if bold else args.font
                filters.append(f"drawtext=fontfile='{font}':textfile='{path}':x={x}:y={y}:fontsize={size}:fontcolor={color}:enable='gte(t,{start})'")
            text('PULSO / LOCAL', 28, 17, 21, '0xd3eea3', True)
            text(name, 28, 45, 20)
            text('DEMO ILUSTRATIVA · DATOS SIMULADOS', 775, 29, 20, '0xd3eea3', True)
            if args.tracking_dir:
                text('SEGUIMIENTO DE PERSONAS · IDs TEMPORALES', 28, 914, 18, '0xd3eea3', True)
            for i, (label, value, detail) in enumerate(cards):
                x = 28 + i * 415
                start = 0.35 + i * 0.45
                filters.extend([
                    f"drawbox=x={x}:y=88:w=394:h=140:color=0x10291f@0.93:t=fill:enable='gte(t,{start})'",
                    f"drawbox=x={x}:y=88:w=394:h=3:color=0xd3eea3:t=fill:enable='gte(t,{start})'",
                ])
                text(label, x+18, 104, 18, '0xd3eea3', True, start)
                text(value, x+18, 132, 40, 'white', True, start)
                text(detail, x+18, 194, 19, '0xe0e9dc', False, start)
            for i in range(3):
                filters.append(f'drawbox=x={28+i*415}:y=941:w=394:h=4:color={"0xd3eea3" if i==number else "0xffffff@0.3"}:t=fill')
            clip = folder / f'{number}.mp4'
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,'-t','9','-vf',','.join(filters),'-an','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p',str(clip)],check=True)
            clips.append(clip)
        manifest = folder / 'concat.txt'
        manifest.write_text(''.join(f"file '{path}'\n" for path in clips))
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy','-movflags','+faststart',str(out/'demo.mp4')],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','3','-i',str(out/'demo.mp4'),'-frames:v','1',str(out/'poster.jpg')],check=True)
    (out/'scenario.json').write_text(json.dumps({'type':'fictional_product_demonstration','business_metrics_simulated':True,'tracking_boxes': 'model_detections' if args.tracking_dir else 'none','duration_seconds':27,'scenes':[{'business':name,'start_s':i*9,'duration_s':9,'illustrative_cards':[dict(zip(['label','value','detail'],card)) for card in cards]} for i,(name,_,cards) in enumerate(SCENES)]},ensure_ascii=False,indent=2))
    print(out/'demo.mp4')


if __name__ == '__main__':
    main()
