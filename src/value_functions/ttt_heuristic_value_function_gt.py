from .base_value_function import BaseValueFunctionSingle

import numpy as np
import torch


class TTTHeuristicValueFunctionGT(BaseValueFunctionSingle):
    def __init__(self):
        super().__init__()

    def lines(self, state: tuple[int, ...]):
        for i in (0, 1, 2):
            yield state[i], state[i + 3], state[i + 6]
        for i in (0, 3, 6):
            yield state[i], state[i + 1], state[i + 2]
        for i in (0,):
            yield state[i], state[i + 4], state[i + 8]
        for i in (2,):
            yield state[i], state[i + 2], state[i + 4]

    def get_V(self, state: tuple[int, ...], player: int, action_space: set[int]) -> float:
        p1 = p2 = a1 = a2 = 0
        for line in self.lines(state):
            p_count = line.count(player)
            a_count = line.count(-player)
            if p_count == 2 and a_count == 0:
                p2 += 1
            if p_count == 1 and a_count == 0:
                p1 += 1
            if p_count == 0 and a_count == 2:
                a2 += 1
            if p_count == 0 and a_count == 1:
                a1 += 1
        return 3 * p2 + p1 - (3 * a2 + a1)

