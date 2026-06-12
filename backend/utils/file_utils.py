import os
import uuid
from pathlib import Path
import shutil

TEMP_DIR = Path(__file__).parent.parent / "temp"
TEMP_DIR.mkdir(exist_ok=True)


def save_upload(file_bytes: bytes, suffix: str) -> Path:
    """Save uploaded bytes to a temp file and return its path."""
    filename = f"{uuid.uuid4().hex}{suffix}"
    path = TEMP_DIR / filename
    path.write_bytes(file_bytes)
    return path


def cleanup(path: Path):
    """Remove a temp file if it exists."""
    try:
        if path and path.exists():
            path.unlink()
    except Exception:
        pass


def cleanup_dir(dir_path: Path):
    """Remove a temp directory."""
    try:
        if dir_path and dir_path.exists():
            shutil.rmtree(dir_path)
    except Exception:
        pass
