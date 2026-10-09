import json
import pytest
from cafe_analytics.owner import SessionEvidence, build_brief, save_owner_brief


def example(name="barra", counts=(0, 2, 2, 1), gates=None):
    evidence = SessionEvidence([{"name": name}])
    for frame, count in enumerate(counts):
        evidence.update({name: count}, frame * 0.2, frame)
    summary = {"run_id": "test-session", "frames_processed": len(counts), "video_seconds": len(counts) * 0.2,
               "source_fps": 5, "timestamp_mode": "container_pts", "stop_reason": "end_of_file",
               "scene_note": "Clip ilustrativo", "gate_counts": gates or {},
               "zones": [{"zone": name, "observed_person_seconds": 0.6, "peak_observed_occupancy": max(counts),
                          "visits": 2, "censored_visits": 2, "mean_observed_visit_s": 0.3}]}
    return summary, evidence


def test_peak_evidence_and_zero_frames_are_preserved():
    summary, evidence = example()
    brief = build_brief(summary, evidence)
    zone = brief["zones"][0]
    assert zone["peak_observed_occupancy"] == 2
    assert zone["first_peak_time_s"] == 0.2
    assert zone["first_peak_frame"] == 1
    assert zone["presence_frame_fraction"] == 0.75
    assert zone["censored_visits"] == 2
    assert brief["business_conclusions"] == "insufficient_evidence"
    assert brief["coverage"]["business_day_fraction"] is None


def test_unconfigured_access_is_unknown_not_zero_customers():
    brief = build_brief(*example(counts=(0, 0)))
    assert brief["access_flow"] == {"status": "not_configured", "counts": None}
    assert brief["zones"][0]["first_peak_time_s"] is None
    assert brief["zones"][0]["presence_frame_fraction"] == 0
    measured = build_brief(*example(gates={"puerta": {"in": 0, "out": 0}}))
    assert measured["access_flow"]["counts"]["puerta"]["in"] == 0
    assert measured["access_flow"]["status"] == "configured_lines_unvalidated"


def test_rejects_incomplete_evidence():
    summary, evidence = example()
    summary["frames_processed"] += 1
    with pytest.raises(ValueError, match="fotogramas"):
        build_brief(summary, evidence)


def test_report_escapes_labels_and_uses_frame_time_for_webcam_video(tmp_path):
    summary, evidence = example(name='<script>alert("x")</script>')
    # Camera capture time and MP4 playback time may differ considerably.
    evidence.zones[next(iter(evidence.zones))]["peak_time_s"] = 60
    summary["timestamp_mode"] = "monotonic_capture"
    summary["scene_note"] = "<img src=x onerror=alert(1)>"
    save_owner_brief(tmp_path, summary, evidence)
    page = (tmp_path / "owner.html").read_text()
    assert "<script>" not in page and "<img src=x" not in page
    assert "&lt;script&gt;" in page
    assert 'annotated.mp4#t=0.000' in page
    assert "60.00 s de sesión" in page
    assert json.loads((tmp_path / "owner-summary.json").read_text())["scope"] == "session"


def test_active_size_filter_is_disclosed():
    summary, evidence = example()
    summary['size_filter'] = {'min_person_height': .2, 'discarded_detection_samples': 9}
    brief = build_brief(summary, evidence)
    assert brief['size_filter']['discarded_detection_samples'] == 9
    assert any('20%' in item and 'omitir' in item for item in brief['limitations'])
