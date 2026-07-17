from __future__ import annotations

import os
import random

import numpy as np
import torch


def set_seed(seed: int = 42):

    random.seed(seed)

    np.random.seed(seed)

    torch.manual_seed(seed)

    torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True

    torch.backends.cudnn.benchmark = False


def count_parameters(model):

    return sum(
p.numel()
for p in model.parameters()
if p.requires_grad
)


def create_directory(path):

    os.makedirs(
        path,
        exist_ok=True,
    )