import re
from math import floor
from os import listdir
from os.path import join, dirname, abspath
from typing import Dict, List

from src.app.config.template_item_args import FileItemArgs
from src.shared.annotation.singleton import singleton
from src.shared.helper.string_helper import has_column, count_white_spaces_until_not_blank_char


@singleton
class TemplateLoader:
    __MIN_HORIZONTAL_PADDING = 3
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

    def make_responsive(self, template: str) -> str:
        responsive = []

        lines = template.split("\n")
        titles_index = self.get_titles(lines)
        columns_width = self.get_table_columns_width(lines)

        max_width = max([len(line[1:-2]) + 2 for line in lines])

        for index, line in enumerate(lines):
            line_without_border = line[1:-2]

            if has_column(line_without_border):
                responsive_columns = []
                columns = line_without_border.split("|")
                number_of_columns = self.get_number_of_columns(line)
                column_width = columns_width[number_of_columns]

                for i, column in enumerate(columns):
                    if re.match(r"^\s*\d+\.\s+[A-Za-z]+\s*$", column):
                        content_index, content = [j.strip() for j in column.split(".", 1)]
                        column = f"{' ' * self.__MIN_HORIZONTAL_PADDING}{content_index}.{' ' * self.__MIN_HORIZONTAL_PADDING}{content}"
                        responsive_columns.append(
                            column.ljust(column_width[i])
                        )
                        continue

                    responsive_columns.append(
                        column.strip().center(column_width[i])
                    )

                responsive_table_line = "|".join(responsive_columns)

                if len(responsive_table_line) < max_width:
                    # Distribuir igualmente os espaços faltantes para atingir o valor de "max_width"
                    for i, column in enumerate(responsive_columns):
                        width = len(column) + (floor((max_width - len(responsive_table_line)) / number_of_columns))

                        if re.match(r"^\s*\d+\.\s+[A-Za-z]+\s*$", column):
                            responsive_columns[i] = column.ljust(width)
                        else:
                            responsive_columns[i] = column.center(width)

                    responsive_table_line = "|".join(responsive_columns).center(max_width)

                responsive.append(f'|{responsive_table_line}|')
                continue

            # responsividade na borda superior do template
            if index == 0 and self.is_border(line):
                first_line = line.center(max_width)
                responsive.append(f" {first_line.replace(' ', '_')} ")
                continue

            # responsividade nos divisores de conteúdo dentro do template
            if self.is_content_divider(line):
                responsive.append(f"|{line_without_border.center(max_width, ' ')}|".replace(" ", "-"))
                continue

            # responsividade na borda inferior do template
            if self.is_border(line):
                responsive.append(f"|{line_without_border.center(max_width)}|".replace(" ", "_"))
                continue

            # alinhar o título no centro
            if index in titles_index:
                responsive.append(f"|{line_without_border.center(max_width)}|")
                continue

            # alinhar tudo que não for título no lado esquerdo
            right_padding = count_white_spaces_until_not_blank_char(line_without_border)
            line = " " * right_padding + line_without_border.strip()

            responsive.append(f"|{line + ' ' * (max_width - len(line))}|")

        return "\n".join(responsive)

    @staticmethod
    def get_number_of_columns(line: str) -> int:
        return line.count("|") - 1

    @staticmethod
    def is_border(line: str) -> bool:
        return line.count("_") > len(line) / 2

    @staticmethod
    def is_content_divider(line: str) -> bool:
        return line.count("-") > len(line) / 2

    def get_titles(self, lines: List[str]) -> List[int]:
        titles_index = []

        for i, line in enumerate(lines):
            if i - 1 < 0 or i + 1 >= len(lines):
                continue

            previous = lines[i - 1]

            if not self.is_border(previous) and not self.is_content_divider(previous):
                continue

            later = lines[i + 1]

            if not self.is_border(later) and not self.is_content_divider(later):
                continue

            titles_index.append(i)

        return titles_index

    def get_table_columns_width(self, lines: List[str]) -> Dict[int, List[int]]:
        columns_width = {}

        for line in lines:
            if not has_column(line):
                continue

            number_of_column = self.get_number_of_columns(line)

            if number_of_column < 2:
                continue

            if number_of_column not in columns_width:
                columns_width.update({number_of_column: [0] * number_of_column})

            columns = line[1:-2].split("|")

            for index, column in enumerate(columns):
                column = " " * self.__MIN_HORIZONTAL_PADDING + \
                         column.replace("|", "").strip() + \
                         " " * self.__MIN_HORIZONTAL_PADDING
                column_width = len(column)

                if columns_width[number_of_column][index] >= column_width:
                    continue

                columns_width[number_of_column][index] = column_width

        return columns_width
