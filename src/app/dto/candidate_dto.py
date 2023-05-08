from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateDTO:
    name: str
    political_party: str
    votes: int
    valid_votes: float
