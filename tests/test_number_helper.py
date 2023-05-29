from unittest import TestCase

from src.shared.helper.number_helper import format_number


class Test(TestCase):
    def test_format_number(self):
        number = 3.1415

        self.assertEqual(format_number(number), "3,14")
