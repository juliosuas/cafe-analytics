# Contrato de datos · schema_version 1

Cada ejecución crea un `run_id` UUID. Los IDs enteros son locales a esa ejecución: usa `(run_id, track_id)` al combinar sesiones. En CSV donde no aparece `run_id`, recupéralo del `summary.json` de la misma carpeta.

## Resumen JSON

`summary.json` contiene `schema_version`, `run_id`, `source`, `webcam`, `frames_processed`, `video_seconds`, `source_fps`, `processing_seconds`, `processing_fps`, `confirmed_track_ids`, `gate_counts`, `zones`, `timestamp_mode`, `stop_reason`, `model_sha256`, `provider`, `platform`, `python`, `video_codec`, `scene_note`, `webcam_playback_note`, `max_observation_gap_s` y la `config` exacta.

`source` puede contener la ruta de un archivo local. Revisa este campo antes de compartir un reporte propio. `processing_fps` mide el bucle, excluye carga de modelo, conversión final de video y reporte. No equivale a precisión ni FPS efectivos de una cámara operando sin interrupciones.

## Tablas

| Archivo | Columnas | Interpretación |
|---|---|---|
| `zones.csv` | zone, track_ids, visits, observed_person_seconds, mean_observed_visit_s, censored_visits, peak_observed_occupancy | Resumen por zona; media incluye visitas parciales |
| `tracks.csv` | track_id, first_seen_s, last_seen_s, observed_seconds, samples | Vida observada del ID confirmado, no identidad humana |
| `visits.csv` | track_id, zone, start_s, end_s, observed_seconds, end_reason, censored | Un episodio dentro de una zona |
| `events.csv` | time_s, track_id, gate, direction | Un cruce; direction es `in` o `out` |
| `trajectories.csv` | run_id, frame, time_s, track_id, x_normalized, y_normalized, confidence | Una muestra confirmada por fotograma/ID |
| `heatmap.csv` | grid_x, grid_y, person_seconds | 14,400 celdas de una cuadrícula 160×90 |

CSV: UTF-8 con encabezado; segundos decimales, no milisegundos. `frame` empieza en 0. `censored` se escribe `True`/`False`. Las imágenes se generan en coordenadas de pantalla, no metros.

### Cierres de visita

- `zone_exit`: salida observada; `censored=false`.
- `observation_gap`: regreso después de un hueco >0.5 s; episodio previo parcial.
- `track_lost`: sin observación durante más de 0.5 s.
- `end_of_run`: sesión terminada mientras la persona seguía en la zona.

`end_s` es la última observación dentro de la zona. `observed_seconds` puede ser menor que `end_s - start_s`, nunca debería ser mayor. No suma una duración inventada para un único fotograma.

## Invariantes

1. El número de frames decodificables del MP4 coincide con `frames_processed`.
2. Cada evento y trayectoria refiere un ID confirmado de `tracks.csv`.
3. Eventos agrupados por línea/dirección coinciden con `gate_counts`.
4. Suma de permanencias de visitas por zona coincide con el resumen de esa zona.
5. Suma de `heatmap_seconds.npy` coincide con suma de `observed_seconds` de pistas.
6. La suma por zonas puede superar el heatmap si las zonas se superponen, o ser menor si no cubren todo el cuadro.

Verificador: `python scripts/verify_run.py runs/mi-demo`. Ejecutar sin `python -O`, porque el verificador emplea aserciones.

## Evolución prevista

Añadir inicio absoluto de sesión, zona horaria, identificadores de cámara/local, cobertura y estado de salud antes de comparar días o generar reportes remotos. Cualquier cambio incompatible deberá incrementar `schema_version`; no reinterpretar archivos históricos silenciosamente.

## Evidencia de sesión añadida en 0.1.1

El `schema_version: 1` del resumen técnico se conserva; los nuevos archivos son adicionales.

| Archivo | Campos / contenido |
|---|---|
| `occupancy.csv` | run_id, frame, time_s, zone, observed_occupancy; una fila por zona por fotograma procesado, incluyendo cero |
| `owner-summary.json` | schema_version propio 1, run_id, scope=session, video_seconds, frames_processed, business_conclusions, coverage, access_flow, zones, limitations, scene_note, evidence |
| `owner.html` | Lectura de esa sesión con enlaces al video; no reporte diario |

Cada zona del resumen para el dueño conserva persona-segundos, pico, visitas, cierres parciales y media observada. Añade `first_peak_time_s`, `first_peak_frame`, `frames_with_presence`, `presence_frame_fraction` (fotogramas, no tiempo), una pregunta y un siguiente paso de revisión. Un pico de cero tiene instante y fotograma `null`.

`coverage.business_day_fraction` es `null`: no se conoce la cobertura del día. `business_conclusions` es siempre `insufficient_evidence` en esta versión: un video y estas métricas no validan decisiones comerciales. `access_flow.status` distingue `not_configured` (counts=null) de `configured_lines_unvalidated` (conteos que requieren calibración). No se infieren roles.

Para video, los instantes analíticos usan PTS; para webcam, reloj de captura. El enlace del reproductor usa `first_peak_frame / source_fps` para coincidir con el MP4 escrito a FPS nominales. El verificador comprueba la serie completa, sus picos y consistencia con el resumen. `occupancy.csv` tampoco garantiza continuidad de captura fuera de los fotogramas procesados.

`summary.json.size_filter` (campo adicional de 0.1.1) guarda `min_person_height` y `discarded_detection_samples`. El conteo se hace antes del tracker y agrega detecciones rechazadas en fotogramas, no individuos. El resumen para el dueño copia esa información y declara el riesgo de omitir personas pequeñas cuando el filtro está activo.
