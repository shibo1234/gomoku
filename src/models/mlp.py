from .mlp_layer import MLPLayer

import torch
from torch import nn


class MLP(nn.Module):
    def __init__(self, hidden_layers, hidden_width, grid_size=3):
        super().__init__()
        self.n_actions = grid_size ** 2

        self.model = nn.Sequential(
            nn.Linear(in_features=self.n_actions,
                      out_features=hidden_width),
            nn.BatchNorm1d(hidden_width),
            nn.LeakyReLU(),
            *[MLPLayer(hidden_width) for _ in range(hidden_layers-1)],
            nn.Linear(in_features=hidden_width,
                      out_features=2 * self.n_actions),
            nn.Tanh()
        )

    def forward(self, x):
        return self.model(x).view(
            -1,  # batch_size
            2,  # num_players
            self.n_actions  # num_actions
        )
