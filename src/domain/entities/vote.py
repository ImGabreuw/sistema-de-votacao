from dataclasses import dataclass

from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.entities.role import Role
from src.shared.monad.result import Result, Err, Ok


@dataclass(frozen=True)
class Vote:
    role: Role
    candidate_number: int

    def is_blank(self) -> bool:
        return self.candidate_number == -1

    def is_null(self) -> bool:
        return self.candidate_number == -2

    def is_valid_vote(self) -> bool:
        return not (self.is_blank() or self.is_null())


def vote(role: Role, candidate_number: int) -> Result[Vote, IllegalArgumentException]:
    if candidate_number < -2:
        return Err(IllegalArgumentException("Número de candidato inválido."))

    return Ok(Vote(role, candidate_number))
