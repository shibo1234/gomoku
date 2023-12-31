from ..base_policy import BasePolicy

from abc import abstractmethod
import itertools as it


class BaseQPolicy(BasePolicy):

    def __call__(self, state: tuple[int], action_space: set[int]) -> int:
        q_dict = self.get_all_Qs(state, action_space)
        return max(q_dict, key=q_dict.__getitem__)

    def get_Q(self, state: tuple[int], action: int) -> float:
        return self.get_all_Qs(state, {action})[action]

    def batch_get_Q(self, states: list[tuple[int]], actions: list[int]) -> list[float]:
        return list(map(
            lambda qd: list(qd.values)[0],
            self.batch_get_all_Qs(states, [{action} for action in actions])
        ))

    @abstractmethod
    def get_all_Qs(self, state: tuple[int], action_space: set[int]) -> dict[int, float]:
        return self.batch_get_all_Qs([state], [action_space])[0]

    @abstractmethod
    def batch_get_all_Qs(self, states: list[tuple[int]], action_spaces: list[set[int]]) -> list[dict[int, float]]:
        return list(it.starmap(self.get_all_Qs, zip(states, action_spaces)))

    @abstractmethod
    def update_Q(self, state: tuple[int], action: int, Q: float) -> None:
        self.batch_update_Q([state], [action], [Q])

    @abstractmethod
    def batch_update_Q(self, states: list[tuple[int]], actions: list[int], Qs: list[float]) -> None:
        list(it.starmap(self.update_Q, zip(states, actions, Qs)))


class BaseQPolicySingle(BaseQPolicy):

    @abstractmethod
    def get_all_Qs(self, state: tuple[int], action_space: set[int]) -> dict[int, float]:
        raise NotImplementedError

    def batch_get_all_Qs(self, states: list[tuple[int]], action_spaces: list[set[int]]) -> list[dict[int, float]]:
        return super().batch_get_all_Qs(states, action_spaces)

    @abstractmethod
    def update_Q(self, state: tuple[int], action: int, Q: float) -> None:
        raise NotImplementedError

    def batch_update_Q(self, states: list[tuple[int]], actions: list[int], Qs: list[float]) -> None:
        super().batch_update_Q(states, actions, Qs)


class BaseQPolicyBatch(BaseQPolicy):

    def get_all_Qs(self, state: tuple[int], action_space: set[int]) -> dict[int, float]:
        return super().get_all_Qs(state, action_space)

    @abstractmethod
    def batch_get_all_Qs(self, states: list[tuple[int]], action_spaces: list[set[int]]) -> list[dict[int, float]]:
        raise NotImplementedError

    def update_Q(self, state: tuple[int], action: int, Q: float) -> None:
        super().update_Q(state, action, Q)

    @abstractmethod
    def batch_update_Q(self, states: list[tuple[int]], actions: list[int], Qs: list[float]) -> None:
        raise NotImplementedError
