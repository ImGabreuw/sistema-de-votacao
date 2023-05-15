from src.app.cli.facade.candidate_facade import CandidateFacade
from src.app.cli.facade.menu_facade import MenuFacade
from src.app.cli.facade.voter_facade import VoterFacade
from src.app.config.template_loader import TemplateLoader
from src.domain.service.candidate_service import CandidateService
from src.domain.service.voter_service import VoterService

if __name__ == '__main__':
    template_loader = TemplateLoader()
    candidate_service = CandidateService()
    voter_service = VoterService()

    while True:
        selected_option = MenuFacade(template_loader).show_menu()

        if selected_option == 1:
            CandidateFacade(candidate_service).register_candidates()

            for candidate in candidate_service.find_all():
                print(candidate)

        if selected_option == 2:
            VoterFacade(voter_service).register_voters()

            for voter in voter_service.find_all():
                print(voter)

        if selected_option == 6:
            print(template_loader.get_template("end"))
            break
