from dataclasses import dataclass
from typing import Tuple, List

from src.app.cli.dto.ranking_dto import RankingDTO
from src.app.cli.dto.voting_result_dto import VotingResultDTO
from src.app.service.candidate_service import CandidateService


@dataclass(frozen=True)
class CheckResultService:
    _candidate_service: CandidateService

    def get_winners(self) -> Tuple[VotingResultDTO | None, Exception | None]:
        mayor_ranking, governor_ranking, president_ranking = self._candidate_service.fetch_ranking()

        if len(mayor_ranking) == 0 \
                or len(governor_ranking) == 0 \
                or len(president_ranking) == 0:
            return None, Exception(
                "Apuração dos resultados cancelada por falta de candidato em uns dos cargos (prefeito, governador ou "
                "president)."
            )

        return VotingResultDTO(
            mayor_ranking[0],
            governor_ranking[0],
            president_ranking[0]
        ), None

    def fetch_ranking(self) -> List[RankingDTO]:
        ranking = []

        for role_ranking in self._candidate_service.fetch_ranking():
            for candidate in role_ranking:
                pass
            ranking.append(RankingDTO())

        return ranking
