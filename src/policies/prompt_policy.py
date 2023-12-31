from .base_policy import BasePolicy

from typing import Callable


class PromptPolicy(BasePolicy):

    def __init__(self, state_formatter: Callable[[tuple[int]], str] = str):
        self.formatter = state_formatter

    def __call__(self, state: tuple[int], player: int, actions: set[int]) -> int:
        # print(self.formatter(state), flush=True)
        return int(input(f"{self.formatter(state)}\nEnter action for {player}: "))
