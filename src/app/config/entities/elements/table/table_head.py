from src.app.config.entities.element import Element
from src.app.config.entities.style import Style


class TableHead(Element):
    def __init__(self, title: str, width: int, style: Style = None) -> None:
        super().__init__(title, width, style)

    def build(self) -> str:
        pass


