from unittest import TestCase
from unittest.mock import patch

from src.app.cli.confirm_vote_cli import ConfirmVoteCLI
from src.app.config.template_loader import TemplateLoader
from src.domain.service.candidate_service import CandidateService
from src.domain.adapter.confirm_vote import ConfirmVote
from src.domain.entities.role import Role
from src.domain.entities.vote import vote


class TestConfirmVoteCLI(TestCase):
    confirm_vote: ConfirmVote

    def setUp(self) -> None:
        candidate_service = CandidateService()
        self.confirm_vote = ConfirmVoteCLI(TemplateLoader(), candidate_service)

        candidate_service.register(
            "Gabriel",
            1,
            "GAB",
            "presidente"
        )

    @patch("src.app.cli.confirm_vote_cli.ConfirmVoteCLI.confirm", return_value="SIM")
    def test_confirm(self, input):
        vote_result = vote(Role.PRESIDENT, 1)

        confirm = self.confirm_vote.confirm(vote_result.unwrap())

        self.assertTrue(confirm)
