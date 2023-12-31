from .base_policy import BasePolicy

import time
from typing import Callable


class PromptPolicy(BasePolicy):

    def __init__(self, player_formatter: Callable[[int], str] = str):
        self.formatter = player_formatter

    def __call__(self, state: tuple[int], player: int, actions: set[int]) -> int:
        time.sleep(0.1)
        return int(input(f"Enter action for {self.formatter(player)}: "))
