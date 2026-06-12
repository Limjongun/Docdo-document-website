"""
CRNN Text Recognizer
--------------------
Menggunakan model CRNN (Convolutional Recurrent NN) via OpenCV DNN (ONNX)
dengan decoder CTC untuk mengubah tiap region teks menjadi string karakter.

Input  : crop gambar teks (numpy array BGR)
Output : string hasil rekognisi
"""

import cv2
import numpy as np
from .model_manager import CRNN_CHARSET


class CRNNRecognizer:
    # CRNN ONNX input: grayscale 32xW
    INPUT_H = 32

    def __init__(self, model_path: str):
        print("[CRNN] Loading model ...")
        self.net     = cv2.dnn.readNetFromONNX(model_path)
        self.charset = CRNN_CHARSET
        print("[CRNN] Model loaded.")

    # ------------------------------------------------------------------
    def recognize(self, crop: np.ndarray) -> str:
        """Recognize text in a single cropped BGR region."""
        if crop is None or crop.size == 0:
            return ""

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        if h == 0 or w == 0:
            return ""

        # Resize strictly to 100x32 (width=100, height=32) as required by OpenCV Zoo CRNN model
        gray  = cv2.resize(gray, (100, 32))

        # Normalize to [-1, 1]
        blob = (gray.astype(np.float32) - 127.5) / 127.5
        blob = blob[np.newaxis, np.newaxis, :, :]   # 1×1×32×100

        self.net.setInput(blob)
        output = self.net.forward()                 # shape: (T, 1, num_classes)
        text   = self._ctc_decode(output)
        return text

    # ------------------------------------------------------------------
    def _ctc_decode(self, output: np.ndarray) -> str:
        """Greedy CTC decoder."""
        T, _, C = output.shape
        indices  = np.argmax(output[:, 0, :], axis=1)  # (T,)
        chars    = []
        prev     = -1
        blank    = C - 1  # blank token is last class

        for idx in indices:
            if idx != blank and idx != prev:
                if idx < len(self.charset):
                    chars.append(self.charset[idx])
            prev = idx

        return "".join(chars)
