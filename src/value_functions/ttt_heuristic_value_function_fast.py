from .base_value_function import BaseValueFunctionSingle

import numpy as np
import torch


class TTTHeuristicValueFunctionFast(BaseValueFunctionSingle):
    def __init__(self, grid_size: int = 3, player_1: int = 1, player_2: int = -1, empty: int = 0):
        super().__init__()
        self.grid_size = grid_size
        self.index_list = list(self._gen_indices())
        self.player_1 = player_1
        self.player_2 = player_2
        self.empty = empty

    def _gen_indices(self):
        s = self.grid_size
        grid = list(range(s*s))
        for i in range(0, s*s, s):
            yield grid[i:i+s]
        for i in range(s):
            yield grid[i::s]
        yield grid[::s+1]
        yield grid[s-1:s*s-1:s-1]

    def _iter_lines(self, state: tuple[int, ...]):
        for i, j, k in self.index_list:
            yield state[i], state[j], state[k]

    def get_V(self, state: tuple[int, ...], player: int, action_space: set[int]) -> float:
        score = 0
        for line in self._iter_lines(state):
            p_count = line.count(self.player_1)
            a_count = line.count(self.player_2)
            if a_count == 0:
                if p_count == 2:
                    score += 3
                elif p_count == 1:
                    score += 1
            if p_count == 0:
                if a_count == 2:
                    score -= 3
                elif a_count == 1:
                    score -= 1
        return score if player == self.player_1 else -score


