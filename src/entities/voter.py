from dataclasses import dataclass

from src.entities.vote import Vote
from src.service.errors.illegal_argument_exception import IllegalArgumentException
from src.utils.cpf_utils import is_valid_cpf
from src.utils.monad.result import Result, Err, Ok


def any_invalid_candidate_number(*numbers) -> bool:
    return any(number < -2 for number in numbers)


@dataclass
class Voter:
    name: str
    cpf: str
    vote: Vote | None

    def voting(
            self,
            mayor_number: int,
            governor_number: int,
            president_number: int
    ) -> Result[None, IllegalArgumentException]:
        if any_invalid_candidate_number(mayor_number, governor_number, president_number):
            return Err(IllegalArgumentException("Voto inválido."))

        self.vote = Vote(mayor_number, governor_number, president_number)

        return Ok(None)


def create(name: str, cpf: str) -> Result[Voter, IllegalArgumentException]:
    if len(name) == 0:
        return Err(
            IllegalArgumentException("Nome é obrigatório.")
        )

    if not is_valid_cpf(cpf):
        return Err(
            IllegalArgumentException("CPF inválido.")
        )

    return Ok(Voter(name, cpf, None))
