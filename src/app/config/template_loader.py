from os import listdir
from os.path import join, dirname, abspath
from typing import Dict

from src.shared.annotion.singleton import singleton


@singleton
class TemplateLoader:
    _TEMPLATE_FOLDER_PATH = join(dirname(abspath(__file__)), "../../../templates")

    templates: Dict[str, str] = {}

    def __init__(self) -> None:
        super().__init__()
        self.__load()

    def __load(self) -> None:
        for filename in listdir(self._TEMPLATE_FOLDER_PATH):
            file_path = join(self._TEMPLATE_FOLDER_PATH, filename)

            with open(file_path, "r") as template:
                self.templates.update({
                    filename: template.read()
                })

    def get_template(self, filename: str) -> str:
        return self.templates[filename]
