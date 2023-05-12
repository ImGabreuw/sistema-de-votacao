from unittest import TestCase

from src.app.config.file_item_args import FileItemArgs
from src.app.config.template_loader import TemplateLoader
from src.domain.entities.voter import create


class TestTemplateLoader(TestCase):
    templateLoader: TemplateLoader

    def setUp(self) -> None:
        self.templateLoader = TemplateLoader()

    def test_should_be_singleton(self):
        self.assertEqual(self.templateLoader, TemplateLoader())

    def test_get_template(self):
        for _, template in self.templateLoader.templates.items():
            self.assertIsNotNone(template)

    def test_fill_files_item(self):
        template = self.templateLoader.get_template("report")

        template = self.templateLoader.fill_files_item(template, [
            FileItemArgs(
                4,
                [
                    [1, "Enzo"],
                    [2, "Gabriel"],
                    [3, "Felipe"],
                    [4, "Nicolas"],
                ]
            )
        ])

        print(self.templateLoader.make_responsive(template))
