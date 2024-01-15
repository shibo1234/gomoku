from .base_value_function import BaseValueFunctionBatch


class QValueFunction(BaseValueFunctionBatch):
    def __init__(self):
        super().__init__()

    def get_V(self, state: tuple[int, ...], player: int) -> float:
        return super().get_V(state, player)

    def batch_get_V(self, states: list[tuple[int, ...]], players: list[int]) -> list[float]:
        return super().batch_get_V(states, players)