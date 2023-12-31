from .base_q_policy import BaseQPolicySingle


class MinMaxPolicy(BaseQPolicySingle):

    def get_all_Qs(self, state: tuple[int], action_space: set[int]) -> dict[int, float]:
        pass

    def update_Q(self, state: tuple[int], action: int, Q: float) -> None:
        raise NotImplementedError

