import re
from os import listdir
from os.path import join, dirname, abspath
from typing import Dict, List

from src.app.config.template_item_args import FileItemArgs
from src.shared.annotion.singleton import singleton
from src.shared.helper.string_helper import has_column, count_white_spaces_until_not_blank_char


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
        match = re.search(r"\{file:(.*?)}", template)

        lines = template.split("\n")

        if match:
            for index, filename in enumerate(match.groups()):
                filled_template = []
                template = self.templates[filename]
                current_file_args = file_item_args[index]

                for i in range(current_file_args.repeat_template):
                    filled_template.append(template.format(*current_file_args.args[i]))

                fill_index = lines.index("{file:" + filename + "}")

                lines[fill_index] = "\n".join(filled_template)

        return "\n".join(lines)

    @staticmethod
    def make_responsive(template: str) -> str:
        responsive = []

        lines = template.split("\n")

        titles_index = get_titles(lines)

        max_width = max([len(line) for line in lines])
        max_column_width = get_table_max_column_width(lines)

        for index, line in enumerate(lines):
            # responsividade na borda superior do template
            if index == 0 and is_border(line):
                first_line = line.center(max_width, ' ')
                responsive.append(f" {first_line.replace(' ', '_')} ")
                continue

            line_without_border = line[1:-2]

            if has_column(line_without_border):
                responsive_columns = []
                columns = line_without_border.split("|")
                column_width = max_column_width[get_number_of_columns(line)]

                for i, column in enumerate(columns):
                    responsive_columns.append(
                        column.center(column_width[i], " ")
                    )

                responsive_table_line = "|".join(responsive_columns)

                if len(responsive_table_line) < max_width:
                    responsive_table_line.center(max_width, " ")

                responsive.append(f'|{responsive_table_line}|')
                continue

            # responsividade nos divisores de conteúdo dentro do template
            if is_content_divider(line):
                responsive.append(f"|{line_without_border.center(max_width, ' ')}|".replace(" ", "-"))
                continue

            # responsividade na borda inferior do template
            if is_border(line):
                responsive.append(f"|{line_without_border.center(max_width, ' ')}|".replace(" ", "_"))
                continue

            # alinhar o título no centro
            if index in titles_index:
                responsive.append(f"|{line_without_border.center(max_width, ' ')}|")
                continue

            # alinhar tudo que não for título no lado esquerdo
            right_padding = count_white_spaces_until_not_blank_char(line_without_border)
            line = " " * right_padding + line_without_border.strip()

            responsive.append(f"|{line + ' ' * (max_width - len(line))}|")

        return "\n".join(responsive)


def get_number_of_columns(line: str) -> int:
    return line.count("|") - 1


def get_table_max_column_width(lines: List[str]) -> Dict[int, List[int]]:
    tables = {}

    for line in lines:
        if not has_column(line):
            continue

        number_of_column = get_number_of_columns(line)

        if number_of_column <= 2:
            continue

        if number_of_column not in tables:
            tables.update({number_of_column: []})

        columns = line[1:-2].split("|")

        for column in columns:
            column = column.replace("|", "")
            tables[number_of_column].append(len(column))

    return tables


def is_border(line: str) -> bool:
    return line.count("_") > len(line) / 2


def is_content_divider(line: str) -> bool:
    return line.count("-") > len(line) / 2


def get_titles(lines: List[str]) -> List[int]:
    titles_index = []

    for i, line in enumerate(lines):
        if i - 1 < 0 or i + 1 >= len(lines):
            continue

        previous = lines[i - 1]

        if not is_border(previous) and not is_content_divider(previous):
            continue

        later = lines[i + 1]

        if not is_border(later) and not is_content_divider(later):
            continue

        titles_index.append(i)

    return titles_index
