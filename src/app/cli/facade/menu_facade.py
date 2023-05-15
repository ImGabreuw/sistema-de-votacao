from dataclasses import dataclass

from src.app.config.template_loader import TemplateLoader
from src.shared.helper.number_helper import parse_int


@dataclass(frozen=True)
class MenuFacade:
    _template_loader: TemplateLoader

    def show_menu(self) -> int:
        menu_template = self.__load_menu_template()

        while True:
            print(menu_template)

            selected_option_result = parse_int(input("Opção escolhida: "))

            if selected_option_result.is_ok() and 1 <= selected_option_result.unwrap() <= 6:
                return selected_option_result.unwrap()

            print("Erro: Opção inválida.")

    def __load_menu_template(self) -> str:
        return self._template_loader.get_template("menu")
