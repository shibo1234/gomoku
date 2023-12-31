from .base_policy import BasePolicy

import random


class RandomPolicy(BasePolicy):

    def __call__(self, state: tuple[int], player: int, actions: set[int]) -> int:
        return random.choice(list(actions))
