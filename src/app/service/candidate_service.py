from operator import itemgetter
from typing import List, Tuple

from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.entities.candidate import Candidate, create
from src.domain.entities.role import Role, find_role_by_name
from src.shared.monad.result import Result, Ok, Err


class CandidateService:
    _president_candidates: List[Candidate] = []
    _governor_candidates: List[Candidate] = []
    _mayor_candidates: List[Candidate] = []

    def find_all(self):
        return [*self._president_candidates, *self._governor_candidates, *self._mayor_candidates]

    def is_unavailable_number(self, number: int) -> bool:
        return any(number == i for i in self.find_all())

    def register(
            self,
            name: str,
            number: int,
            political_party: str,
            disputed_role: str
    ) -> Result[None, IllegalArgumentException]:
        role_result = find_role_by_name(disputed_role)

        if role_result.is_err():
            return Err(role_result.propagate())

        if self.is_unavailable_number(number):
            return Err(IllegalArgumentException(f"O número {number} já está em uso."))

        candidate_result = create(
            name,
            number,
            political_party,
            disputed_role,
        )

        if candidate_result.is_err():
            return Err(candidate_result.propagate())

        candidate = candidate_result.unwrap()

        if candidate.disputed_role == Role.PRESIDENT:
            self._president_candidates.append(candidate)
            return Ok(None)

        if candidate.disputed_role == Role.GOVERNOR:
            self._governor_candidates.append(candidate)
            return Ok(None)

        self._mayor_candidates.append(candidate)
        return Ok(None)

    def find_by_number(self, number: int) -> Result[Candidate, IllegalArgumentException]:
        for candidate in self.find_all():
            if candidate.number == number:
                return Ok(candidate)

        return Err(
            IllegalArgumentException(f"Não foi possível encontrar um candidato com o número '{number}'.")
        )

    def fetch_ranking(self) -> Tuple[List[Candidate], List[Candidate], List[Candidate]]:
        self._president_candidates.sort(
            key=itemgetter('number_of_votes'),
            reverse=True
        )
        self._governor_candidates.sort(
            key=itemgetter('number_of_votes'),
            reverse=True
        )
        self._mayor_candidates.sort(
            key=itemgetter('number_of_votes'),
            reverse=True
        )

        return self._mayor_candidates, self._governor_candidates, self._president_candidates
