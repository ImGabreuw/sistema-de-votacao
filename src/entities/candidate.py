from dataclasses import dataclass
from typing import Tuple

from src.entities.candidate import Candidate
from src.entities.role import Role


@dataclass
class Candidate:
    name: str
    number: int
    political_party: str
    disputed_role: Role
    _number_of_votes: int

    @staticmethod
    def create(
            name: str,
            number: int,
            political_party: str,
            disputed_role: Role
    ) -> Tuple[Candidate | None, Exception | None]:
        if len(name) == 0:
            return None, Exception("Nome do candidato é obrigatório.")

        if disputed_role is None:
            return None, Exception("Cargo em disputa inválido.")

        return Candidate(
            name,
            number,
            political_party,
            disputed_role,
            0
        ), None

    def get_number_of_votes(self) -> int:
        return self._number_of_votes

    def increment_vote(self) -> None:
        self._number_of_votes += 1


