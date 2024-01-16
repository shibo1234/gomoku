from .base_value_function import BaseValueFunctionBatch
from ..policies.q_policies.base_q_policy import BaseQPolicy


class QValueFunction(BaseValueFunctionBatch):
    def __init__(self, q_policy: BaseQPolicy):
        super().__init__()
        self.policy = q_policy

    def batch_get_V(self,
                    states: list[tuple[int, ...]],
                    players: list[int],
                    action_spaces: list[set[int]]) -> list[float]:
        all_qs = self.policy.batch_get_all_Qs(states, players, action_spaces)
        return [max(qs.values()) for qs in all_qs]
