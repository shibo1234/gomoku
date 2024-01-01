from .base_policy import BasePolicy

import time
from typing import Callable


class PromptPolicy(BasePolicy):

    def __init__(self, player_formatter: Callable[[int], str] = str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatter = player_formatter

    def __call__(self, state: tuple[int, ...], player: int, actions: set[int]) -> int:
        time.sleep(0.1)  # to prevent the prompt from being printed before the game state
        return int(input(f"Enter action for {self.formatter(player)}: "))
