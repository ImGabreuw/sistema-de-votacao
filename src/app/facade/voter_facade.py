from dataclasses import dataclass

from src.app.service.voter_service import VoterService


@dataclass
class VoterFacade:
    _voter_service: VoterService

    def register_candidates(self) -> None:
        while True:
            print("\nInsira as informações do candidato:\n")

            name = input("Nome: ")
            cpf = input("CPF: ")

            _, error = self._voter_service.register(
                name,
                cpf,
            )

            if error is Exception:
                print(f"""
                        Não foi possível realizar o cadastro do eleitor '{name}'.

                        Erro: {error.args}
                        """)
                continue

            if input("Deseja inserir um novo candidato? (SIM ou NÃO) ").upper() == "NÃO":
                break
