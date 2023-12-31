from abc import ABC, abstractmethod


class BasePolicy(ABC):

    @abstractmethod
    def __call__(self, state: tuple[int], actions: set[int]) -> int:
        raise NotImplementedError
