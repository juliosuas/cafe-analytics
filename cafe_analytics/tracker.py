"""Original geometric tracker: Kalman motion, Hungarian assignment, two score passes.

No appearance embeddings, face processing, or external tracking implementation.
"""
from collections import deque
import numpy as np
from scipy.optimize import linear_sum_assignment


def mm(a, b):
    # Tiny matrices: explicit contraction avoids platform BLAS floating-point
    # status anomalies and is inexpensive for the 4x4/8x8 filter.
    return np.einsum("ij,jk->ik", a, b, optimize=False)


def measurement(box):
    return np.r_[(box[:2] + box[2:4]) / 2, box[2:4] - box[:2]]


def iou(a, b):
    intersection = np.maximum(0, np.minimum(a[2:], b[2:]) - np.maximum(a[:2], b[:2])).prod()
    union = np.maximum(0, a[2:] - a[:2]).prod() + np.maximum(0, b[2:] - b[:2]).prod() - intersection
    return float(intersection / max(union, 1e-6))


class Track:
    def __init__(self, tid, detection, time):
        self.id = tid
        self.x = np.r_[measurement(detection[:4]), np.zeros(4)]
        self.p = np.diag([10.] * 4 + [1000.] * 4)
        self.box = detection[:4].copy()
        self.score = float(detection[4])
        self.last_seen = self.predicted_at = time
        self.hits = 1
        self.confirmed = False
        self.trail = deque(maxlen=150)

    def predict(self, time):
        dt = max(0, time - self.predicted_at)
        f = np.eye(8)
        f[:4, 4:] = np.eye(4) * dt
        self.x = f @ self.x
        self.x[2:4] = np.maximum(self.x[2:4], 2)
        self.p = mm(mm(f, self.p), f.T) + np.eye(8) * max(dt, 0.001) * 8
        self.predicted_at = time
        return np.r_[self.x[:2] - self.x[2:4] / 2, self.x[:2] + self.x[2:4] / 2]

    def update(self, detection, time, min_hits):
        h = np.eye(4, 8)
        noise = np.eye(4) * 4
        k = np.linalg.solve(mm(mm(h, self.p), h.T) + noise, mm(h, self.p)).T
        self.x += k @ (measurement(detection[:4]) - h @ self.x)
        ikh = np.eye(8) - mm(k, h)
        self.p = mm(mm(ikh, self.p), ikh.T) + mm(mm(k, noise), k.T)
        self.box = detection[:4].copy()
        self.score = float(detection[4])
        self.last_seen = time
        self.hits += 1
        self.confirmed = self.confirmed or self.hits >= min_hits


class Tracker:
    def __init__(self, max_age=1.0, min_hits=3, high_score=0.4):
        self.max_age, self.min_hits, self.high_score = max_age, min_hits, high_score
        self.tracks = []
        self.next_id = 1

    def update(self, detections, time):
        self.tracks = [t for t in self.tracks if time - t.last_seen <= self.max_age]
        predicted = [t.predict(time) for t in self.tracks]
        unmatched_t = set(range(len(self.tracks)))
        unmatched_d = set(range(len(detections)))
        for high_pass in (True, False):
            ti = sorted(i for i in unmatched_t if high_pass or self.tracks[i].confirmed)
            di = sorted(i for i in unmatched_d if (detections[i, 4] >= self.high_score) == high_pass)
            if not ti or not di:
                continue
            costs = np.full((len(ti), len(di)), 1e6)
            for row, i in enumerate(ti):
                for col, j in enumerate(di):
                    a, b = predicted[i], detections[j, :4]
                    overlap = iou(a, b)
                    distance = np.linalg.norm(measurement(a)[:2] - measurement(b)[:2])
                    scale = max(np.linalg.norm(a[2:] - a[:2]), 1)
                    # Reject distant candidates before solving the assignment.
                    if overlap >= 0.1 or (high_pass and distance / scale < 0.45):
                        costs[row, col] = 0.75 * (1 - overlap) + 0.25 * min(distance / scale, 1)
            rows, cols = linear_sum_assignment(costs)
            for row, col in zip(rows, cols):
                if costs[row, col] >= 1e5:
                    continue
                i, j = ti[row], di[col]
                self.tracks[i].update(detections[j], time, self.min_hits)
                unmatched_t.remove(i)
                unmatched_d.remove(j)
        for j in sorted(unmatched_d):
            if detections[j, 4] >= self.high_score:
                track = Track(self.next_id, detections[j], time)
                track.confirmed = self.min_hits <= 1
                self.tracks.append(track)
                self.next_id += 1
        return [t for t in self.tracks if t.confirmed and t.last_seen == time]
