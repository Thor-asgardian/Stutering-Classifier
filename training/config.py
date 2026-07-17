from pathlib import Path
import torch

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "dataset"

TRAIN_DIR = DATASET_DIR / "train"
VAL_DIR = DATASET_DIR / "val"
TEST_DIR = DATASET_DIR / "test"

CHECKPOINT_DIR = Path(__file__).resolve().parent / "checkpoints"
CHECKPOINT_DIR.mkdir(exist_ok=True)

MODEL_PATH = CHECKPOINT_DIR / "best_model.pth"

IMAGE_SIZE = 224
BATCH_SIZE = 16
NUM_EPOCHS = 20
LEARNING_RATE = 1e-4

CLASS_NAMES = [
    "ASD",
    "Control",
]

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
) 