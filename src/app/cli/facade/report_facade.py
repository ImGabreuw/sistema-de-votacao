from dataclasses import dataclass
from typing import List

from src.app.config.template_item_args import FileItemArgs
from src.app.config.template_loader import TemplateLoader
from src.domain.service.candidate_service import CandidateService
from src.domain.service.voter_service import VoterService
from src.domain.entities.voter import Voter


@dataclass
class ReportFacade:
    _candidate_service: CandidateService
    _voter_service: VoterService
    _template_loader: TemplateLoader

    def show_report(self) -> None:
        if self._candidate_service.is_insufficient_candidates():
            print(
                "Apuração dos resultados cancelada por falta de candidato em uns dos cargos (prefeito, governador ou "
                "presidente)."
            )
            return

        voters = self._voter_service.find_all()
        report_template = self.__load_report_template(voters)

        valid_election = self._voter_service.is_all_voters_voted()
        who_voted = len(self._voter_service.fetch_who_voted())
        total = len(self._voter_service.find_all())
        political_party_ranking = list(self._candidate_service.fetch_political_party_ranking().keys())

        report_template = report_template.format(
            "SIM" if valid_election else "NÃO",
            who_voted,
            total,
            political_party_ranking[0],
            political_party_ranking[-1]
        )

        print(self._template_loader.make_responsive(report_template))

    def __load_report_template(self, voters: List[Voter]) -> str:
        report_template_item_args = [[index + 1, voter.name] for index, voter in enumerate(voters)]

        report_template = self._template_loader.get_template("report")
        report_template = self._template_loader.fill_files_item(
            report_template,
            [
                FileItemArgs(
                    len(voters),
                    report_template_item_args
                )
            ]
        )
        return report_template
