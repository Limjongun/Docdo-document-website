"""
EAST Text Detector
------------------
Menggunakan model EAST (Efficient and Accurate Scene Text) via OpenCV DNN
untuk menghasilkan bounding box area teks di gambar.

Input  : BGR image (numpy array)
Output : list of (x, y, w, h) bounding boxes (koordinat original image)
"""

import cv2
import numpy as np
from typing import List, Tuple


class EASTDetector:
    OUTPUT_LAYERS = [
        "feature_fusion/Conv_7/Sigmoid",   # scores
        "feature_fusion/concat_3",          # geometry
    ]

    def __init__(
        self,
        model_path: str,
        conf_threshold: float = 0.5,
        nms_threshold: float = 0.4,
        input_size: Tuple[int, int] = (320, 320),
    ):
        print("[EAST] Loading model ...")
        self.net = cv2.dnn.readNet(model_path)
        self.conf_threshold = conf_threshold
        self.nms_threshold  = nms_threshold
        # EAST requires width & height to be multiples of 32
        self.inp_w = (input_size[0] // 32) * 32
        self.inp_h = (input_size[1] // 32) * 32
        print("[EAST] Model loaded.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def detect(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Return list of (x, y, w, h) bounding boxes in original coords."""
        orig_h, orig_w = image.shape[:2]

        # Pad image to a multiple of 32 without distortion
        pad_w = ((orig_w + 31) // 32) * 32
        pad_h = ((orig_h + 31) // 32) * 32
        padded = np.zeros((pad_h, pad_w, 3), dtype=np.uint8)
        padded[:orig_h, :orig_w] = image

        ratio_w = orig_w / pad_w
        ratio_h = orig_h / pad_h

        blob = cv2.dnn.blobFromImage(
            padded, 1.0, (pad_w, pad_h),
            (123.68, 116.78, 103.94), swapRB=True, crop=False,
        )
        self.net.setInput(blob)
        scores, geometry = self.net.forward(self.OUTPUT_LAYERS)

        boxes, confidences = self._decode_predictions(scores, geometry)
        if not boxes:
            return []

        indices = cv2.dnn.NMSBoxesRotated(
            boxes, confidences,
            self.conf_threshold, self.nms_threshold,
        )
        if isinstance(indices, tuple) or len(indices) == 0:
            return []

        results: List[Tuple[int, int, int, int]] = []
        scale_x = orig_w / (scores.shape[3] * 4)
        scale_y = orig_h / (scores.shape[2] * 4)

        for i in indices.flatten():
            box   = boxes[i]
            cx, cy = box[0][0] * scale_x, box[0][1] * scale_y
            w,  h  = box[1][0] * scale_x, box[1][1] * scale_y
            x = int(cx - w / 2)
            y = int(cy - h / 2)
            x = max(0, x)
            y = max(0, y)
            w = min(int(w), orig_w - x)
            h = min(int(h), orig_h - y)
            if w > 0 and h > 0:
                results.append((x, y, w, h))

        # Sort top-to-bottom, left-to-right
        results.sort(key=lambda b: (b[1] // 20, b[0]))
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _decode_predictions(
        self, scores: np.ndarray, geometry: np.ndarray
    ) -> Tuple[list, list]:
        num_rows, num_cols = scores.shape[2:4]
        boxes: list       = []
        confidences: list = []

        for y in range(num_rows):
            score_data = scores[0, 0, y]
            d0 = geometry[0, 0, y]  # top
            d1 = geometry[0, 1, y]  # right
            d2 = geometry[0, 2, y]  # bottom
            d3 = geometry[0, 3, y]  # left
            angles = geometry[0, 4, y]

            for x in range(num_cols):
                score = float(score_data[x])
                if score < self.conf_threshold:
                    continue

                offset_x = x * 4.0
                offset_y = y * 4.0
                angle    = float(angles[x])
                cos_a    = np.cos(angle)
                sin_a    = np.sin(angle)
                h        = float(d0[x]) + float(d2[x])
                w        = float(d1[x]) + float(d3[x])
                cx = offset_x + cos_a * float(d1[x]) + sin_a * float(d2[x])
                cy = offset_y - sin_a * float(d1[x]) + cos_a * float(d2[x])

                boxes.append(((cx, cy), (w, h), -angle * 180.0 / np.pi))
                confidences.append(score)

        return boxes, confidences
