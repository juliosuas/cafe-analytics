"""Independent integrity check of a completed run (not an accuracy benchmark)."""
import csv
import json
from pathlib import Path
import sys
import cv2
import numpy as np


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verify(directory):
    root = Path(directory)
    summary = json.loads((root / "summary.json").read_text())
    cap = cv2.VideoCapture(str(root / "annotated.mp4"))
    decoded = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        assert frame.size > 0
        decoded += 1
    cap.release()
    assert decoded == summary["frames_processed"] > 0
    people = read_csv(root / "tracks.csv")
    ids = {row["track_id"] for row in people}
    assert len(ids) == summary["confirmed_track_ids"]
    events = read_csv(root / "events.csv")
    paths = read_csv(root / "trajectories.csv")
    assert all(row["track_id"] in ids for row in paths + events)
    for gate, counts in summary["gate_counts"].items():
        for direction in ("in", "out"):
            assert counts[direction] == sum(e["gate"] == gate and e["direction"] == direction for e in events)
    visits = read_csv(root / "visits.csv")
    for visit in visits:
        assert 0 <= float(visit["observed_seconds"]) <= float(visit["end_s"]) - float(visit["start_s"]) + 1e-6
    for zone in summary["zones"]:
        total = sum(float(v["observed_seconds"]) for v in visits if v["zone"] == zone["zone"])
        assert abs(total - zone["observed_person_seconds"]) < 1e-6
    heat = np.load(root / "heatmap_seconds.npy")
    assert np.isfinite(heat).all() and (heat >= 0).all()
    assert abs(heat.sum() - sum(float(p["observed_seconds"]) for p in people)) < 1e-6
    for name in ("preview.jpg", "heatmap.jpg", "trajectories.jpg"):
        assert cv2.imread(str(root / name)) is not None
    # Added in 0.1.1; old archived runs remain verifiable without these files.
    if (root / "owner-summary.json").exists():
        brief = json.loads((root / "owner-summary.json").read_text())
        timeline = read_csv(root / "occupancy.csv")
        assert brief["run_id"] == summary["run_id"]
        assert brief["frames_processed"] == decoded
        assert len(timeline) == decoded * len(summary["zones"])
        for z in brief["zones"]:
            rows = [r for r in timeline if r["zone"] == z["zone"]]
            assert [int(r["frame"]) for r in rows] == list(range(decoded))
            assert all(r["run_id"] == summary["run_id"] for r in rows)
            counts = [int(r["observed_occupancy"]) for r in rows]
            assert all(n >= 0 for n in counts)
            assert max(counts) == z["peak_observed_occupancy"]
            assert sum(n > 0 for n in counts) == z["frames_with_presence"]
            assert abs(z["presence_frame_fraction"] - sum(n > 0 for n in counts) / decoded) < 1e-9
            if max(counts):
                first = counts.index(max(counts))
                assert first == z["first_peak_frame"]
                assert abs(float(rows[first]["time_s"]) - z["first_peak_time_s"]) < 1e-6
            else:
                assert z["first_peak_time_s"] is None and z["first_peak_frame"] is None
        assert brief["access_flow"]["counts"] == (summary["gate_counts"] or None)
        assert (root / "owner.html").stat().st_size > 1000
    assert (root / "report.html").stat().st_size > 1000
    result = {"passed": True, "decoded_video_frames": decoded, "confirmed_ids": len(ids), "trajectory_samples": len(paths), "crossing_events": len(events), "heatmap_person_seconds": float(heat.sum())}
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    verify(sys.argv[1])
