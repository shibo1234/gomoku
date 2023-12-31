from .base_q_policy import BaseQPolicySingle

from collections import defaultdict
import pickle as pkl
import numpy as np


class QTablePolicy(BaseQPolicySingle):
    @classmethod
    def load(cls, name, ext='pkl', *args, **kwargs):
        return cls(q_table=pkl.load(open(f'{name}.{ext}', 'rb')), *args, **kwargs)

    def save(self, name):
        pkl.dump(self.q_table, open(f'{name}.pkl', 'wb'))

    def __init__(self, q_table=None, lr=0.1):
        self.q_table = q_table or defaultdict(float)
        self.lr = lr

    def get_all_Qs(self, state: tuple[int], player: int, action_space: set[int]) -> dict[int, float]:
        return {action: self.q_table[state, player, action] for action in action_space}

    def update_Q(self, state: tuple[int], player: int, action: int, Q: float) -> float:
        act_q, exp_q = self.get_Q(state, player, action), Q
        self.q_table[state, player, action] = (1 - self.lr) * act_q + self.lr * exp_q
        return np.abs(act_q - exp_q)

