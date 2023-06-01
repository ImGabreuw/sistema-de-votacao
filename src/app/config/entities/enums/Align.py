from enum import Enum


def center(text: str, width: int, padding: int) -> str:
    return text.center(width)


def right(text: str, width: int, right_padding: int = 3) -> str:
    return text.rjust(right_padding).ljust(width)


def left(text: str, width: int, left_padding: int = 3) -> str:
    return text.ljust(left_padding).rjust(width)


class Align(Enum):
    CENTER = center
    RIGHT = right
    LEFT = left
