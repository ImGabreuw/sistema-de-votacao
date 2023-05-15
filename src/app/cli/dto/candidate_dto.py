from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateDTO:
    name: str
    political_party: str
    votes: int
    perc_valid_votes: float
