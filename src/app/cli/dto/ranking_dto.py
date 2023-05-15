from dataclasses import dataclass
from typing import List

from src.app.cli.dto.candidate_dto import CandidateDTO


@dataclass(frozen=True)
class RankingDTO:
    candidates: List[CandidateDTO]

    total_votes: int

    total_valid_votes: int
    perc_total_valid_votes: float

    total_blank: int
    perc_total_blank: float

    total_null: int
    perc_total_null: float
