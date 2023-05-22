import textwrap
from dataclasses import dataclass

from src.domain.service.candidate_service import CandidateService
from src.domain.entities.role import format_roles
from src.shared.helper.number_helper import parse_int


@dataclass(frozen=True)
class CandidateFacade:
    _candidate_service: CandidateService

    def register_candidates(self) -> None:
        while True:
            print("\nInsira as informações do candidato:\n")

            name = input("Nome: ")
            number_result = parse_int(input("Número: "))
            political_party = input("Partido político: ")
            disputed_role = input(f"Cargo para disputa ({format_roles()}): ")

            if number_result.is_err():
                print(textwrap.dedent(
                    f"""
                    Não foi possível realizar o cadastro do candidato '{name}'.
                    Erro: {number_result.get_error_message()}
                    """
                ))
                continue

            result = self._candidate_service.register(
                name,
                number_result.unwrap(),
                political_party,
                disputed_role
            )

            if result.is_err():
                print(textwrap.dedent(
                    f"""
                    Não foi possível realizar o cadastro do candidato '{name}'.
                    Erro: {result.get_error_message()}
                    """
                ))
                continue

            if input("Deseja inserir um novo candidato? (SIM ou NAO) ").upper() == "NAO":
                break
