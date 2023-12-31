from .base_policy import BasePolicy
from .stochastic_multipolicy import StochasticMultiPolicy
from .random_policy import RandomPolicy


class EpsilonGreedyPolicy(StochasticMultiPolicy):
    def __init__(self, policy: BasePolicy, epsilon: float = 0.1):
        super().__init__([policy, RandomPolicy()], [1 - epsilon, epsilon])

