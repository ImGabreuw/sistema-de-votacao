from src.app.cli.adapter.confirm_vote_cli import ConfirmVoteCLI
from src.app.cli.facade.candidate_facade import CandidateFacade
from src.app.cli.facade.check_results_facade import CheckResultsFacade
from src.app.cli.facade.end_facade import EndFacade
from src.app.cli.facade.menu_facade import MenuFacade
from src.app.cli.facade.report_facade import ReportFacade
from src.app.cli.facade.voter_facade import VoterFacade
from src.app.cli.facade.voting_facade import VotingFacade
from src.app.config.template_loader import TemplateLoader
from src.domain.service.candidate_service import CandidateService
from src.domain.service.check_results_service import CheckResultService
from src.domain.service.voter_service import VoterService
from src.domain.service.voting_service import VotingService

if __name__ == '__main__':
    template_loader = TemplateLoader()
    candidate_service = CandidateService()
    voter_service = VoterService()
    confirm_vote_cli = ConfirmVoteCLI(template_loader, candidate_service)
    voting_service = VotingService(candidate_service, voter_service)
    check_results_service = CheckResultService(candidate_service, voter_service)

    menu_facade = MenuFacade(template_loader)
    candidate_facade = CandidateFacade(candidate_service)
    voter_facade = VoterFacade(voter_service)
    voting_facade = VotingFacade(
        confirm_vote_cli,
        voting_service,
        voter_service,
        candidate_service
    )
    check_results_facade = CheckResultsFacade(template_loader, check_results_service)
    report_facade = ReportFacade(
        candidate_service,
        voter_service,
        template_loader
    )
    end_facade = EndFacade(template_loader)

    while True:
        selected_option = menu_facade.show_menu()

        if selected_option == 1:
            candidate_facade.register_candidates()

        if selected_option == 2:
            voter_facade.register_voters()

        if selected_option == 3:
            voting_facade.voting()

        if selected_option == 4:
            check_results_facade.show_results()

        if selected_option == 5:
            report_facade.show_report()

        if selected_option == 6:
            end_facade.show_end()
            break
