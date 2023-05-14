from dataclasses import dataclass

from src.domain.entities.role import Role
from src.domain.service.errors.illegal_argument_exception import IllegalArgumentException
from src.shared.helper.string_helper import normalize_person_name
from src.shared.monad.result import Result, Err, Ok


@dataclass
class Candidate:
    name: str
    number: int
    political_party: str
    disputed_role: Role
    number_of_votes: int

    def __eq__(self, other) -> bool:
        if not isinstance(other, Candidate):
            return False

        return self.name == other.name

    def get_number_of_votes(self) -> int:
        return self.number_of_votes

    def increment_vote(self) -> None:
        self.number_of_votes += 1


def create(
        name: str,
        number: int,
        political_party: str,
        disputed_role: Role
) -> Result[Candidate, IllegalArgumentException]:
    if len(name) == 0:
        return Err(
            IllegalArgumentException("Nome do candidato é obrigatório.")
        )

    if number < 0:
        return Err(
            IllegalArgumentException("O número do candidato deve ser positivo ou 0.")
        )

    if len(political_party) == 0:
        return Err(
            IllegalArgumentException("Partido político é obrigatório.")
        )

    if disputed_role is None:
        return Err(
            IllegalArgumentException("Cargo em disputa é obrigatório.")
        )

    return Ok(Candidate(
        normalize_person_name(name),
        number,
        political_party.upper(),
        disputed_role,
        0
    ))
