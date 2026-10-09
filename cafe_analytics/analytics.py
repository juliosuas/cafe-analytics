import copy
import math
import cv2
import numpy as np


def validate_config(config):
    c = copy.deepcopy(config)
    if c.get("anchor", "bottom_center") not in ("bottom_center", "center"):
        raise ValueError("anchor debe ser bottom_center o center")
    if not isinstance(c.get("zones"), list) or not c["zones"]:
        raise ValueError("Define al menos una zona")
    c.setdefault("gates", [])
    for kind, points_key, minimum in (("zones", "polygon", 3), ("gates", "points", 2)):
        names = set()
        for item in c[kind]:
            name = item.get("name")
            if not isinstance(name, str) or not name.strip() or name in names:
                raise ValueError("Los nombres deben ser unicos y no vacios")
            names.add(name)
            points = item.get(points_key, [])
            if len(points) < minimum or (kind == "gates" and len(points) != 2):
                raise ValueError("Poligonos: minimo 3 puntos; lineas: exactamente 2")
            for p in points:
                if len(p) != 2 or any(not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in p):
                    raise ValueError("Usa coordenadas normalizadas finitas entre 0 y 1")
            if kind == "zones":
                poly = np.asarray(points, np.float32)
                if abs(cv2.contourArea(poly)) < 1e-6 or not cv2.isContourConvex(poly):
                    raise ValueError("Usa zonas convexas, sin cruces; divide las zonas complejas")
            else:
                if np.linalg.norm(np.array(points[1]) - points[0]) < 0.01:
                    raise ValueError("La linea de conteo es demasiado corta")
                if item.get("in_direction", "negative_to_positive") not in ("negative_to_positive", "positive_to_negative"):
                    raise ValueError("Direccion de entrada invalida")
                margin = item.get("hysteresis", 0.012)
                if not isinstance(margin, (int, float)) or not 0 < margin < 0.2:
                    raise ValueError("hysteresis debe estar entre 0 y 0.2")
    return c


def anchor(box, width, height, mode):
    x = (box[0] + box[2]) / 2
    y = box[3] if mode == "bottom_center" else (box[1] + box[3]) / 2
    return np.clip([x / width, y / height], 0, 1)


def cross2(a, b):
    return float(a[0] * b[1] - a[1] * b[0])


def crosses_segment(p, q, a, b):
    r, s = q - p, b - a
    denominator = cross2(r, s)
    if abs(denominator) < 1e-10:
        return False
    t, u = cross2(a - p, s) / denominator, cross2(a - p, r) / denominator
    return 0 <= t <= 1 and 0 <= u <= 1


class Analytics:
    def __init__(self, config, max_gap=0.5):
        self.config = validate_config(config)
        self.max_gap = max_gap
        self.polygons = {z["name"]: np.array(z["polygon"], np.float32) for z in config["zones"]}
        self.people = {}
        self.active = {}
        self.visits = []
        self.events = []
        self.gate_state = {}
        self.counts = {g["name"]: {"in": 0, "out": 0} for g in config.get("gates", [])}
        self.peak = {name: 0 for name in self.polygons}
        self.heat = np.zeros((90, 160), np.float64)

    def close_visit(self, key, reason):
        visit = self.active.pop(key)
        visit["end_reason"] = reason
        visit["censored"] = reason != "zone_exit"
        self.visits.append(visit)

    def update(self, observations, time):
        # observations = [(track_id, normalized_position), ...], measured detections only.
        occupancy = {name: 0 for name in self.polygons}
        seen = set()
        for tid, point in observations:
            point = np.asarray(point, dtype=float)
            seen.add(tid)
            previous = self.people.get(tid)
            dt = time - previous["last_seen_s"] if previous else 0
            continuous = previous is not None and 0 <= dt <= self.max_gap
            if previous is None:
                self.people[tid] = {"track_id": tid, "first_seen_s": time, "last_seen_s": time,
                                    "observed_seconds": 0.0, "samples": 0}
            person = self.people[tid]
            person["samples"] += 1
            if continuous:
                person["observed_seconds"] += dt
                x = min(int(point[0] * 160), 159)
                y = min(int(point[1] * 90), 89)
                self.heat[y, x] += dt
            person["last_seen_s"] = time
            for name, poly in self.polygons.items():
                key = (tid, name)
                inside = cv2.pointPolygonTest(poly, tuple(map(float, point)), False) >= 0
                if key in self.active and not continuous:
                    self.close_visit(key, "observation_gap")
                if inside:
                    occupancy[name] += 1
                    if key not in self.active:
                        self.active[key] = {"track_id": tid, "zone": name, "start_s": time,
                                            "end_s": time, "observed_seconds": 0.0}
                    else:
                        self.active[key]["observed_seconds"] += dt
                        self.active[key]["end_s"] = time
                elif key in self.active:
                    # Conservative: do not assign the unknown boundary interval.
                    self.close_visit(key, "zone_exit")
            for gate in self.config.get("gates", []):
                key = (tid, gate["name"])
                if not continuous:
                    self.gate_state.pop(key, None)
                a, b = np.array(gate["points"], dtype=float)
                distance = cross2(b - a, point - a) / np.linalg.norm(b - a)
                if abs(distance) < gate.get("hysteresis", 0.012):
                    continue
                side = 1 if distance > 0 else -1
                old = self.gate_state.get(key)
                if old and side != old[0] and crosses_segment(old[1], point, a, b):
                    incoming = side == 1
                    if gate.get("in_direction", "negative_to_positive") == "positive_to_negative":
                        incoming = not incoming
                    direction = "in" if incoming else "out"
                    self.counts[gate["name"]][direction] += 1
                    self.events.append({"time_s": time, "track_id": tid, "gate": gate["name"], "direction": direction})
                self.gate_state[key] = (side, point.copy())
        for key in list(self.active):
            if key[0] not in seen and time - self.people[key[0]]["last_seen_s"] > self.max_gap:
                self.close_visit(key, "track_lost")
        for key in list(self.gate_state):
            if time - self.people[key[0]]["last_seen_s"] > self.max_gap:
                del self.gate_state[key]
        for name, count in occupancy.items():
            self.peak[name] = max(self.peak[name], count)
        return occupancy

    def finish(self):
        for key in list(self.active):
            self.close_visit(key, "end_of_run")
        zones = []
        for name in self.polygons:
            visits = [v for v in self.visits if v["zone"] == name]
            seconds = sum(v["observed_seconds"] for v in visits)
            zones.append({"zone": name, "track_ids": len({v["track_id"] for v in visits}),
                          "visits": len(visits), "observed_person_seconds": seconds,
                          "mean_observed_visit_s": seconds / len(visits) if visits else 0,
                          "censored_visits": sum(v["censored"] for v in visits),
                          "peak_observed_occupancy": self.peak[name]})
        return zones
