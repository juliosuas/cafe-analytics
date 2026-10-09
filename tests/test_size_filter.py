import numpy as np
import pytest
from cafe_analytics.analytics import validate_config
from cafe_analytics.detector import filter_by_height


def test_size_filter_is_opt_in_and_keeps_boundary():
    boxes = np.array([[10, 10, 30, 19, .9], [0, 0, 20, 20, .8], [0, 0, 50, 90, .7]])
    assert np.array_equal(filter_by_height(boxes, 100), boxes)
    assert np.array_equal(filter_by_height(boxes, 100, .2), boxes[1:])
    assert filter_by_height(np.empty((0, 5)), 100, .2).shape == (0, 5)


@pytest.mark.parametrize("value", [-1, 1, float("nan"), float("inf"), True, "0.2"])
def test_invalid_size_calibration_rejected(value):
    with pytest.raises(ValueError, match="min_person_height"):
        validate_config({"min_person_height": value, "zones": [{"name": "all", "polygon": [[0,0],[1,0],[1,1],[0,1]]}]})
