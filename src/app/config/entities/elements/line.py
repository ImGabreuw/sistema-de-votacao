from dataclasses import dataclass, field


@dataclass
class Line:
    symbol: str
    match_parent: bool = field(default=True)
