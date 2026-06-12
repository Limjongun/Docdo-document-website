"""
OCR Service
-----------
Gateway antara router dan pipeline EAST + CRNN.
"""

from backend.ocr.pipeline import run_pipeline


def extract_text_from_image(image_bytes: bytes, lang: str = "ind+eng") -> str:
    """
    Jalankan pipeline EAST (deteksi) + CRNN (rekognisi).
    Parameter `lang` dipertahankan untuk kompatibilitas API,
    namun model saat ini menggunakan charset latin universal.
    """
    return run_pipeline(image_bytes)
