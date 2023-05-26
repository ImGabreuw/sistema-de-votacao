from unittest import TestCase

from src.app.config.template_item_args import FileItemArgs
from src.app.config.template_loader import TemplateLoader
from src.domain.entities.role import Role
from src.shared.helper.faker_helper import get_fake_instance


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

    def test_table_responsiveness(self):
        template = self.templateLoader.get_template("ranking-president")

        fake = get_fake_instance()

        args = []
        n = 10

        for i in range(n):
            args.append([
                i + 1,
                fake.unique.name(),
                fake.company(),
                fake.random_int(min=0),
                fake.random_int(min=0, max=100),
            ])

        template = self.templateLoader.fill_files_item(template, [
            FileItemArgs(n, args)
        ])

        template = template.format(
            10,
            8, 80,
            1, 10,
            1, 10
        )

        print(self.templateLoader.make_responsive(template))

    def test_make_responsive_on_confirm_vote(self):
        template = self.templateLoader.get_template("confirm-vote")
        template = template.format("Gabriel", "GAB", 1)

        template = self.templateLoader.make_responsive(template)

        print(template)
