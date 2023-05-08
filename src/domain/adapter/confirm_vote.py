from abc import abstractmethod

from src.domain.entities.vote import Vote


class ConfirmVote:
    @abstractmethod
    def confirm(self, vote: Vote) -> bool:
        pass
