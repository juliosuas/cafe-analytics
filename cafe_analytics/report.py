import csv
import html
import json
import cv2
import numpy as np


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def color(tid):
    return (80 + tid * 79 % 170, 90 + tid * 43 % 160, 80 + tid * 113 % 170)


def draw_config(frame, config):
    h, w = frame.shape[:2]
    overlay = frame.copy()
    for zone in config["zones"]:
        points = (np.array(zone["polygon"]) * [w, h]).astype(np.int32)
        cv2.fillPoly(overlay, [points], (160, 110, 25))
    frame[:] = cv2.addWeighted(frame, 0.86, overlay, 0.14, 0)
    for zone in config["zones"]:
        points = (np.array(zone["polygon"]) * [w, h]).astype(np.int32)
        cv2.polylines(frame, [points], True, (235, 205, 70), 2)
        cv2.putText(frame, zone["name"], tuple(points[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 240, 150), 1)
    for gate in config.get("gates", []):
        a, b = (np.array(gate["points"]) * [w, h]).astype(int)
        cv2.line(frame, tuple(a), tuple(b), (60, 225, 255), 3)
        center = (a + b) / 2
        delta = b - a
        normal = np.array([-delta[1], delta[0]], float)
        normal /= max(np.linalg.norm(normal), 1)
        if gate.get("in_direction", "negative_to_positive") == "positive_to_negative":
            normal *= -1
        end = (center + normal * 35).astype(int)
        cv2.arrowedLine(frame, tuple(center.astype(int)), tuple(end), (60, 225, 255), 2)
        cv2.putText(frame, gate["name"] + " IN", tuple(end), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (60, 225, 255), 1)


def save_report(out, summary, analytics, background, trajectory_image):
    zones = summary["zones"]
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(out / "zones.csv", zones, ["zone", "track_ids", "visits", "observed_person_seconds", "mean_observed_visit_s", "censored_visits", "peak_observed_occupancy"])
    write_csv(out / "visits.csv", analytics.visits, ["track_id", "zone", "start_s", "end_s", "observed_seconds", "end_reason", "censored"])
    write_csv(out / "tracks.csv", list(analytics.people.values()), ["track_id", "first_seen_s", "last_seen_s", "observed_seconds", "samples"])
    write_csv(out / "events.csv", analytics.events, ["time_s", "track_id", "gate", "direction"])
    np.save(out / "heatmap_seconds.npy", analytics.heat)
    write_csv(out / "heatmap.csv", [{"grid_x": x, "grid_y": y, "person_seconds": float(analytics.heat[y, x])} for y in range(90) for x in range(160)], ["grid_x", "grid_y", "person_seconds"])
    smooth = cv2.GaussianBlur(analytics.heat.astype(np.float32), (0, 0), 2)
    smooth = cv2.resize(smooth, (background.shape[1], background.shape[0]))
    normalized = smooth / max(float(smooth.max()), 1e-9)
    colors = cv2.applyColorMap((normalized * 255).astype(np.uint8), cv2.COLORMAP_TURBO)
    alpha = (normalized * 0.78)[..., None]
    heatmap = (background * (1 - alpha) + colors * alpha).astype(np.uint8)
    draw_config(heatmap, analytics.config)
    cv2.imwrite(str(out / "heatmap.jpg"), heatmap)
    cv2.imwrite(str(out / "trajectories.jpg"), trajectory_image)
    rows = "".join(f"<tr><td>{html.escape(z['zone'])}</td><td>{z['track_ids']}</td><td>{z['observed_person_seconds']:.1f} s</td><td>{z['mean_observed_visit_s']:.1f} s</td><td>{z['peak_observed_occupancy']}</td></tr>" for z in zones)
    incoming = sum(c["in"] for c in analytics.counts.values())
    outgoing = sum(c["out"] for c in analytics.counts.values())
    document = f'''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Café Analytics · Reporte local</title><style>
*{{box-sizing:border-box}}body{{background:#101a20;color:#e9efef;font:16px system-ui;margin:0}}main{{max-width:1200px;margin:auto;padding:40px 28px}}header{{display:flex;justify-content:space-between;align-items:center}}small,.muted{{color:#a1b4ba}}h1{{font-size:44px;letter-spacing:-2px;margin:14px 0 10px}}h2{{font-size:22px}}.badge{{color:#9af5c1;border:1px solid #3b6353;padding:9px 14px;border-radius:24px}}.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:30px 0}}.card,section{{background:#19272f;border:1px solid #30414b;border-radius:14px;padding:22px}}.number{{font-size:40px;font-weight:650;margin:10px 0}}video{{width:100%;border-radius:10px;background:#000}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px 0}}img{{width:100%;border-radius:8px}}table{{border-collapse:collapse;width:100%}}th,td{{padding:14px 8px;border-bottom:1px solid #33444e;text-align:left}}a{{color:#94e7c3}}nav{{display:flex;gap:18px;flex-wrap:wrap;margin:22px 0}}p{{line-height:1.6}}.note{{border-left:3px solid #d9bd7a;padding-left:16px;color:#c9d5d9}}@media(max-width:720px){{.cards,.grid{{grid-template-columns:1fr 1fr}}main{{padding:22px 14px}}h1{{font-size:34px}}table{{font-size:12px}}}}
</style><main><header><small>CAFÉ / ANALYTICS · MVP 0.1</small><span class="badge">Procesamiento local</span></header>
<h1>Movimiento que puedes medir.</h1><p class="muted">Sesión {html.escape(summary['run_id'][:8])} · {summary['video_seconds']:.1f} s de video · {summary['frames_processed']} fotogramas analizados</p>
<div class="cards"><div class="card"><small>IDs confirmados</small><div class="number">{summary['confirmed_track_ids']}</div><small>No equivale a clientes únicos</small></div><div class="card"><small>Cruces de entrada</small><div class="number">{incoming}</div><small>Según líneas configuradas</small></div><div class="card"><small>Cruces de salida</small><div class="number">{outgoing}</div><small>Según líneas configuradas</small></div><div class="card"><small>Velocidad de proceso</small><div class="number">{summary['processing_fps']:.1f}</div><small>Fotogramas por segundo</small></div></div>
<section><h2>La sesión, con contexto</h2><video controls preload="metadata" poster="preview.jpg" src="annotated.mp4"></video><p class="muted">ID, zonas, trayectorias y flecha de entrada. <a href="annotated.mp4">Abrir video</a> si tu navegador no admite el códec.</p></section>
<div class="grid"><section><h2>Tiempo de presencia</h2><img src="heatmap.jpg" alt="Mapa de presencia"><p class="muted">Frío → cálido: menor → mayor tiempo acumulado. Intensidad relativa a esta sesión.</p></section><section><h2>Trayectorias observadas</h2><img src="trajectories.jpg" alt="Trayectorias"><p class="muted">Un color por ID. Los huecos largos no se conectan.</p></section></div>
<section><h2>Actividad por zona</h2><table><thead><tr><th>Zona</th><th>IDs</th><th>Persona-segundos</th><th>Media / visita</th><th>Pico</th></tr></thead><tbody>{rows}</tbody></table><p class="muted">Tiempo observado: excluye huecos mayores de 0.5 s. Visitas cortadas por fin de video u oclusión se marcan en CSV; no son visitas completas.</p></section>
<nav>{''.join(f'<a href="{file}" download>{label}</a>' for file,label in [('summary.json','Resumen JSON'),('zones.csv','Zonas CSV'),('visits.csv','Visitas CSV'),('events.csv','Entradas / salidas'),('trajectories.csv','Trayectorias CSV'),('tracks.csv','IDs CSV'),('heatmap.csv','Heatmap CSV'),('config.json','Configuración')])}</nav>
<p class="note">{html.escape(summary.get('scene_note', 'Las zonas representan coordenadas de imagen: utiliza una cámara fija y calibra la línea en el acceso real.'))} Los IDs pueden fragmentarse o intercambiarse con oclusiones. Sin reconocimiento facial ni inferencias de edad, género o emoción.</p>
<p class="muted">Motor: YOLOX-S + ONNX Runtime CPU. Sin subir video a la nube.</p></main></html>'''
    (out / "report.html").write_text(document, encoding="utf-8")
