from unittest import TestCase

from src.entities.voter import any_invalid_candidate_number, create
from src.service.errors.illegal_argument_exception import IllegalArgumentException


class Test(TestCase):
    def test_should_return_false_when_pass_candidate_number_grader_than_2(self):
        is_invalid = any_invalid_candidate_number(1, 2, -2)

        self.assertFalse(is_invalid)

    def test_should_return_true_when_pass_candidate_number_lower_than_3(self):
        is_invalid = any_invalid_candidate_number(1, 2, -3)

        self.assertTrue(is_invalid)

    def test_should_create_voter(self):
        name = "Gabriel"
        cpf = "237.972.060-62"

        voter_result = create(name, cpf)

        self.assertTrue(voter_result.is_ok())
        self.assertIsNone(voter_result.unwrap().vote)

    def test_should_throw_illegal_argument_exception_when_create_voter_because_name_is_blank(self):
        name = ""
        cpf = "237.972.060-62"

        voter_result = create(name, cpf)

        self.assertTrue(voter_result.is_err())
        with self.assertRaises(IllegalArgumentException, msg="Nome é obrigatório."):
            voter_result.unwrap()

    def test_should_throw_illegal_argument_exception_when_create_voter_because_cpf_is_invalid(self):
        name = "Gabriel"
        cpf = "123.456.789-00"

        voter_result = create(name, cpf)

        self.assertTrue(voter_result.is_err())
        with self.assertRaises(IllegalArgumentException, msg="CPF inválido."):
            voter_result.unwrap()

    def test_should_add_vote(self):
        name = "Gabriel"
        cpf = "237.972.060-62"

        voter = create(name, cpf).unwrap()

        voting_result = voter.voting(1, 2, 3)

        self.assertTrue(voting_result.is_ok())
        self.assertIsNotNone(voter.vote)

    def test_should_throw_illegal_argument_exception_when_voting_because_candidate_number_is_invalid(self):
        name = "Gabriel"
        cpf = "237.972.060-62"

        voter = create(name, cpf).unwrap()

        with self.assertRaises(IllegalArgumentException, msg="Voto inválido."):
            voting_result = voter.voting(1, 2, -3)

            self.assertTrue(voting_result.is_err())

            voting_result.unwrap()
