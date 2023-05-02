from dataclasses import dataclass

from src.service.candidate_service import CandidateService
from src.service.voter_service import VoterService
from src.service.voting_service import VotingService


@dataclass
class VotingFacade:
    _voting_service: VotingService
    _voter_service: VoterService
    _candidate_service: CandidateService

    def confirm_vote(self, number: int) -> bool:
        candidate, error = self._candidate_service.find_by_number(number)

        if error is Exception or candidate.number == -2:
            print(f"""
            Confirmação do voto

            Voto nulo
            """)

        if candidate.number == -1:
            print(f"""
            Confirmação do voto

            Voto nulo
            """)

        print(f"""
        Confirmação do voto

        Candidato: {candidate.name} ({candidate.political_party})
        Número: {candidate.name}
        """)

        return input("Confirmar (SIM ou NÃO): ").upper() == "SIM"

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
