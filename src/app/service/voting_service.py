from dataclasses import dataclass
from typing import Tuple

from src.app.service.candidate_service import CandidateService
from src.app.service.voter_service import VoterService


@dataclass
class VotingService:
    _candidate_service: CandidateService
    _voter_service: VoterService

    def count_vote(
            self,
            voter_cpf: str,
            mayor_number: int,
            governor_number: int,
            president_number: int
    ) -> Tuple[None, Exception | None]:
        voter, error = self._voter_service.find_by_cpf(voter_cpf)

        if error is Exception:
            return None, error

        _, error = voter.count_votes(mayor_number, governor_number, president_number)

        if error is Exception:
            return None, error

        for number in [mayor_number, governor_number, president_number]:
            candidate, error = self._candidate_service.find_by_number(number)

            if error is Exception:
                return None, error

            candidate.increment_vote()

        return None, None
