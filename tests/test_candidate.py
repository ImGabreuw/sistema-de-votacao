from unittest import TestCase

from src.entities.candidate import create
from src.entities.role import Role


class TestCandidate(TestCase):
    def test_should_create_candidate(self):
        name = "Gabriel"
        number = 1
        political_party = "GAB"
        disputed_role = Role.PRESIDENT

        candidate_result = create(name, number, political_party, disputed_role)

        self.assertTrue(candidate_result.is_ok())

    def test_should_throw_error_when_create_candidate_because_name_is_blank(self):
        name = ""
        number = 1
        political_party = "GAB"
        disputed_role = Role.PRESIDENT

        candidate_result = create(name, number, political_party, disputed_role)

        self.assertTrue(candidate_result.is_err())

    def test_should_throw_error_when_create_candidate_because_number_is_negative(self):
        name = "Gabriel"
        number = -1
        political_party = "GAB"
        disputed_role = Role.PRESIDENT

        candidate_result = create(name, number, political_party, disputed_role)

        self.assertTrue(candidate_result.is_err())

    def test_should_throw_error_when_create_candidate_because_name_political_party_was_not_given(self):
        name = "Gabriel"
        number = 1
        political_party = ""
        disputed_role = Role.PRESIDENT

        candidate_result = create(name, number, political_party, disputed_role)

        self.assertTrue(candidate_result.is_err())

    def test_should_throw_error_when_create_candidate_because_disputed_role_was_not_given(self):
        name = "Gabriel"
        number = 1
        political_party = "GAB"

        candidate_result = create(name, number, political_party, None)

        self.assertTrue(candidate_result.is_err())
