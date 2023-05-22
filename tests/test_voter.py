from unittest import TestCase

from src.domain.entities.role import Role
from src.domain.entities.vote import Vote
from src.domain.entities.voter import create
from src.domain.service.errors.illegal_argument_exception import IllegalArgumentException


class Test(TestCase):
    def test_should_create_voter(self):
        name = "Gabriel"
        cpf = "237.972.060-62"

        voter_result = create(name, cpf)

        self.assertTrue(voter_result.is_ok())
        self.assertEqual(len(voter_result.unwrap().votes), 0)

    def test_not_eq_voter(self):
        voter_1 = create("Gabriel", "483.727.230-44").unwrap()
        voter_2 = create("Enzo", "649.958.900-41").unwrap()

        self.assertFalse(voter_1 == voter_2)

    def test_eq_voter(self):
        voter_1 = create("Gabriel", "483.727.230-44").unwrap()
        voter_2 = create("Enzo", "483.727.230-44").unwrap()

        self.assertTrue(voter_1 == voter_2)

    def test_eq_other_not_voter(self):
        voter = create("Gabriel", "483.727.230-44").unwrap()
        other = "aaa"

        self.assertFalse(voter == other)

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

        voter.add_vote(
            Vote(Role.MAYOR, 1),
        )

        self.assertEqual(len(voter.votes), 1)

    def test_has_voted(self):
        voter = create("Gabriel", "483.727.230-44").unwrap()

        voter.add_vote(
            Vote(Role.MAYOR, 1),
        )
        voter.add_vote(
            Vote(Role.GOVERNOR, 2),
        )
        voter.add_vote(
            Vote(Role.PRESIDENT, 3),
        )

        self.assertTrue(voter.has_voted())

    def test_has_not_voted(self):
        voter = create("Gabriel", "483.727.230-44").unwrap()

        voter.add_vote(
            Vote(Role.MAYOR, 1),
        )
        voter.add_vote(
            Vote(Role.GOVERNOR, 2),
        )

        self.assertFalse(voter.has_voted())
