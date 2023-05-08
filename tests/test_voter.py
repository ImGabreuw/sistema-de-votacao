from unittest import TestCase

from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.entities.role import Role
from src.domain.entities.vote import Vote
from src.domain.entities.voter import create


class Test(TestCase):
    def test_should_create_voter(self):
        name = "Gabriel"
        cpf = "237.972.060-62"

        voter_result = create(name, cpf)

        self.assertTrue(voter_result.is_ok())
        self.assertEqual(len(voter_result.unwrap().votes), 0)

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

        voter.voting(
            Vote(Role.MAYOR, 1),
            Vote(Role.GOVERNOR, 2),
            Vote(Role.PRESIDENT, 3),
        )

        self.assertEqual(len(voter.votes), 3)
