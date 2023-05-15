from dataclasses import dataclass
from typing import Tuple

from src.domain.entities.voter import Voter
from src.domain.service.candidate_service import CandidateService
from src.domain.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.service.voter_service import VoterService
from src.shared.monad.result import Result, Err, Ok


@dataclass
class VotingService:
    _candidate_service: CandidateService
    _voter_service: VoterService

    def count_votes(
            self,
            voter: Voter
    ) -> Result[None, IllegalArgumentException]:
        if not voter.has_voted():
            return Err(
                IllegalArgumentException(f"O eleitor '{voter.name}' ainda não votou.")
            )

        for role, vote in voter.votes.items():
            if not vote.is_valid_vote():
                continue

            candidate_result = self._candidate_service.find_by_number(vote.candidate_number)

            if candidate_result.is_err():
                # usuário inseriu um candidato inexiste -> voto nulo
                voter.votes[role].candidate_number = -2
                continue

            candidate_result.unwrap().increment_vote()

        return Ok(None)
