from src.app.cli.facade.candidate_facade import CandidateFacade
from src.app.cli.facade.voter_facade import VoterFacade
from src.domain.service.candidate_service import CandidateService
from src.domain.service.voter_service import VoterService

if __name__ == '__main__':
    candidate_service = CandidateService()
    voter_service = VoterService()

    CandidateFacade(candidate_service).register_candidates()
    VoterFacade(voter_service).register_voters()

    for candidate in candidate_service.find_all():
        print(candidate)
