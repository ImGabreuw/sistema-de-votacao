from dataclasses import dataclass

from src.app.config.template_loader import TemplateLoader
from src.app.service.candidate_service import CandidateService
from src.domain.adapter.confirm_vote import ConfirmVote
from src.domain.entities.vote import Vote


@dataclass
class ConfirmVoteCLI(ConfirmVote):
    _template_loader: TemplateLoader
    _candidate_service: CandidateService

    def confirm(self, vote: Vote) -> bool:
        message: str

        if vote.is_blank():
            message = self._template_loader.get_template("confirm-blank-vote")
        elif vote.is_null():
            message = self._template_loader.get_template("confirm-null-vote")
        else:
            message = self._template_loader.get_template("confirm-vote")

        return input(message).upper() == "SIM"
