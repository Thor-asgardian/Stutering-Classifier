from __future__ import annotations

from pathlib import Path

import torch
import torch.nn as nn
from transformers import ViTForImageClassification

from app.config import NUM_CLASSES


class ASDViTModel(nn.Module):
    """
    Vision Transformer for ASD facial image classification.
    """

    def __init__(self):
        super().__init__()

        self.model = ViTForImageClassification.from_pretrained(
            "google/vit-base-patch16-224",
            num_labels=NUM_CLASSES,
            ignore_mismatched_sizes=True,
        )

    def forward(self, x):
        return self.model(pixel_values=x).logits


def load_model(model_path, device):
    model = ASDViTModel()

    checkpoint = torch.load(model_path, map_location=device)

    if isinstance(checkpoint, dict):
        if "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
        elif "state_dict" in checkpoint:
            state_dict = checkpoint["state_dict"]
        else:
            state_dict = checkpoint
    else:
        state_dict = checkpoint

    # Convert old checkpoint keys (vit.*) -> current model keys (model.vit.*)
    new_state_dict = {}

    for key, value in state_dict.items():
        if key.startswith("model."):
            new_state_dict[key] = value
        else:
            new_state_dict["model." + key] = value

    model.load_state_dict(new_state_dict, strict=True)

    model.to(device)
    model.eval()

    return model