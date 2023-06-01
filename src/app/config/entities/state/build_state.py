from src.app.config.entities.state.state import State


class BuildState(State):

    def build(self) -> str:
        pass

    def render(self) -> str:
        raise NotImplementedError("render method not implemented")
