from src.app.cli.confirm_vote_cli import ConfirmVoteCLI
from src.app.cli.facade.candidate_facade import CandidateFacade
from src.app.cli.facade.menu_facade import MenuFacade
from src.app.cli.facade.report_facade import ReportFacade
from src.app.cli.facade.voter_facade import VoterFacade
from src.app.cli.facade.voting_facade import VotingFacade
from src.app.config.template_loader import TemplateLoader
from src.domain.service.candidate_service import CandidateService
from src.domain.service.voter_service import VoterService
from src.domain.service.voting_service import VotingService

if __name__ == '__main__':
    template_loader = TemplateLoader()
    candidate_service = CandidateService()
    voter_service = VoterService()
    confirm_vote_cli = ConfirmVoteCLI(template_loader, candidate_service)
    voting_service = VotingService(candidate_service, voter_service)

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

        if selected_option == 3:
            VotingFacade(
                confirm_vote_cli,
                voting_service,
                voter_service,
                candidate_service
            ).voting()

        if selected_option == 5:
            ReportFacade(
                candidate_service,
                voter_service,
                template_loader
            ).show_report()

        if selected_option == 6:
            print(template_loader.get_template("end"))
            break
