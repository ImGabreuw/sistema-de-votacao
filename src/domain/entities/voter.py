from dataclasses import dataclass, field
from typing import Dict

from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.entities import vote
from src.domain.entities.role import Role
from src.domain.entities.vote import Vote
from src.shared.cpf_utils import is_valid_cpf
from src.shared.monad.result import Result, Err, Ok


@dataclass
class Voter:
    name: str
    cpf: str
    votes: Dict[Role, Vote] = field(default_factory=dict)

    def voting(
            self,
            mayor: Vote,
            governor: Vote,
            president: Vote
    ) -> None:
        self.votes = {
            mayor.role: mayor,
            governor.role: governor,
            president.role: president
        }


def create(name: str, cpf: str) -> Result[Voter, IllegalArgumentException]:
    if len(name) == 0:
        return Err(
            IllegalArgumentException("Nome é obrigatório.")
        )

    if not is_valid_cpf(cpf):
        return Err(
            IllegalArgumentException("CPF inválido.")
        )

    return Ok(Voter(name, cpf))