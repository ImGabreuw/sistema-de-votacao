from dataclasses import dataclass

from src.app.service.candidate_service import CandidateService
from src.app.service.voter_service import VoterService
from src.app.service.voting_service import VotingService


@dataclass
class VotingFacade:
    _voting_service: VotingService
    _voter_service: VoterService
    _candidate_service: CandidateService

    def voting(self) -> None:
        voters = self._voter_service.find_all()
        index = 0

        while index < len(voters):
            voter = voters[index]

            print(f"""
            
            Voto do eleitor: {voter.name}
            (branco = -1 e nulo = -2)
            
            """)

            mayor_number = int(input("Número do candidato para prefeito: "))
            if not self.confirm_vote(mayor_number):
                continue

            governor_number = int(input("Número do candidato para governador: "))
            if not self.confirm_vote(governor_number):
                continue

            president_number = int(input("Número do candidato para presidente: "))
            if not self.confirm_vote(president_number):
                continue

            _, error = self._voting_service.count_vote(voter.cpf, mayor_number, governor_number, president_number)

            if error is Exception:
                print(f"Não foi possível contabilizar o voto do eleitor '{voter.name}'.")
                continue

            index += 1
