from typing import Any, List


class FileItemArgs:
    def __init__(self, repeat_template: int, args: List[List[Any]]) -> None:
        self.repeat_template = repeat_template
        self.args = args
