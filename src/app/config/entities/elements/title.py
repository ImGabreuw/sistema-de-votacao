from src.app.config.entities.element import Element
from src.app.config.entities.style import Style


class Title(Element):
    def __init__(self, content: str, width: int, style: Style = None) -> None:
        super().__init__(content, width, style)
