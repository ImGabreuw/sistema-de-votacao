from dataclasses import dataclass
from typing import Tuple, List, Dict

from src.app.cli.dto.candidate_dto import CandidateDTO
from src.app.cli.dto.ranking_dto import RankingDTO
from src.app.cli.dto.voting_result_dto import VotingResultDTO
from src.domain.entities.role import Role
from src.domain.service.candidate_service import CandidateService
from src.domain.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.service.voter_service import VoterService
from src.shared.monad.result import Result, Err, Ok


@dataclass(frozen=True)
class CheckResultService:
    _candidate_service: CandidateService
    _voter_service: VoterService

    def get_winners(self) -> Result[VotingResultDTO, IllegalArgumentException]:
        if self._candidate_service.is_insufficient_candidates():
            return Err(
                IllegalArgumentException(
                    "Apuração dos resultados cancelada por falta de candidato em uns dos cargos (prefeito, governador "
                    "ou presidente)."
                )
            )

        mayor_ranking, governor_ranking, president_ranking = self._candidate_service.fetch_ranking()

        return Ok(
            VotingResultDTO(
                mayor_ranking[0],
                governor_ranking[0],
                president_ranking[0]
            )
        )

    def fetch_ranking(self) -> List[RankingDTO]:
        ranking_dto = []
        ranking = self._candidate_service.fetch_ranking()

        for i in range(len(Role)):
            candidates: List[CandidateDTO] = []
            total_votes = len(self._voter_service.find_all()) * 3
            total_valid_votes = 0
            total_blank = 0
            total_null = 0

            for vote in self._voter_service.fetch_all_votes():
                if vote.is_blank():
                    total_blank += 1
                    continue

                if vote.is_null():
                    total_null += 1
                    continue

                total_valid_votes += 1

            for candidate in ranking[i]:
                candidates.append(CandidateDTO(
                    candidate.name,
                    candidate.political_party,
                    candidate.number_of_votes,
                    candidate.number_of_votes / total_valid_votes
                ))

            ranking_dto.append(RankingDTO(
                candidates,
                total_votes,
                total_valid_votes,
                total_valid_votes / total_votes,
                total_blank,
                total_blank / total_votes,
                total_null,
                total_null / total_votes
            ))

        return ranking_dto
