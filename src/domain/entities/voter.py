from dataclasses import dataclass, field
from typing import Dict

from src.domain.entities.role import Role
from src.domain.entities.vote import Vote
from src.domain.service.errors.illegal_argument_exception import IllegalArgumentException
from src.shared.helper.cpf_helper import is_valid_cpf, format_cpf
from src.shared.helper.string_helper import normalize_person_name
from src.shared.monad.result import Result, Err, Ok


@dataclass
class Voter:
    name: str
    cpf: str
    votes: Dict[Role, Vote] = field(default_factory=dict)

    def __eq__(self, other):
        if not isinstance(other, Voter):
            return False
        return self.cpf == other.cpf

    def add_vote(
            self,
            vote: Vote
    ) -> None:
        self.votes.update({
            vote.role: vote
        })

    def has_voted(self) -> bool:
        return len(set(self.votes.keys())) == 3


def create(name: str, cpf: str) -> Result[Voter, IllegalArgumentException]:
    if len(name) == 0:
        return Err(
            IllegalArgumentException("Nome é obrigatório.")
        )

    if not is_valid_cpf(cpf):
        return Err(
            IllegalArgumentException("CPF inválido.")
        )

    return Ok(Voter(
        normalize_person_name(name),
        format_cpf(cpf)
    ))
