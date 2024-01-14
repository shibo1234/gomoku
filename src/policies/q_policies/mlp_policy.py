from .base_q_policy import BaseQPolicyBatch

import torch
from torch import nn


class MLPPolicy(BaseQPolicyBatch):

    @classmethod
    def load(cls, ckpt_name, ext='pt', *args, **kwargs):
        policy = cls(*args, **kwargs)
        policy.mlp.load_state_dict(torch.load(f'{ckpt_name}.{ext}'))
        return policy

    def save(self, ckpt_name, ext='pt'):
        torch.save(self.mlp.state_dict(), f'{ckpt_name}.{ext}')

    def __init__(self, mlp, lr=0.001, device='cpu', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mlp = mlp.to(device)
        self.criterion = nn.MSELoss()
        self.optim = torch.optim.Adam(mlp.parameters(), lr=lr)
        self.device = device

    @torch.no_grad()
    def batch_get_all_Qs(self,
                         states: list[tuple[int, ...]],
                         players: list[int],
                         action_spaces: list[set[int]]) -> list[dict[int, float]]:
        states_t = torch.tensor(states).float().to(self.device)
        players_t = (torch.tensor(players) > 0).long().to(self.device)
        raw_qs = self.mlp(states_t)
        qs = raw_qs[torch.arange(raw_qs.shape[0]), players_t, :]
        return [
            {action: qs[i, action] for action in action_space}
            for i, action_space in enumerate(action_spaces)
        ]

    def batch_update_Q(self,
                       states: list[tuple[int, ...]],
                       players: list[int],
                       actions: list[int],
                       Qs: list[float]) -> float:
        states_t = torch.tensor(states).float().to(self.device)
        actions_t = torch.tensor(actions).long().to(self.device)
        players_t = (torch.tensor(players) > 0).long().to(self.device)
        qs_t = torch.tensor(Qs).float().to(self.device)
        self.optim.zero_grad()
        pred = self.mlp(states_t)[
            torch.arange(states_t.shape[0]),
            players_t,
            actions_t
        ]
        loss = self.criterion(pred, qs_t)
        loss.backward()
        self.optim.step()
        return loss.item()
