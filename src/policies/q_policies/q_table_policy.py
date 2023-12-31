from .base_q_policy import BaseQPolicySingle

import pickle as pkl


class QTablePolicy(BaseQPolicySingle):
    @classmethod
    def load(cls, file, *args, **kwargs):
        return cls(q_table=pkl.load(open(file, 'rb')), *args, **kwargs)

    def save(self, file):
        pkl.dump(self.q_table, open(file, 'wb'))

    def __init__(self, q_table, lr=0.1):
        self.q_table = q_table
        self.lr = lr

    def get_all_Qs(self, state: tuple[int], action_space: set[int]) -> dict[int, float]:
        return {action: self.q_table[state, action] for action in action_space}

    def update_Q(self, state: tuple[int], action: int, Q: float) -> None:
        self.q_table[state, action] = (1 - self.lr) * self.get_Q(state, action) + self.lr * Q

