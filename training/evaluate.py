from __future__ import annotations

import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from transformers import ViTForImageClassification

from config import (
    CLASS_NAMES,
    DEVICE,
    MODEL_PATH,
)
from dataset import test_loader


NUM_CLASSES = len(CLASS_NAMES)


def load_model():

    model = ViTForImageClassification.from_pretrained(
        "google/vit-base-patch16-224",
        num_labels=NUM_CLASSES,
        ignore_mismatched_sizes=True,
    )

    model.load_state_dict(
        torch.load(
            MODEL_PATH,
            map_location=DEVICE,
        )
    )

    model.to(DEVICE)
    model.eval()

    return model


def evaluate():

    model = load_model()

    predictions = []
    labels_list = []

    with torch.inference_mode():

        for images, labels in test_loader:

            images = images.to(DEVICE)

            outputs = model(pixel_values=images)

            predicted = outputs.logits.argmax(dim=1)

            predictions.extend(
                predicted.cpu().numpy()
            )

            labels_list.extend(
                labels.numpy()
            )

        print("\nAccuracy")

        print(
                accuracy_score(
                    labels_list,
                    predictions,
                )
            )

        print("\nClassification Report")

        print(
                classification_report(
                    labels_list,
                    predictions,
                    target_names=CLASS_NAMES,
                )
            )

        print("\nConfusion Matrix")

        print(
                confusion_matrix(
                    labels_list,
                    predictions,
                )
            )


if __name__ == "__main__":
    evaluate()