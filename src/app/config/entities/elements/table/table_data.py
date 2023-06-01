from dataclasses import dataclass, field

from src.app.config.entities.element import Element
from src.app.config.entities.elements.table.table_head import TableHead


@dataclass
class TableData(Element):
    parent: TableHead = field(default=None)

    def __init__(self, content: str) -> None:
        super().__init__(content=content)

    def bind(self, parent: TableHead) -> None:
        self.parent = parent
        self.width = parent.width
        self.style = parent.style
