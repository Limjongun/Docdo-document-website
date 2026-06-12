"""
EAST + CRNN Pipeline
--------------------
1. EAST mendeteksi bounding box setiap region teks di gambar.
2. Setiap region di-crop lalu dikenali oleh CRNN.
3. Hasil digabung menjadi teks akhir yang terurut (atas→bawah, kiri→kanan).
"""

import cv2
import numpy as np
from typing import List, Tuple

from .model_manager import get_east_path, get_crnn_path
from .east_detector  import EASTDetector
from .crnn_recognizer import CRNNRecognizer

# Singleton instances (lazy-load)
_east: EASTDetector  | None = None
_crnn: CRNNRecognizer | None = None


def _get_east() -> EASTDetector:
    global _east
    if _east is None:
        _east = EASTDetector(get_east_path())
    return _east


def _get_crnn() -> CRNNRecognizer:
    global _crnn
    if _crnn is None:
        _crnn = CRNNRecognizer(get_crnn_path())
    return _crnn


# ------------------------------------------------------------------
def preprocess(image_bytes: bytes) -> np.ndarray:
    """Decode image bytes → BGR numpy array."""
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Tidak dapat mendekode gambar.")
    return img


def run_pipeline(image_bytes: bytes) -> str:
    """
    Jalankan pipeline EAST → crop → CRNN pada gambar.
    Kembalikan teks yang dikenali.
    """
    img   = preprocess(image_bytes)
    east  = _get_east()
    crnn  = _get_crnn()

    boxes = east.detect(img)

    if not boxes:
        # Fallback: coba kenali seluruh gambar jika tidak ada kotak terdeteksi
        return crnn.recognize(img)

    lines: List[Tuple[int, str]] = []
    for (x, y, w, h) in boxes:
        # Sedikit padding supaya karakter di tepi tidak terpotong
        pad = 4
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img.shape[1], x + w + pad)
        y2 = min(img.shape[0], y + h + pad)
        crop = img[y1:y2, x1:x2]
        text = crnn.recognize(crop)
        if text.strip():
            lines.append((y, text.strip()))

    # Gabung teks dalam urutan atas→bawah
    lines.sort(key=lambda t: t[0])
    return "\n".join(t for _, t in lines)
