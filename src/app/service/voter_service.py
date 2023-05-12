from typing import List

from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.entities.voter import Voter, create
from src.shared.cpf_utils import is_valid_cpf
from src.shared.monad.result import Result, Err, Ok


class VoterService:
    _voters: List[Voter] = []

    def register(self, name: str, cpf: str) -> Result[None, IllegalArgumentException]:
        voter_result = create(name, cpf)

        if voter_result.is_err():
            return Err(voter_result.propagate())

        self._voters.append(voter_result.unwrap())

    def find_by_cpf(self, cpf: str) -> Result[Voter, IllegalArgumentException]:
        if not is_valid_cpf(cpf):
            return Err(IllegalArgumentException("CPF inválido"))

        for voter in self._voters:
            if voter.cpf == cpf:
                return Ok(voter)

        return Err(IllegalArgumentException(f"Não foi possível encontrar um eleitor com o CPF '{cpf}'."))

    def find_all(self) -> List[Voter]:
        self._voters.sort(key=lambda voter: voter.name)
        return self._voters

    def find_who_voted(self) -> List[Voter]:
        return [voter for voter in self._voters if voter.has_voted()]

    def is_all_voters_voted(self) -> bool:
        return len(self._voters) == len(self.find_who_voted())
