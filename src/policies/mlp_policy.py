import random
import torch
from torch import nn


class MLPPolicy:
    @classmethod
    def load(cls, mlp, file, *args, **kwargs):
        mlp.load_state_dict(torch.load(file))
        return cls(mlp, *args, **kwargs)

    def __init__(self, mlp, lr=0.001):
        self.mlp = mlp
        self.criterion = nn.MSELoss()
        self.optim = torch.optim.Adam(mlp.parameters(), lr=lr)

    @torch.no_grad()
    def __call__(self, state: tuple[int], action_space: set[int]):
        state_t = torch.tensor(state).float()
        actions_t = torch.tensor(list(action_space)).long()
        return actions_t[self.mlp(state_t)[actions_t].argmax()].item()

    @torch.no_grad()
    def get_q(self, state: tuple[int], action: int):
        state_t = torch.tensor(state).float()
        return self.mlp(state_t)[action].item()

    @torch.no_grad()
    def batch_get_q(self, states: list[tuple[int]], actions: list[int]):
        states_t = torch.tensor(states).float()
        actions_t = torch.tensor(actions).long()
        return self.mlp(states_t)[torch.arange(len(actions_t)), actions_t].tolist()

    def update_q(self, state: tuple[int], action: int, q: float):
        pass

    def batch_update_q(self, states: list[tuple[int]], actions: list[int], qs: list[float]):
        states_t = torch.tensor(states).float()
        actions_t = torch.tensor(actions)
        qs_t = torch.tensor(qs).float()
        self.optim.zero_grad()
        pred = self.mlp(states_t)[torch.arange(len(actions_t)), actions_t]
        loss = self.criterion(pred, qs_t)
        loss.backward()
        self.optim.step()
        return loss.item()

    def save(self, file):
        torch.save(self.mlp.state_dict(), file)
