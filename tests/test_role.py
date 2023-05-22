from unittest import TestCase

from src.domain.entities.role import find_role_by_name, Role, format_roles
from src.domain.service.errors.illegal_argument_exception import IllegalArgumentException


class TestRole(TestCase):

    def test_find_role_by_name(self):
        under_test = find_role_by_name("presidente").unwrap()

        self.assertEquals(under_test, Role.PRESIDENT)

    def test_find_role_by_name_throw_illegal_argument_exception(self):
        role_name = "aaaa"
        under_test = find_role_by_name(role_name)

        with self.assertRaises(IllegalArgumentException, msg=f"Não existe cargo ({role_name}) para disputa."):
            under_test.unwrap()

    def test_format_roles(self):
        under_test = format_roles()

        self.assertEquals(under_test, "prefeito / governador / presidente")
