import textwrap
from dataclasses import dataclass

from src.domain.service.candidate_service import CandidateService
from src.domain.service.errors.illegal_argument_exception import IllegalArgumentException
from src.domain.service.errors.not_confirm_vote_exception import NotConfirmVoteException
from src.domain.service.voter_service import VoterService
from src.domain.service.voting_service import VotingService
from src.domain.adapter.confirm_vote import ConfirmVote
from src.domain.entities.role import Role
from src.domain.entities.vote import create
from src.domain.entities.voter import Voter
from src.shared.helper.number_helper import parse_int
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
            vote_result = self.__get_voter_votes(voter)

            if vote_result.is_err():
                if vote_result.propagate() is NotConfirmVoteException:
                    print(f"O voto do eleitor '{voter.name}' não foi confirmado.")
                    continue

                if vote_result.propagate() is IllegalArgumentException:
                    print(textwrap.dedent(
                        f"""
                        Não foi possível prosseguir com a votação de {voter.name}. 
                        Erro: {vote_result.get_error_message()}
                        """
                    ))
                    continue

            index += 1

        if index == 0:
            print("Erro: Registre os candidatos e eleitores antes de realizar a votação.")

    def __get_voter_votes(self, voter: Voter) -> Result[None, IllegalArgumentException | NotConfirmVoteException]:
        print(textwrap.dedent(f"""

        Voto do eleitor: {voter.name}
        (branco = -1 e nulo = -2)

        """))

        for role in Role:
            candidate_number_result = parse_int(input(f"Número do candidato para {role.value}: "))

            if candidate_number_result.is_err():
                return Err(candidate_number_result.propagate())

            candidate_number = candidate_number_result.unwrap()
            vote_result = create(role, candidate_number)

            if vote_result.is_err():
                return Err(vote_result.propagate())

            vote = vote_result.unwrap()

            confirm = self._confirm_vote.confirm(vote)

            if not confirm:
                return Err(NotConfirmVoteException())

            voter.add_vote(vote)

        result = self._voting_service.count_votes(voter)

        if result.is_err():
            return Err(result.propagate())

        return Ok(None)
