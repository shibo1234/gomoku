import torch
from torch import nn


class MLPLayer(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(in_features=width, out_features=width),
            nn.BatchNorm1d(width),
            nn.LeakyReLU()
        )

    def forward(self, x):
        return x + self.model(x)
