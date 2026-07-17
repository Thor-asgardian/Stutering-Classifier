from __future__ import annotations

from pathlib import Path
import torch

# Project Paths

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = BASE_DIR / "training" / "checkpoints" / "best_model.pth"

print("MODEL_PATH =", MODEL_PATH)
print("Exists =", MODEL_PATH.exists())
# Dataset

CLASS_NAMES = [
    "ASD",
    "Control",
]

NUM_CLASSES = len(CLASS_NAMES)

# Vision Transformer

IMAGE_SIZE = 224

MEAN = [0.485, 0.456, 0.406]

STD = [0.229, 0.224, 0.225]

# Device

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# API

SUPPORTED_IMAGE_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
}

MIN_CONFIDENCE = 0.50