import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path
import io
import base64


def sharpen_image(image_bytes: bytes) -> bytes:
    """Sharpen, denoise, and enhance contrast of a document image."""
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Denoise
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    # Sharpen kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    # Convert to PIL for contrast enhancement
    pil_img = Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
    pil_img = ImageEnhance.Contrast(pil_img).enhance(1.3)

    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return buf.getvalue()


def extract_signature(image_bytes: bytes) -> bytes:
    """Isolate signature: convert to grayscale, threshold, invert for white bg."""
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Adaptive threshold to isolate dark strokes
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 4
    )

    # Slight dilation to thicken strokes
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # White background output
    result = np.full_like(img, 255)
    result[dilated == 255] = [0, 0, 0]

    pil_img = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return buf.getvalue()


def image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode()
