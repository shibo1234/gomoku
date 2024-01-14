import torch
from torch import nn


class MLP(nn.Module):
    def __init__(self, grid_size=3):
        super().__init__()
        self.n_actions = grid_size ** 2
        self.model = nn.Sequential(
            nn.Linear(in_features=self.n_actions, out_features=32),
            nn.LeakyReLU(),
            nn.Linear(in_features=32, out_features=64),
            nn.LeakyReLU(),
            nn.Linear(in_features=64, out_features=32),
            nn.LeakyReLU(),
            nn.Linear(in_features=32, out_features=2 * self.n_actions),
            nn.Tanh()
        )

    def forward(self, x):
        return self.model(x).view(
            -1,  # batch_size
            2,  # num_players
            self.n_actions  # num_actions
        )
