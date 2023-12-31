from .base_q_policy import BaseQPolicyBatch

import torch
from torch import nn


class MLPPolicy(BaseQPolicyBatch):
    @classmethod
    def load(cls, mlp, file, *args, **kwargs):
        mlp.load_state_dict(torch.load(file))
        return cls(mlp, *args, **kwargs)

    def save(self, file):
        torch.save(self.mlp.state_dict(), file)

    def __init__(self, mlp, lr=0.001):
        self.mlp = mlp
        self.criterion = nn.MSELoss()
        self.optim = torch.optim.Adam(mlp.parameters(), lr=lr)

    @torch.no_grad()
    def __call__(self, state: tuple[int], action_space: set[int]) -> int:
        state_t = torch.tensor(state).float()
        actions_t = torch.tensor(list(action_space)).long()
        return actions_t[self.mlp(state_t)[actions_t].argmax()].item()

    @torch.no_grad()
    def get_Q(self, state: tuple[int], action: int) -> float:
        state_t = torch.tensor(state).float()
        return self.mlp(state_t)[action].item()

    @torch.no_grad()
    def batch_get_Q(self, states: list[tuple[int]], actions: list[int]) -> list[float]:
        states_t = torch.tensor(states).float()
        actions_t = torch.tensor(actions).long()
        return self.mlp(states_t)[torch.arange(len(actions_t)), actions_t].tolist()

    @torch.no_grad()
    def get_all_Qs(self, state: tuple[int], action_space: set[int]) -> dict[int, float]:
        state_t = torch.tensor(state).float()
        actions_t = torch.tensor(list(action_space)).long()
        return dict(zip(action_space, self.mlp(state_t)[actions_t].tolist()))

    def batch_get_all_Qs(self, states: list[tuple[int]], action_spaces: list[set[int]]) -> list[dict[int, float]]:
        pass

    def update_Q(self, state: tuple[int], action: int, Q: float) -> None:
        raise NotImplementedError

    def batch_update_Q(self, states: list[tuple[int]], actions: list[int], Qs: list[float]) -> None:
        states_t = torch.tensor(states).float()
        actions_t = torch.tensor(actions)
        qs_t = torch.tensor(Qs).float()
        self.optim.zero_grad()
        pred = self.mlp(states_t)[torch.arange(len(actions_t)), actions_t]
        loss = self.criterion(pred, qs_t)
        loss.backward()
        self.optim.step()
        return loss.item()
