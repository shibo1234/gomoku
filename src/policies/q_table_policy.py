import random
import pickle as pkl


class QTablePolicy:
    @classmethod
    def load(cls, file, *args, **kwargs):
        return cls(q_table=pkl.load(open(file, 'rb')), *args, **kwargs)

    def __init__(self, q_table, lr=0.1):
        self.q_table = q_table
        self.lr = lr

    def __call__(self, state, actions):
        actions = {action: self.q_table[state, action] for action in actions}
        return sorted(actions, key=lambda m: -actions[m])[0]

    def get_q(self, state, action):
        return self.q_table[state, action]

    def batch_get_q(self, states, actions):
        return [self.get_q(state, action) for state, action in zip(states, actions)]

    def update_q(self, state, action, q):
        self.q_table[state, action] = (1 - self.lr) * self.get_q(state, action) + self.lr * q

    def batch_update_q(self, states, actions, qs):
        for state, action, q in zip(states, actions, qs):
            self.update_q(state, action, q)

    def save(self, file):
        pkl.dump(self.q_table, open(file, 'wb'))
