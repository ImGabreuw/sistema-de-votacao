from unittest import TestCase

from src.app.service.candidate_service import CandidateService
from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.entities.role import Role


class TestCandidateService(TestCase):
    under_test: CandidateService

    def setUp(self) -> None:
        self.under_test = CandidateService()

        self.under_test.register(
            "Gabriel",
            1,
            "GAB",
            Role.PRESIDENT.value
        )
        self.under_test.register(
            "Enzo",
            2,
            "ENZO",
            Role.PRESIDENT.value
        )

    def test_should_find_all(self):
        candidates = self.under_test.find_all()

        self.assertIs(len(candidates), 2)

    def test_is_unavailable_number_return_true(self):
        is_unavailable = self.under_test.is_unavailable_number(1)

        self.assertTrue(is_unavailable)

    def test_is_unavailable_number_return_false(self):
        is_unavailable = self.under_test.is_unavailable_number(3)

        self.assertFalse(is_unavailable)

    def test_should_register_mayor(self):
        name = "Gabriel 2"
        number = 3
        political_party = "GAB2"
        disputed_role = Role.MAYOR.value

        result = self.under_test.register(
            name,
            number,
            political_party,
            disputed_role
        )

        self.assertTrue(result.is_ok())
        self.assertIsNone(result.unwrap())

    def test_should_register_governor(self):
        name = "Gabriel 2"
        number = 3
        political_party = "GAB2"
        disputed_role = Role.GOVERNOR.value

        result = self.under_test.register(
            name,
            number,
            political_party,
            disputed_role
        )

        self.assertTrue(result.is_ok())
        self.assertIsNone(result.unwrap())

    def test_should_register_president(self):
        name = "Gabriel 2"
        number = 3
        political_party = "GAB2"
        disputed_role = Role.PRESIDENT.value

        result = self.under_test.register(
            name,
            number,
            political_party,
            disputed_role
        )

        self.assertTrue(result.is_ok())
        self.assertIsNone(result.unwrap())

    def test_should_throw_illegal_argument_exception_when_register_because_role_is_invalid(self):
        name = "Gabriel 2"
        number = 3
        political_party = "GAB2"
        disputed_role = "aaa"

        result = self.under_test.register(
            name,
            number,
            political_party,
            disputed_role
        )

        self.assertTrue(result.is_err())
        with self.assertRaises(IllegalArgumentException, msg=f"Não existe cargo ({disputed_role}) para disputa."):
            result.unwrap()

    def test_should_throw_illegal_argument_exception_when_register_because_number_is_unavailable(self):
        name = "Gabriel 2"
        number = 1
        political_party = "GAB2"
        disputed_role = Role.MAYOR.value

        result = self.under_test.register(
            name,
            number,
            political_party,
            disputed_role
        )

        self.assertTrue(result.is_err())
        with self.assertRaises(IllegalArgumentException, msg=f"O número {number} já está em uso."):
            result.unwrap()

    def test_should_throw_illegal_argument_exception_when_register_because_name_is_blank(self):
        name = ""
        number = 3
        political_party = "GAB2"
        disputed_role = Role.MAYOR.value

        result = self.under_test.register(
            name,
            number,
            political_party,
            disputed_role
        )

        self.assertTrue(result.is_err())
        with self.assertRaises(IllegalArgumentException, msg="Nome do candidato é obrigatório."):
            result.unwrap()

    def test_should_find_candidate_by_number(self):
        number = 1

        candidate_result = self.under_test.find_by_number(number)

        self.assertTrue(candidate_result.is_ok())
        self.assertIs(candidate_result.unwrap().number, number)

    def test_should_not_find_candidate_by_number(self):
        number = 3

        candidate_result = self.under_test.find_by_number(number)

        self.assertTrue(candidate_result.is_err())
        with self.assertRaises(
                IllegalArgumentException,
                msg=f"Não foi possível encontrar um candidato com o número '{number}'."
        ):
            candidate_result.unwrap()

    def test_should_fetch_ranking(self):
        self.under_test.find_all()[0].increment_vote()

        _, _, president_candidates = self.under_test.fetch_ranking()

        self.assertIs(len(president_candidates), 2)
        self.assertEqual(
            president_candidates,
            sorted(
                self.under_test.president_candidates,
                key=lambda candidate: candidate.number_of_votes,
                reverse=True
            )
        )
