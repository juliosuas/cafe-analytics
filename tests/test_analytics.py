import copy
import numpy as np
import pytest
from cafe_analytics.analytics import Analytics, validate_config
from cafe_analytics.tracker import Tracker


CONFIG = {"zones": [{"name": "all", "polygon": [[0,0],[1,0],[1,1],[0,1]]}],
          "gates": [{"name": "door", "points": [[0.5,0.2],[0.5,0.8]], "in_direction": "positive_to_negative", "hysteresis": 0.01}]}


def test_dwell_uses_media_time_and_excludes_lost_gap():
    a = Analytics(CONFIG)
    for t in [0, 0.1, 0.2, 2, 2.1]:
        a.update([(1, [0.2, 0.5])], t)
    zones = a.finish()
    assert zones[0]["observed_person_seconds"] == pytest.approx(0.3)
    assert zones[0]["visits"] == 2
    assert a.heat.sum() == pytest.approx(0.3)
    assert a.visits[0]["end_reason"] == "observation_gap"


def test_segment_crossings_and_hysteresis():
    a = Analytics(CONFIG)
    for i, x in enumerate([0.4, 0.499, 0.501, 0.499, 0.6, 0.7, 0.4]):
        a.update([(1, [x, 0.5])], i * 0.1)
    assert a.counts["door"] == {"in": 1, "out": 1}
    assert len(a.events) == 2


def test_crossing_infinite_extension_does_not_count():
    a = Analytics(CONFIG)
    a.update([(1, [0.4, 0.95])], 0)
    a.update([(1, [0.6, 0.95])], 0.1)
    assert a.counts["door"] == {"in": 0, "out": 0}


def test_reappearance_does_not_create_crossing():
    a = Analytics(CONFIG)
    a.update([(1, [0.4, 0.5])], 0)
    a.update([], 0.6)
    a.update([(1, [0.6, 0.5])], 0.8)
    assert a.counts["door"]["in"] == 0
    assert a.visits[0]["end_s"] == 0


def test_empty_video_metrics():
    a = Analytics(CONFIG)
    a.update([], 0)
    assert a.finish()[0]["observed_person_seconds"] == 0
    assert not a.people


def test_exit_does_not_inflate_dwell_or_appear_as_entry():
    cfg = copy.deepcopy(CONFIG)
    cfg["zones"][0]["polygon"] = [[0,0],[0.5,0],[0.5,1],[0,1]]
    a = Analytics(cfg)
    for t, x in [(0,0.2),(0.1,0.3),(0.2,0.7)]:
        a.update([(1,[x,0.5])],t)
    a.finish()
    assert a.visits[0]["observed_seconds"] == pytest.approx(0.1)
    assert a.visits[0]["censored"] is False


def test_invalid_geometry_rejected():
    cfg = copy.deepcopy(CONFIG)
    cfg["zones"][0]["polygon"][0] = [2,0]
    with pytest.raises(ValueError):
        validate_config(cfg)
    cfg = copy.deepcopy(CONFIG)
    cfg["zones"][0]["polygon"] = [[0,0],[1,1],[1,0],[0,1]]
    with pytest.raises(ValueError):
        validate_config(cfg)


def det(x, score=0.9):
    return [x, 10, x+40, 100, score]


def test_tracker_id_survives_short_occlusion_and_low_score():
    tracker = Tracker(min_hits=2)
    assert tracker.update(np.array([det(10)]), 0) == []
    tid = tracker.update(np.array([det(12)]), 0.1)[0].id
    tracker.update(np.empty((0,5)), 0.2)
    assert tracker.update(np.array([det(16,0.2)]), 0.3)[0].id == tid
    assert tracker.update(np.array([det(18)]), 1.5) == []
    assert tracker.update(np.array([det(20)]), 1.6)[0].id != tid


def test_low_confidence_does_not_spawn_ids():
    tracker = Tracker(min_hits=1)
    assert tracker.update(np.array([det(10,0.2)]), 0) == []


def test_detection_order_does_not_swap_ids():
    tracker = Tracker(min_hits=1)
    tracks = tracker.update(np.array([det(10),det(200)]),0)
    ids = [t.id for t in tracks]
    tracks = tracker.update(np.array([det(198),det(12)]),0.1)
    assert [t.id for t in tracks] == ids
    assert tracks[0].box[0] == 12
