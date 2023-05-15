import re
from os import listdir
from os.path import join, dirname, abspath
from typing import Dict, List

from src.app.config.template_item_args import FileItemArgs
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

    def fill_files_item(self, template: str, file_item_args: List[FileItemArgs]) -> str:
        filled_template = ""
        match = re.search(r"\{file:(.*?)}", template)

        if match:
            for index, filename in enumerate(match.groups()):
                template = self.templates[filename]
                current_file_args = file_item_args[index]

                for i in range(current_file_args.repeat_template):
                    filled_template += template.format(*current_file_args.args[i]) + "\n"

        return filled_template

    @staticmethod
    def make_responsive(template: str) -> str:
        responsive = []

        lines = template.split("\n")
        # lines.pop()

        max_width = max([len(line) for line in lines])

        for index, line in enumerate(lines):
            # responsividade na borda superior do template
            if index == 0:
                first_line = line.center(max_width, ' ')
                responsive.append(f" {first_line.replace(' ', '_')} ")
                continue

            line_without_border = line[1:-2]

            # responsividade nos divisores de conteúdo dentro do template
            if line.count("-") > len(line) / 2:
                responsive.append(f"|{line_without_border.center(max_width, ' ')}|".replace(" ", "-"))
                continue

            # responsividade na borda inferior do template
            if line.count("_") > len(line) / 2:
                responsive.append(f"|{line_without_border.center(max_width, ' ')}|".replace(" ", "_"))
                continue

            responsive.append(f"|{line_without_border.center(max_width, ' ')}|")

        return "\n".join(responsive)
