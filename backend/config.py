from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

# Windows DLL Fix (PyTorch)

def configure_windows_dlls() -> None:
    """Add common virtual environment DLL directories (Windows only)."""

    if os.name != "nt":
        return

    try:
        venv = Path(sys.executable).resolve().parent.parent

        dll_dirs = [
            venv,
            venv / "Scripts",
            venv / "Library" / "bin",
            venv / "Lib" / "site-packages" / "numpy" / ".libs",
            venv / "Lib" / "site-packages" / "scipy" / ".libs",
            venv / "Lib" / "site-packages" / "sklearn" / ".libs",
        ]

        for directory in dll_dirs:
            if directory.exists():
                try:
                    os.add_dll_directory(str(directory))
                except OSError:
                    pass

    except Exception:
        pass


configure_windows_dlls()

# Torch
try:
    import torch
except OSError as e:
    raise RuntimeError(
    "\nPyTorch failed to load.\n"
    "Install the Microsoft Visual C++ 2015–2022 Redistributable (x64), "
    "then restart VS Code."
) from e

# Paths

BACKEND_DIR = Path(__file__).resolve().parent

MODEL_DIR = BACKEND_DIR / "models"

MODEL_PATH = MODEL_DIR / "best_model.pt"

# Audio

SAMPLE_RATE = 16000

WINDOW_SEC = 5.0

STRIDE_SEC = 2.5

# Thresholds

MIN_CONFIDENCE = 0.50

MIN_STUTTER_PERCENT = 10.0

# Labels

CLASS_NAMES = [
    "Fluent",
    "Repetition",
    "Prolongation",
    "Block",
]

# Device

def get_device() -> str:
    device = os.getenv("DEVICE", "").strip().lower()

    if device in {"cpu", "cuda"}:
        return device

    return "cuda" if torch.cuda.is_available() else "cpu"


DEVICE = get_device()

# Logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

LOGGER = logging.getLogger("stuttering_backend")

LOGGER.info("Backend initialized")
LOGGER.info("Device: %s", DEVICE)
LOGGER.info("Sample Rate: %d", SAMPLE_RATE)

if MODEL_PATH.exists():
    LOGGER.info("Model: %s", MODEL_PATH)
else:
    LOGGER.warning("Model checkpoint not found.")