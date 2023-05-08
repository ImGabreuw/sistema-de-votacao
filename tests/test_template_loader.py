from unittest import TestCase

from src.app.config.template_loader import TemplateLoader


class TestTemplateLoader(TestCase):
    templateLoader: TemplateLoader

    def setUp(self) -> None:
        self.templateLoader = TemplateLoader()

    def test_should_be_singleton(self):
        self.assertEqual(self.templateLoader, TemplateLoader())

    def test_get_template(self):
        for _, template in self.templateLoader.templates.items():
            self.assertIsNotNone(template)
