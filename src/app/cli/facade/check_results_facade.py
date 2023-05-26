from dataclasses import dataclass
from typing import List

from src.app.cli.dto.ranking_dto import RankingDTO
from src.app.config.template_item_args import FileItemArgs
from src.app.config.template_loader import TemplateLoader
from src.domain.entities.role import Role
from src.domain.service.check_results_service import CheckResultService
from src.domain.service.errors.illegal_argument_exception import IllegalArgumentException
from src.shared.helper.number_helper import format_number
from src.shared.monad.result import Result, Err, Ok


@dataclass
class CheckResultsFacade:
    _template_loader: TemplateLoader
    _check_results_service: CheckResultService

    def show_results(self) -> None:
        result = self.show_winners()

        if result.is_err():
            print(result.get_error_message())
            return

        self.show_ranking()

    def show_winners(self) -> Result[None, IllegalArgumentException]:
        winners_template = self._template_loader.get_template("winners")
        result = self._check_results_service.get_winners()

        if result.is_err():
            return Err(result.propagate())

        voting_result = result.unwrap()
        mayor_winner = voting_result.mayor
        governor_winner = voting_result.governor
        president_winner = voting_result.president

        winners_template = winners_template.format(
            mayor_winner.name, mayor_winner.political_party,
            governor_winner.name, governor_winner.political_party,
            president_winner.name, president_winner.political_party
        )

        print(self._template_loader.make_responsive(winners_template))
        return Ok(None)

    def show_ranking(self) -> None:
        ranking = self._check_results_service.fetch_ranking()

        for index, role in enumerate(Role):
            role_ranking = ranking[index]

            report_template = self.__load_ranking_template(role, role_ranking)
            report_template = report_template.format(
                role_ranking.total_votes,
                role_ranking.total_valid_votes, role_ranking.perc_total_valid_votes,
                role_ranking.total_blank, role_ranking.perc_total_blank,
                role_ranking.total_null, role_ranking.perc_total_null
            )

            print(self._template_loader.make_responsive(report_template))

    def __load_ranking_template(self, role: Role, ranking: RankingDTO) -> str:
        ranking_template_item_args = [
            [
                index + 1,
                candidate.name,
                candidate.political_party,
                candidate.votes,
                format_number(candidate.perc_valid_votes)
            ] for index, candidate in enumerate(ranking.candidates)
        ]

        ranking_template = self._template_loader.get_template(f"ranking-{role.name.lower()}")
        ranking_template = self._template_loader.fill_files_item(
            ranking_template,
            [
                FileItemArgs(
                    len(ranking.candidates),
                    ranking_template_item_args
                )
            ]
        )

        return ranking_template
