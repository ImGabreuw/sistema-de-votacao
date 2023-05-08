from dataclasses import dataclass

from src.app.service.candidate_service import CandidateService


@dataclass
class CandidateFacade:
    _candidate_service: CandidateService

    def register_candidates(self) -> None:
        while True:
            print("\nInsira as informações do candidato:\n")

            name = input("Nome: ")
            number = int(input("Número: "))
            political_party = input("Partido político: ")
            disputed_role = input("Cargo para disputa: ")

            result = self._candidate_service.register(
                name,
                number,
                political_party,
                disputed_role
            )

            if result is Exception:
                print(f"""
                        Não foi possível realizar o cadastro do candidato '{name}'.

                        Erro: {result.args}
                        """)
                continue

            if input("Deseja inserir um novo candidato? (SIM ou NÃO) ").upper() == "NÃO":
                break
