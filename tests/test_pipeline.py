"""Actual ONNX inference and simulated camera input; never opens a physical camera."""
import argparse
import json
from pathlib import Path
import cv2
import numpy as np
import pytest
from cafe_analytics.detector import Detector
from cafe_analytics import cli

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/yolox_s.onnx"
VIDEO = ROOT / "assets/retail.mp4"
pytestmark = pytest.mark.skipif(not MODEL.exists() or not VIDEO.exists(), reason="Descarga assets para pruebas de inferencia real")


def test_real_detector_finds_people_and_ignores_blank_frame():
    detector = Detector(MODEL)
    cap = cv2.VideoCapture(str(VIDEO))
    ok, frame = cap.read()
    cap.release()
    assert ok
    detections = detector(frame)
    assert len(detections) > 0
    assert np.isfinite(detections).all()
    assert np.all(detections[:, 2:4] > detections[:, :2])
    assert len(detector(np.zeros((540, 960, 3), dtype=np.uint8))) == 0


def test_webcam_branch_with_recorded_source_and_unknown_fps(monkeypatch, tmp_path):
    actual_capture = cv2.VideoCapture
    opened = []

    class SimulatedCamera:
        def __init__(self, index):
            opened.append(index)
            self.cap = actual_capture(str(VIDEO))
            self.frames = 0

        def isOpened(self):
            return self.cap.isOpened()

        def get(self, prop):
            return 0 if prop == cv2.CAP_PROP_FPS else self.cap.get(prop)

        def read(self):
            self.frames += 1
            return self.cap.read() if self.frames <= 6 else (False, None)

        def release(self):
            self.cap.release()

    monkeypatch.setattr(cli.cv2, "VideoCapture", SimulatedCamera)
    # Exercise MP4V fallback without external FFmpeg; detector remains real.
    monkeypatch.setattr(cli.shutil, "which", lambda _: None)
    out = tmp_path / "camera-test"
    args = argparse.Namespace(config=str(ROOT / "configs/demo.json"), max_seconds=None,
                              width=640, threads=2, low_score=0.12, confidence=0.4,
                              model=str(MODEL), output=str(out), webcam=0, source=None, preview=False)
    cli.run(args)
    summary = json.loads((out / "summary.json").read_text())
    assert opened == [0]
    assert summary["frames_processed"] == 6
    assert summary["timestamp_mode"] == "monotonic_capture"
    assert summary["source_fps"] == 30
    assert summary["video_seconds"] > 0
    assert summary["video_codec"] == "mp4v"
    assert summary["confirmed_track_ids"] > 0
    assert (out / "report.html").exists()
    import csv
    with (out / "occupancy.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 6 * len(summary["zones"])
    assert {int(row["frame"]) for row in rows} == set(range(6))
    brief = json.loads((out / "owner-summary.json").read_text())
    assert brief["coverage"]["timestamp_mode"] == "monotonic_capture"
    assert (out / "owner.html").exists()


@pytest.mark.skipif(not (ROOT / "assets/cafe-counter.mp4").exists(), reason="Descarga --demo cafe para regresion de figuras impresas")
def test_cafe_poster_filter_preserves_two_visible_people():
    from cafe_analytics.detector import filter_by_height
    cap = cv2.VideoCapture(str(ROOT / "assets/cafe-counter.mp4"))
    cap.set(cv2.CAP_PROP_POS_FRAMES, 90)
    ok, frame = cap.read()
    cap.release()
    assert ok
    frame = cv2.resize(frame, (960, 506))
    detections = Detector(MODEL)(frame)
    filtered = filter_by_height(detections, 506, 0.2)
    # Manually inspected frame: two physical people and a small printed figure.
    strong = filtered[filtered[:, 4] >= 0.4]
    assert len(strong) == 2
    assert len(filtered) < len(detections)
    assert sum((b[0] + b[2]) / 2 < 480 for b in strong) == 1
