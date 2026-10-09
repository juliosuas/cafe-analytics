import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
import shutil
import subprocess
import time
import uuid
import cv2
import numpy as np
from .analytics import Analytics, anchor, validate_config
from .detector import Detector, filter_by_height
from .tracker import Tracker
from .report import color, draw_config, save_report
from .owner import SessionEvidence, save_owner_brief


def run(args):
    config = validate_config(json.loads(Path(args.config).read_text(encoding="utf-8")))
    if args.max_seconds is not None and args.max_seconds <= 0:
        raise ValueError("--max-seconds debe ser positivo")
    if args.width < 320 or args.width % 2 or args.threads < 1:
        raise ValueError("--width debe ser par y >=320; --threads debe ser positivo")
    if not 0 < args.low_score <= args.confidence < 1:
        raise ValueError("Se requiere 0 < low-score <= confidence < 1")
    model = Path(args.model)
    if not model.is_file():
        raise ValueError("Falta el modelo. Ejecuta python scripts/download_assets.py")
    out = Path(args.output)
    if out.exists() and any(out.iterdir()):
        raise ValueError("La carpeta de salida no esta vacia; elige otra para conservar los resultados")
    detector = Detector(model, args.low_score, args.threads)
    webcam = args.webcam is not None
    source = args.webcam if webcam else args.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        cap.release()
        raise ValueError("No se pudo abrir el video/camara. Revisa ruta o permisos de camara.")
    fps = cap.get(cv2.CAP_PROP_FPS)
    if webcam and (not np.isfinite(fps) or fps <= 0):
        fps = 30.0  # Container playback only; analytics uses monotonic capture time.
    if not np.isfinite(fps) or fps <= 0:
        cap.release()
        raise ValueError("La fuente no indica FPS validos; convierte el archivo a FPS constantes")
    out.mkdir(parents=True, exist_ok=True)
    (out / "config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    analytics = Analytics(config)
    evidence = SessionEvidence(config["zones"])
    tracker = Tracker(high_score=args.confidence)
    run_id = str(uuid.uuid4())
    processed = frame_index = 0
    filtered_detections = 0
    writer = None
    start = time.monotonic()
    first_capture = None
    last_time = 0.0
    timestamp_mode = "monotonic_capture" if webcam else "container_pts"
    background = trajectory_image = None
    previous_points = {}
    stopped = "end_of_file"
    path_file = (out / "trajectories.csv").open("w", newline="", encoding="utf-8")
    paths = csv.writer(path_file)
    paths.writerow(["run_id", "frame", "time_s", "track_id", "x_normalized", "y_normalized", "confidence"])
    occupancy_file = (out / "occupancy.csv").open("w", newline="", encoding="utf-8")
    occupancy_rows = csv.writer(occupancy_file)
    occupancy_rows.writerow(["run_id", "frame", "time_s", "zone", "observed_occupancy"])
    try:
        while True:
            ok, original = cap.read()
            captured_at = time.monotonic()
            if not ok:
                stopped = "capture_ended" if webcam else "end_of_file"
                break
            if first_capture is None:
                first_capture = captured_at
            timestamp = captured_at - first_capture if webcam else cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            if not webcam and (not np.isfinite(timestamp) or (processed and timestamp <= last_time)):
                timestamp = last_time + 1 / fps if processed else 0.0
                timestamp_mode = "fps_fallback"
            if args.max_seconds is not None and timestamp >= args.max_seconds:
                stopped = "duration_limit"
                break
            height = max(2, round(original.shape[0] * args.width / original.shape[1] / 2) * 2)
            frame = cv2.resize(original, (args.width, height))
            if background is None:
                background = frame.copy()
                trajectory_image = frame.copy()
                draw_config(trajectory_image, config)
                writer = cv2.VideoWriter(str(out / "annotated.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), fps, (args.width, height))
                if not writer.isOpened():
                    raise RuntimeError("No se pudo crear el video MP4")
            detections = detector(frame)
            accepted = filter_by_height(detections, height, config.get("min_person_height", 0))
            filtered_detections += len(detections) - len(accepted)
            detections = accepted
            tracks = tracker.update(detections, timestamp)
            observations = [(t.id, anchor(t.box, args.width, height, config.get("anchor", "bottom_center"))) for t in tracks]
            occupancy = analytics.update(observations, timestamp)
            evidence.update(occupancy, timestamp, frame_index)
            for name, count in occupancy.items():
                occupancy_rows.writerow([run_id, frame_index, f"{timestamp:.6f}", name, count])
            draw_config(frame, config)
            for track, (_, point) in zip(tracks, observations):
                pixel = tuple((point * [args.width, height]).astype(int))
                prior = previous_points.get(track.id)
                if prior and timestamp - prior[0] <= analytics.max_gap:
                    cv2.line(trajectory_image, prior[1], pixel, color(track.id), 2)
                elif prior:
                    track.trail.clear()
                previous_points[track.id] = (timestamp, pixel)
                track.trail.append(pixel)
                if len(track.trail) > 1:
                    cv2.polylines(frame, [np.array(track.trail, np.int32)], False, color(track.id), 2)
                x1, y1, x2, y2 = track.box.astype(int)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color(track.id), 2)
                cv2.circle(frame, pixel, 4, color(track.id), -1)
                label = f"ID {track.id}  {track.score:.2f}"
                cv2.putText(frame, label, (x1, max(78, y1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.48, color(track.id), 2)
                paths.writerow([run_id, frame_index, f"{timestamp:.6f}", track.id, f"{point[0]:.6f}", f"{point[1]:.6f}", f"{track.score:.4f}"])
            cv2.rectangle(frame, (0, 0), (args.width, 65), (31, 26, 17), -1)
            counts = "  ".join(f"{name}: IN {v['in']} OUT {v['out']}" for name, v in analytics.counts.items())
            cv2.putText(frame, f"CAFE ANALYTICS | {timestamp:05.1f}s | visibles {len(tracks)} | {counts}", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 245, 225), 1)
            cv2.putText(frame, "  ".join(f"{name}: {v}" for name, v in occupancy.items()), (15, 49), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (210, 210, 210), 1)
            writer.write(frame)
            if processed == 0 or processed == 90:
                cv2.imwrite(str(out / "preview.jpg"), frame)
            processed += 1
            frame_index += 1
            last_time = timestamp
            if processed % 60 == 0:
                print(f"{processed} frames | {timestamp:.1f}s | {len(analytics.people)} IDs confirmados", flush=True)
            if args.preview:
                cv2.imshow("Cafe Analytics - Q para terminar", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    stopped = "user_stopped"
                    break
    except KeyboardInterrupt:
        stopped = "interrupted"
    finally:
        cap.release()
        if writer:
            writer.release()
        path_file.close()
        occupancy_file.close()
        if args.preview:
            cv2.destroyAllWindows()
    if not processed:
        raise ValueError("No se pudo procesar ningun fotograma")
    elapsed = time.monotonic() - start
    codec = "mp4v"
    if shutil.which("ffmpeg"):
        converted = out / "annotated.h264.mp4"
        result = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(out / "annotated.mp4"), "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(converted)], capture_output=True)
        if result.returncode == 0:
            converted.replace(out / "annotated.mp4")
            codec = "h264"
        else:
            converted.unlink(missing_ok=True)
            print("FFmpeg no pudo convertir; se conserva MP4V", flush=True)
    summary = {"schema_version": 1, "run_id": run_id, "source": str(source), "webcam": webcam,
               "frames_processed": processed, "video_seconds": last_time + (0 if webcam else 1 / fps),
               "source_fps": fps, "processing_seconds": elapsed, "processing_fps": processed / elapsed,
               "confirmed_track_ids": len(analytics.people), "gate_counts": analytics.counts,
               "zones": analytics.finish(), "timestamp_mode": timestamp_mode, "stop_reason": stopped,
               "model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
               "provider": "CPUExecutionProvider", "platform": platform.platform(),
               "python": platform.python_version(), "video_codec": codec,
               "scene_note": config.get("scene_note", "Usa camara fija y calibra las zonas y el acceso real."),
               "webcam_playback_note": "Webcam: MP4 a FPS nominales; tiempos reales en CSV/JSON." if webcam else None,
               "max_observation_gap_s": analytics.max_gap, "config": config}
    summary["size_filter"] = {"min_person_height": config.get("min_person_height", 0),
                              "discarded_detection_samples": filtered_detections}
    save_report(out, summary, analytics, background, trajectory_image)
    save_owner_brief(out, summary, evidence)
    print(json.dumps({"report": str(out / "report.html"), "frames": processed, "ids": len(analytics.people), "fps": round(processed / elapsed, 2)}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Analytics local de personas, sin biometria")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("run", help="Procesar un archivo o webcam")
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--source", help="Ruta a un video local")
    source.add_argument("--webcam", type=int, help="Indice de camara, normalmente 0")
    p.add_argument("--config", required=True)
    p.add_argument("--model", default="models/yolox_s.onnx")
    p.add_argument("--output", default="runs/session")
    p.add_argument("--max-seconds", type=float)
    p.add_argument("--width", type=int, default=960)
    p.add_argument("--threads", type=int, default=4)
    p.add_argument("--confidence", type=float, default=0.4)
    p.add_argument("--low-score", type=float, default=0.12)
    p.add_argument("--preview", action="store_true")
    editor = sub.add_parser("configure", help="Crear editor visual HTML para un video")
    editor_source = editor.add_mutually_exclusive_group(required=True)
    editor_source.add_argument("--source")
    editor_source.add_argument("--webcam", type=int)
    editor.add_argument("--output", default="zone-editor.html")
    args = parser.parse_args()
    try:
        if args.command == "run":
            run(args)
        else:
            from .editor import create_editor
            create_editor(args.webcam if args.webcam is not None else args.source, args.output)
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
