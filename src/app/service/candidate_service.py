from typing import List, Tuple, Dict

from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.entities.candidate import Candidate, create
from src.domain.entities.role import Role, find_role_by_name
from src.shared.monad.result import Result, Ok, Err


class CandidateService:
    president_candidates: List[Candidate] = []
    governor_candidates: List[Candidate] = []
    mayor_candidates: List[Candidate] = []

    def find_all(self) -> List[Candidate]:
        return [*self.president_candidates, *self.governor_candidates, *self.mayor_candidates]

    def is_unavailable_number(self, number: int) -> bool:
        for n in self.find_all():
            if n.number == number:
                return True

        return False

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
            role_result.unwrap()
        )

        if candidate_result.is_err():
            return Err(candidate_result.propagate())

        candidate = candidate_result.unwrap()

        if candidate.disputed_role == Role.PRESIDENT:
            self.president_candidates.append(candidate)
            return Ok(None)

        if candidate.disputed_role == Role.GOVERNOR:
            self.governor_candidates.append(candidate)
            return Ok(None)

        self.mayor_candidates.append(candidate)
        return Ok(None)

    def find_by_number(self, number: int) -> Result[Candidate, IllegalArgumentException]:
        for candidate in self.find_all():
            if candidate.number == number:
                return Ok(candidate)

        return Err(
            IllegalArgumentException(f"Não foi possível encontrar um candidato com o número '{number}'.")
        )

    def fetch_ranking(self) -> Tuple[List[Candidate], List[Candidate], List[Candidate]]:
        self.president_candidates.sort(
            key=lambda candidate: candidate.number_of_votes,
            reverse=True
        )
        self.governor_candidates.sort(
            key=lambda candidate: candidate.number_of_votes,
            reverse=True
        )
        self.mayor_candidates.sort(
            key=lambda candidate: candidate.number_of_votes,
            reverse=True
        )

        return self.mayor_candidates, self.governor_candidates, self.president_candidates

    def fetch_political_party_ranking(self) -> Dict[str, int]:
        count: Dict[str, int] = {}

        for candidate in self.find_all():
            political_party = candidate.political_party

            if political_party in count:
                count[political_party] += 1
                continue

            count.update({political_party: 1})

        return dict(sorted(
            count.items(),
            key=lambda item: item[1]
        ))
