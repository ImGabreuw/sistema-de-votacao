from dataclasses import dataclass

from src.app.config.entities.enums.Align import Align


@dataclass
class Style:
    align: Align
    padding: int = 3
