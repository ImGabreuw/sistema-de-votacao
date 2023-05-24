import textwrap
from dataclasses import dataclass

from src.domain.service.voter_service import VoterService


@dataclass
class VoterFacade:
    _voter_service: VoterService

    def register_voters(self) -> None:
        while True:
            print("\nInsira as informações do eleitor:\n")

            name = input("Nome: ")
            cpf = input("CPF: ")

            result = self._voter_service.register(
                name,
                cpf,
            )

            if result.is_err():
                print(textwrap.dedent(
                    f"""
                    Não foi possível realizar o cadastro do eleitor '{name}'.

                    Erro: {result.get_error_message()}
                    """
                ))
                continue

            if input("Deseja inserir um novo eleitor? (SIM ou NAO) ").upper() == "NAO":
                break
