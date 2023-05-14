from src.app.cli.facade.candidate_facade import CandidateFacade
from src.domain.service.candidate_service import CandidateService

if __name__ == '__main__':
    candidate_service = CandidateService()

    CandidateFacade(candidate_service).register_candidates()

    for candidate in candidate_service.find_all():
        print(candidate)
