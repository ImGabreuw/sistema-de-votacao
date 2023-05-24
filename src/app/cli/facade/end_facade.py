from dataclasses import dataclass

from src.app.config.template_loader import TemplateLoader


@dataclass(frozen=True)
class EndFacade:
    _template_loader: TemplateLoader

    def show_end(self) -> None:
        end_template = self.__load_template()
        print(end_template)

    def __load_template(self) -> str:
        return self._template_loader.get_template("end")
