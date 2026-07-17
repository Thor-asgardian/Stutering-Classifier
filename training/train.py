from pathlib import Path

import torch
import torch.nn as nn
from torch.optim import AdamW
from tqdm import tqdm
from transformers import ViTForImageClassification

from config import (
    DEVICE,
    MODEL_PATH,
    NUM_EPOCHS,
    LEARNING_RATE,
)
from dataset import (
    train_loader,
    val_loader,
)


NUM_CLASSES = 2


def create_model():

    model = ViTForImageClassification.from_pretrained(
        "google/vit-base-patch16-224",
        num_labels=NUM_CLASSES,
        ignore_mismatched_sizes=True,
    )

    return model.to(DEVICE)


def evaluate(model, loader, criterion):

    model.eval()

    total_loss = 0.0
    correct = 0
    total = 0

    with torch.inference_mode():

        for images, labels in loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(pixel_values=images)

            loss = criterion(outputs.logits, labels)

            total_loss += loss.item()

            predictions = outputs.logits.argmax(dim=1)

            correct += (predictions == labels).sum().item()

            total += labels.size(0)

        accuracy = 100 * correct / total

        return total_loss / len(loader), accuracy


def train():

    model = create_model()

    optimizer = AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
    )

    criterion = nn.CrossEntropyLoss()

    best_accuracy = 0.0

    print("\nTraining Started...\n")

    for epoch in range(NUM_EPOCHS):

        model.train()

        running_loss = 0.0

        progress = tqdm(train_loader)

        for images, labels in progress:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            optimizer.zero_grad()

            outputs = model(pixel_values=images)

            loss = criterion(
                outputs.logits,
                labels,
            )

            loss.backward()

            optimizer.step()

            running_loss += loss.item()

            progress.set_description(
                f"Epoch {epoch+1}/{NUM_EPOCHS}"
            )

            progress.set_postfix(
                loss=f"{loss.item():.4f}"
            )

        val_loss, val_accuracy = evaluate(
            model,
            val_loader,
            criterion,
        )

        print(
                f"\nValidation Loss : {val_loss:.4f}"
            )

        print(
                f"Validation Accuracy : {val_accuracy:.2f}%\n"
            )

        if val_accuracy > best_accuracy:

            best_accuracy = val_accuracy

            torch.save(
                model.state_dict(),
                MODEL_PATH,
            )

            print(
                    f"Best model saved to\n{MODEL_PATH}\n"
                )

        print("\nTraining Complete\n")

        print(
                    f"Best Validation Accuracy : {best_accuracy:.2f}%"
                )


if __name__ == "__main__":
    train()