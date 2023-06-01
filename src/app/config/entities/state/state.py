from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def build(self) -> str:
        pass

    @abstractmethod
    def render(self) -> str:
        pass
