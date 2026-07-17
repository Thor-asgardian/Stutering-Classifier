from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

# ---------------------------------------------------------------------
# Make backend importable
# ---------------------------------------------------------------------

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

    # ---------------------------------------------------------------------
    # Project imports
    # ---------------------------------------------------------------------

from app.config import (
    DEVICE,
    MODEL_PATH,
    SUPPORTED_IMAGE_FORMATS,
)

from inference.pipeline import InferencePipeline
from models.final_model import load_model

# ---------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------

app = FastAPI(
    title="ASD Screening API",
    version="1.0.0",
    description="Vision Transformer-based facial image screening system.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------
# Load AI Model
# ---------------------------------------------------------------------

pipeline = None

try:
    model = load_model(MODEL_PATH, DEVICE)
    pipeline = InferencePipeline(model)
    print("✓ Vision Transformer loaded successfully.")

except FileNotFoundError:
    print("WARNING: best_model.pth not found.")

except Exception as e:
    print(f"ERROR loading model: {e}")

    # ---------------------------------------------------------------------
    # React Frontend
    # ---------------------------------------------------------------------

FRONTEND_DIST = BACKEND_DIR / "frontend_dist"

if FRONTEND_DIST.exists():

    assets_dir = FRONTEND_DIST / "assets"

    if assets_dir.exists():
        app.mount(
            "/assets",
            StaticFiles(directory=assets_dir),
            name="assets",
        )

    @app.get("/", include_in_schema=False)
    async def frontend():
        return FileResponse(FRONTEND_DIST / "index.html")

else:

    @app.get("/")
    def root():
        return {
            "application": "ASD Screening API",
            "status": "running",
            "model_loaded": pipeline is not None,
        }

# ---------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "device": str(DEVICE),
        "model_loaded": pipeline is not None,
    }

# ---------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------

@app.post("/predict")
async def predict(image: UploadFile = File(...)):

    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Model has not been trained yet.",
        )

    if not image.filename:
        raise HTTPException(
            status_code=400,
            detail="No image uploaded.",
        )

    extension = Path(image.filename).suffix.lower()

    if extension not in SUPPORTED_IMAGE_FORMATS:
        raise HTTPException(
            status_code=400,
            detail="Supported formats: jpg, jpeg, png.",
        )

    try:
        img = Image.open(image.file).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image.",
        )

    result = pipeline.predict(img)

    return result.model_dump()