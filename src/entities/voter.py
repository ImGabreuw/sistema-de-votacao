from dataclasses import dataclass
from typing import Tuple, List

from src.entities.voter import Voter
from src.utils.cpf_utils import is_valid_cpf


def any_invalid_candidate_number(*numbers) -> bool:
    return any(number < -2 for number in numbers)


@dataclass()
class Voter:
    name: str
    cpf: str
    mayor: int
    governor: int
    president: int

    @staticmethod
    def create(name: str, cpf: str) -> Tuple[Voter | None, Exception | None]:
        if not is_valid_cpf(cpf):
            return None, Exception("CPF inválido.")

        return Voter(name, cpf, -2, -2, -2), None

    def count_votes(
            self,
            mayor_number: int,
            governor_number: int,
            president_number: int
    ) -> Tuple[None, Exception | None]:
        if any_invalid_candidate_number(mayor_number, governor_number, president_number):
            return None, Exception("Voto inválido.")

        self.mayor = mayor_number
        self.governor = governor_number
        self.president = president_number
