from dataclasses import dataclass, field
from typing import List

from src.app.config.entities.element import Element
from src.app.config.entities.elements.table.table_data import TableData
from src.app.config.entities.elements.table.table_head import TableHead


@dataclass
class TableRow(Element):
    elements: List[TableHead | TableData] = field(default_factory=list)

    def __init__(self, elements: List[TableHead | TableData]) -> None:
        super().__init__(elements, len(self.build()))

    def build(self) -> str:
        if not super()._is_changed:
            return self.built

        elements: List[str] = []

        for element in self.elements:
            if element.has_styles():
                element.apply_styles()

            elements.append(element.content)

        self.built = '|'.join(elements)

        super().has_built()
        return self.built
