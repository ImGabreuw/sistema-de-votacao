from unittest import TestCase

from src.domain.entities.candidate import create
from src.domain.entities.role import Role


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

    def test_not_eq_candidate(self):
        candidate_1 = create("Gabriel", 1, "AAA", Role.PRESIDENT).unwrap()
        candidate_2 = create("Enzo", 2, "BBB", Role.PRESIDENT).unwrap()

        self.assertFalse(candidate_1 == candidate_2)

    def test_eq_candidate(self):
        candidate_1 = create("Gabriel", 1, "AAA", Role.PRESIDENT).unwrap()
        candidate_2 = create("Gabriel", 2, "BBB", Role.PRESIDENT).unwrap()

        self.assertTrue(candidate_1 == candidate_2)

    def test_eq_other_not_candidate(self):
        candidate = create("Gabriel", 1, "AAA", Role.PRESIDENT).unwrap()
        other = "other"

        self.assertFalse(candidate == other)

    def test_get_number_of_votes(self):
        candidate = create("Gabriel", 1, "AAA", Role.PRESIDENT).unwrap()

        self.assertEqual(candidate.get_number_of_votes(), 0)

    def test_increment_vote(self):
        candidate = create("Gabriel", 1, "AAA", Role.PRESIDENT).unwrap()

        candidate.increment_vote()

        self.assertEqual(candidate.get_number_of_votes(), 1)
