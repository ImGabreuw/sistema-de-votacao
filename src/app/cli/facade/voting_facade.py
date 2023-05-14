from dataclasses import dataclass

from src.domain.service.candidate_service import CandidateService
from src.domain.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.service.errors.not_confirm_vote_exception import NotConfirmVoteException
from src.domain.service.voter_service import VoterService
from src.domain.service.voting_service import VotingService
from src.domain.adapter.confirm_vote import ConfirmVote
from src.domain.entities.role import Role
from src.domain.entities.vote import vote
from src.domain.entities.voter import Voter
from src.shared.monad.result import Result, Err, Ok


@dataclass
class VotingFacade:
    _confirm_vote: ConfirmVote
    _voting_service: VotingService
    _voter_service: VoterService
    _candidate_service: CandidateService

    def voting(self) -> None:
        index = 0
        voters = self._voter_service.find_all()

        while index < len(voters):
            voter = voters[index]
            vote_result = self.__count_vote(voter)

            if vote_result.propagate() is NotConfirmVoteException:
                print(f"O voto do eleitor '{voter.name}' não foi confirmado.")
                continue

            if vote_result.propagate() is IllegalArgumentException:
                print(f"Não foi possível prosseguir com a votação. Erro: {vote_result.propagate()}")

            index += 1

    def __count_vote(self, voter: Voter) -> Result[None, IllegalArgumentException | NotConfirmVoteException]:
        print(f"""

        Voto do eleitor: {voter.name}
        (branco = -1 e nulo = -2)

        """)

        for role in Role:
            candidate_number = int(input(f"Número do candidato para {role.value}: "))
            vote_result = vote(role, candidate_number)

            if vote_result.is_err():
                return Err(vote_result.propagate())

            confirm = self._confirm_vote.confirm(vote_result.unwrap())

            if not confirm:
                return Err(NotConfirmVoteException())

            voter.add_vote(vote_result.unwrap())

        return Ok(None)
