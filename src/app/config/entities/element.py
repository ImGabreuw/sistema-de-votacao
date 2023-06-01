from abc import abstractmethod, ABC
from dataclasses import dataclass, field

from src.app.config.entities.style import Style


@dataclass
class Element(ABC):
    content: any
    width: int
    style: Style = field(default=None)

    built: str = field(default="")
    _is_changed: bool = field(default=True)

    def fill(self, *args) -> None:
        self.content = self.content.format(*args)

    def has_styles(self) -> bool:
        return self.style is not None

    def apply_styles(self) -> None:
        self.content = self.style.align(
            self.content,
            self.width,
            self.style.padding
        )

    def must_build(self) -> None:
        self._is_changed = True

    def has_built(self) -> None:
        self._is_changed = False

    @abstractmethod
    def build(self) -> str:
        pass
