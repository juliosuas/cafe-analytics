"""YOLOX-S official ONNX release, person class only.

Pre/postprocessing follows Megvii YOLOX (Apache-2.0); see NOTICE.
"""
import cv2
import numpy as np
import onnxruntime as ort


class Detector:
    def __init__(self, path, threshold=0.12, threads=4):
        options = ort.SessionOptions()
        options.intra_op_num_threads = threads
        self.session = ort.InferenceSession(str(path), options, providers=["CPUExecutionProvider"])
        inp = self.session.get_inputs()[0]
        if inp.shape != [1, 3, 640, 640]:
            raise ValueError("Se requiere el modelo oficial YOLOX-S ONNX de 640 x 640.")
        self.input_name = inp.name
        self.threshold = threshold
        grids, strides = [], []
        for stride in (8, 16, 32):
            y, x = np.mgrid[:640 // stride, :640 // stride]
            grids.append(np.stack([x, y], axis=-1).reshape(-1, 2))
            strides.append(np.full((x.size, 1), stride))
        self.grid = np.concatenate(grids)
        self.strides = np.concatenate(strides)

    def __call__(self, frame):
        h, w = frame.shape[:2]
        ratio = min(640 / h, 640 / w)
        # Official release uses BGR float32 in [0,255], top-left letterbox.
        canvas = np.full((640, 640, 3), 114, dtype=np.uint8)
        resized = cv2.resize(frame, (int(w * ratio), int(h * ratio)))
        canvas[:resized.shape[0], :resized.shape[1]] = resized
        tensor = np.ascontiguousarray(canvas.transpose(2, 0, 1)[None], dtype=np.float32)
        pred = self.session.run(None, {self.input_name: tensor})[0][0]
        scores = pred[:, 4] * pred[:, 5]  # COCO class 0 = person
        keep = (scores >= self.threshold) & (pred[:, 5:].argmax(axis=1) == 0)
        p, scores = pred[keep], scores[keep]
        if not len(p):
            return np.empty((0, 5), dtype=np.float32)
        centers = (p[:, :2] + self.grid[keep]) * self.strides[keep]
        sizes = np.exp(np.clip(p[:, 2:4], -10, 10)) * self.strides[keep]
        boxes = np.concatenate([centers - sizes / 2, centers + sizes / 2], axis=1) / ratio
        boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, w - 1)
        boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, h - 1)
        xywh = boxes.copy()
        xywh[:, 2:] -= xywh[:, :2]
        indices = cv2.dnn.NMSBoxes(xywh.tolist(), scores.tolist(), self.threshold, 0.45)
        indices = np.asarray(indices).reshape(-1)
        return np.column_stack([boxes[indices], scores[indices]]).astype(np.float32)
