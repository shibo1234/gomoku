from .base_policy import BasePolicy

import random


class StochasticMultiPolicy(BasePolicy):
    def __init__(self, policies, probs=None):
        self.policies = policies
        self.probs = probs or [1/len(policies) for _ in policies]

    def __call__(self, state: list[int], actions: set[int]) -> int:
        return random.choices(self.policies, weights=self.probs)[0](state, actions)
