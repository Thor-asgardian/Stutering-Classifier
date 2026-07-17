from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

from config import *
from transforms import train_transform, test_transform

train_dataset = ImageFolder(
    TRAIN_DIR,
    transform=train_transform,
)

val_dataset = ImageFolder(
    VAL_DIR,
    transform=test_transform,
)

test_dataset = ImageFolder(
    TEST_DIR,
    transform=test_transform,
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
)