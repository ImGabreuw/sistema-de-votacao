from dataclasses import dataclass

from src.domain.entities.candidate import Candidate


@dataclass(frozen=True)
class VotingResultDTO:
    mayor: Candidate
    governor: Candidate
    president: Candidate
