"""Deterministic, evidence-linked session brief. No business outcome inference."""
import html
import json


class SessionEvidence:
    """Constant memory per zone; keep the first frame at each observed peak."""

    def __init__(self, zones):
        self.frames = 0
        self.zones = {z["name"]: {"frames_with_presence": 0, "peak": 0,
                                   "peak_time_s": None, "peak_frame": None} for z in zones}

    def update(self, occupancy, timestamp, frame):
        self.frames += 1
        for name, count in occupancy.items():
            zone = self.zones[name]
            zone["frames_with_presence"] += int(count > 0)
            if count > zone["peak"]:
                zone.update(peak=count, peak_time_s=float(timestamp), peak_frame=int(frame))


def build_brief(summary, evidence):
    """Only observed facts, missing evidence and review prompts; never causal advice."""
    if evidence.frames != summary["frames_processed"]:
        raise ValueError("La evidencia debe cubrir todos los fotogramas procesados")
    zones = []
    for z in summary["zones"]:
        e = evidence.zones[z["zone"]]
        if e["peak"] != z["peak_observed_occupancy"]:
            raise ValueError("El pico de ocupacion no coincide con la evidencia")
        zones.append({
            "zone": z["zone"],
            "observed_person_seconds": z["observed_person_seconds"],
            "peak_observed_occupancy": e["peak"],
            "first_peak_time_s": e["peak_time_s"], "first_peak_frame": e["peak_frame"],
            "frames_with_presence": e["frames_with_presence"],
            "presence_frame_fraction": e["frames_with_presence"] / evidence.frames,
            "visits": z["visits"], "censored_visits": z["censored_visits"],
            "mean_observed_visit_s": z["mean_observed_visit_s"],
            "review_question": "¿Qué ocurre en esta zona cuando alcanza su máximo observado?"
                if e["peak"] else "¿La zona está visible y bien configurada? No hubo detecciones confirmadas.",
            "next_step": "Revisar el fragmento y anotar el contexto antes de cambiar la operación."
                if e["peak"] else "Verificar el encuadre y el detector antes de interpretar este cero.",
        })
    brief = {
        "schema_version": 1, "run_id": summary["run_id"], "scope": "session",
        "video_seconds": summary["video_seconds"], "frames_processed": evidence.frames,
        "business_conclusions": "insufficient_evidence",
        "coverage": {"kind": "processed_frames_only", "business_day_fraction": None,
                     "timestamp_mode": summary["timestamp_mode"], "stop_reason": summary["stop_reason"]},
        "access_flow": {"status": "configured_lines_unvalidated" if summary["gate_counts"] else "not_configured",
                        "counts": summary["gate_counts"] or None},
        "zones": zones,
        "limitations": [
            "Es un resumen de esta sesión, no un reporte diario ni una comparación histórica.",
            "La precisión en este local y la cobertura de la jornada no están validadas.",
            "No distingue empleados de clientes; los IDs pueden fragmentarse o intercambiarse.",
            "Permanencia no equivale a espera, atención, compra ni abandono.",
            "La media incluye visitas parciales; el cierre de una visita no garantiza que se vio su inicio.",
            "La presencia se expresa por fotogramas, no como porcentaje del tiempo ni de capacidad.",
        ],
        "scene_note": summary["scene_note"],
        "size_filter": summary.get("size_filter", {"min_person_height": 0, "discarded_detection_samples": 0}),
        "evidence": {"video": "annotated.mp4", "timeline": "occupancy.csv",
                     "summary": "summary.json", "visits": "visits.csv"},
    }
    if brief["size_filter"]["min_person_height"] > 0:
        brief["limitations"].append(
            f"Filtro de esta cámara: altura mínima de caja {brief['size_filter']['min_person_height']:.0%} de la imagen. "
            "Puede omitir personas pequeñas o lejanas; requiere validación independiente.")
    return brief


def save_owner_brief(out, summary, evidence):
    brief = build_brief(summary, evidence)
    (out / "owner-summary.json").write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")
    cards = []
    for z in brief["zones"]:
        t = z["first_peak_time_s"]
        # Camera analytics uses capture time; its MP4 uses nominal FPS. Link by frame.
        playback = z["first_peak_frame"] / summary["source_fps"] if t is not None else None
        link = (f'<a href="annotated.mp4#t={max(0, playback - 1):.3f}">Revisar evidencia · '
                f'{t:.2f} s de sesión ↗</a>') if t is not None else '<p>Sin instante de presencia confirmado.</p>'
        cards.append(f'''<article><p class="eyebrow">{html.escape(z['zone'].replace('_', ' '))}</p>
<h2>{z['peak_observed_occupancy']} {'persona' if z['peak_observed_occupancy'] == 1 else 'personas'}</h2><p>Máximo observado simultáneamente en la zona.</p>
<dl><dt>Presencia acumulada</dt><dd>{z['observed_person_seconds']:.2f} persona-segundos</dd>
<dt>Fotogramas con presencia</dt><dd>{z['frames_with_presence']} / {brief['frames_processed']}</dd>
<dt>Media de permanencia observada</dt><dd>{z['mean_observed_visit_s']:.2f} s / visita</dd>
<dt>Visitas con cierre parcial</dt><dd>{z['censored_visits']} / {z['visits']}</dd></dl>
{link}<h3>Pregunta para revisar</h3><p>{html.escape(z['review_question'])}</p>
<p>{html.escape(z['next_step'])}</p></article>''')
    access = ('Hay líneas configuradas. Sus cruces necesitan validación antes de interpretarse como entradas al negocio.'
              if brief['access_flow']['counts'] is not None else
              'Entradas y salidas: no disponibles. Esta sesión no tiene una línea de acceso configurada; no significa cero clientes.')
    document = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Resumen para el dueño · Café Analytics</title>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#f4f3ec;color:#16372e;font:16px system-ui}}main{{max-width:1080px;margin:auto;padding:36px 24px}}h1{{font-size:clamp(32px,5vw,52px);letter-spacing:-1.5px}}h2{{font-size:32px}}p,li{{line-height:1.7}}a{{color:#215c41}}.eyebrow{{font-size:12px;text-transform:uppercase;letter-spacing:1px}}.notice{{padding:20px;background:#f4e6c8;border-radius:12px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:20px;margin:28px 0}}article{{background:white;border:1px solid #d4dcd2;border-radius:14px;padding:26px}}dl{{font-size:14px}}dt{{color:#5c6d65;margin-top:14px}}dd{{margin:3px 0 0;font-weight:600}}nav{{display:flex;gap:20px;flex-wrap:wrap}}video{{width:100%;border-radius:12px}}a:focus-visible{{outline:3px solid #be6814;outline-offset:4px}}</style></head>
<body><main><nav><a href="report.html">Reporte técnico</a><a href="owner-summary.json">Datos de este resumen</a></nav>
<p class="eyebrow">Café Analytics · Resumen de sesión</p><h1>Qué se observó. Qué conviene revisar.</h1>
<p>{brief['video_seconds']:.2f} segundos · {brief['frames_processed']} fotogramas · sesión {html.escape(brief['run_id'][:8])}</p>
<div class="notice"><strong>Evidencia insuficiente para una conclusión comercial.</strong><br>Este resumen local ayuda a encontrar momentos para revisar. No recomienda personal, compras ni cambios de horario.</div>
<p>{html.escape(brief['scene_note'])}</p><video controls playsinline preload="metadata" poster="preview.jpg" src="annotated.mp4"></video>
<div class="grid">{''.join(cards)}</div><p>{access}</p>
<h2>Antes de tomar una decisión</h2><ul>{''.join('<li>'+html.escape(x)+'</li>' for x in brief['limitations'])}</ul>
<p>El siguiente paso es validar una pregunta concreta con una cámara fija y una muestra representativa del local.</p>
<nav><a href="occupancy.csv">Ocupación por fotograma</a><a href="visits.csv">Permanencias observadas</a><a href="summary.json">Resumen técnico</a></nav>
</main></body></html>'''
    (out / "owner.html").write_text(document, encoding="utf-8")
    return brief
