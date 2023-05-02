from dataclasses import dataclass

from src.entities.voter import Voter


@dataclass
class Vote:
    voter: Voter
    mayor: int
    governor: int
    president: int
