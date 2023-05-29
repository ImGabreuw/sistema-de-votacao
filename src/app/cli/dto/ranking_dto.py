from dataclasses import dataclass
from typing import List

from src.app.cli.dto.candidate_dto import CandidateDTO


@dataclass(frozen=True)
class RankingDTO:
    candidates: List[CandidateDTO]

    total_votes: int

    total_valid_votes: int
    perc_total_valid_votes: str

    total_blank: int
    perc_total_blank: str

    total_null: int
    perc_total_null: str
