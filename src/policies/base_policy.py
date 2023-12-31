from abc import ABC, abstractmethod


class BasePolicy(ABC):

    @abstractmethod
    def __call__(self, state: tuple[int], player: int, action_space: set[int]) -> int:
        raise NotImplementedError
