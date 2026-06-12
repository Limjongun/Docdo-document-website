"""
Model Manager: Auto-download EAST dan CRNN models on first use.
"""

import os
import requests
from pathlib import Path

MODELS_DIR = Path(__file__).parent / "weights"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

EAST_URLS = [
    "https://raw.githubusercontent.com/oyyd/frozen_east_text_detection.pb/master/frozen_east_text_detection.pb",
    "https://raw.githubusercontent.com/ZER-0-NE/EAST-Detector-for-text-in-Natural-Scene-Images/master/frozen_east_text_detection.pb",
]

CRNN_URLS = [
    "https://github.com/opencv/opencv_zoo/raw/main/models/text_recognition_crnn/text_recognition_CRNN_EN_2021sep.onnx",
]

EAST_PATH = MODELS_DIR / "east.pb"
CRNN_PATH = MODELS_DIR / "crnn.onnx"

# Charset for text_recognition_CRNN_EN_2021sep.onnx (90 chars)
CRNN_CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]_`~ "


def _download_with_fallback(urls: list, dest: Path, name: str) -> Path:
    if dest.exists() and dest.stat().st_size > 1000:
        return dest

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    last_err = None
    for url in urls:
        print(f"[Model Manager] Mencoba download {name} dari:\n  {url}")
        try:
            with requests.get(url, headers=headers, stream=True, allow_redirects=True, timeout=120) as r:
                r.raise_for_status()
                with open(dest, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            size_kb = dest.stat().st_size // 1024
            if size_kb < 1:
                print(f"[Model Manager] Response terlalu kecil ({size_kb} KB), skip.")
                continue
                
            print(f"[Model Manager] {name} berhasil disimpan ({size_kb} KB)")
            return dest
        except Exception as e:
            print(f"[Model Manager] Gagal: {e}")
            last_err = e
            if dest.exists():
                dest.unlink()

    raise RuntimeError(
        f"Gagal mengunduh {name}.\n"
        "Silakan download manual dan taruh di:\n"
        f"  {dest}\n"
        f"Error terakhir: {last_err}"
    )


def get_east_path() -> str:
    _download_with_fallback(EAST_URLS, EAST_PATH, "EAST model")
    return str(EAST_PATH)


def get_crnn_path() -> str:
    _download_with_fallback(CRNN_URLS, CRNN_PATH, "CRNN model")
    return str(CRNN_PATH)
