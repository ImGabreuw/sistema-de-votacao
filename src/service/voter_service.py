from typing import List, Tuple

from src.entities.voter import Voter
from src.utils.cpf_utils import is_valid_cpf


class VoterService:
    _voters: List[Voter] = []

    def register(self, name: str, cpf: str) -> Tuple[None, Exception]:
        voter, error = Voter.create(name, cpf)

        if error is Exception:
            return None, error

        self._voters.append(voter)

    def find_by_cpf(self, cpf: str) -> Tuple[Voter | None, Exception | None]:
        if not is_valid_cpf(cpf):
            return None, Exception("CPF inválido")

        for voter in self._voters:
            if voter.cpf == cpf:
                return voter, None

        return None, Exception(f"Não foi possível encontrar um eleitor com o CPF '{cpf}'.")

    def find_all(self) -> List[Voter]:
        return self._voters
