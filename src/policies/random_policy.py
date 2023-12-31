from .base_policy import BasePolicy

import random


class RandomPolicy(BasePolicy):
    def __init__(self):
        pass

    def __call__(self, state: list[int], actions: set[int]) -> int:
        return random.choice(list(actions))
