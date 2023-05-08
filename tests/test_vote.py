from unittest import TestCase

from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.entities.role import Role
from src.domain.entities.vote import vote


class TestVote(TestCase):

    def test_should_create_vote(self):
        role = Role.PRESIDENT
        candidate_number = 1

        vote_result = vote(role, candidate_number)

        self.assertTrue(vote_result.is_ok())

    def test_should_throw_illegal_argument_exception_when_create_vote_because_candidate_number_is_invalid(self):
        role = Role.PRESIDENT
        candidate_number = -3

        vote_result = vote(role, candidate_number)

        self.assertTrue(vote_result.is_err())
        with self.assertRaises(IllegalArgumentException, msg="Número de candidato inválido."):
            vote_result.unwrap()

    def test_is_blank(self):
        role = Role.PRESIDENT
        candidate_number = -1

        vote_result = vote(role, candidate_number)

        self.assertTrue(vote_result.unwrap().is_blank())

    def test_is_null(self):
        role = Role.PRESIDENT
        candidate_number = -2

        vote_result = vote(role, candidate_number)

        self.assertTrue(vote_result.unwrap().is_null())

    def test_is_valid_vote(self):
        role = Role.PRESIDENT
        candidate_number = 1

        vote_result = vote(role, candidate_number)

        self.assertTrue(vote_result.unwrap().is_valid_vote())
