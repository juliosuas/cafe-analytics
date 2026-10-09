"""Render the fictional product demo; this script never runs analytics.

Requires ffmpeg with drawtext. Input sources and licenses are in SOURCES.md.
All displayed metrics are authored examples, not model outputs.
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
            filters = ['scale=1280:720:force_original_aspect_ratio=decrease',
                       'pad=1280:720:(ow-iw)/2:(oh-ih)/2', 'setsar=1', 'fps=30',
                       'drawbox=x=0:y=0:w=1280:h=82:color=0x10291f@0.96:t=fill']
            def text(value, x, y, size, color='white', bold=False, start=0):
                path = folder / f'text-{number}-{len(filters)}.txt'
                path.write_text(value, encoding='utf-8')
                font = args.bold_font if bold else args.font
                filters.append(f"drawtext=fontfile='{font}':textfile='{path}':x={x}:y={y}:fontsize={size}:fontcolor={color}:enable='gte(t,{start})'")
            text('PULSO / LOCAL', 28, 17, 21, '0xd3eea3', True)
            text(name, 28, 45, 20)
            text('DEMO ILUSTRATIVA · DATOS SIMULADOS', 775, 29, 20, '0xd3eea3', True)
            for i, (label, value, detail) in enumerate(cards):
                x = 28 + i * 415
                start = 0.35 + i * 0.45
                filters.extend([
                    f"drawbox=x={x}:y=526:w=394:h=158:color=0x10291f@0.93:t=fill:enable='gte(t,{start})'",
                    f"drawbox=x={x}:y=526:w=394:h=3:color=0xd3eea3:t=fill:enable='gte(t,{start})'",
                ])
                text(label, x+18, 544, 18, '0xd3eea3', True, start)
                text(value, x+18, 574, 40, 'white', True, start)
                text(detail, x+18, 636, 19, '0xe0e9dc', False, start)
            for i in range(3):
                filters.append(f'drawbox=x={28+i*415}:y=701:w=394:h=4:color={"0xd3eea3" if i==number else "0xffffff@0.3"}:t=fill')
            clip = folder / f'{number}.mp4'
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,'-t','9','-vf',','.join(filters),'-an','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p',str(clip)],check=True)
            clips.append(clip)
        manifest = folder / 'concat.txt'
        manifest.write_text(''.join(f"file '{path}'\n" for path in clips))
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy','-movflags','+faststart',str(out/'demo.mp4')],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','3','-i',str(out/'demo.mp4'),'-frames:v','1',str(out/'poster.jpg')],check=True)
    (out/'scenario.json').write_text(json.dumps({'type':'fictional_product_demonstration','all_metrics_simulated':True,'duration_seconds':27,'scenes':[{'business':name,'start_s':i*9,'duration_s':9,'illustrative_cards':[dict(zip(['label','value','detail'],card)) for card in cards]} for i,(name,_,cards) in enumerate(SCENES)]},ensure_ascii=False,indent=2))
    print(out/'demo.mp4')


if __name__ == '__main__':
    main()
