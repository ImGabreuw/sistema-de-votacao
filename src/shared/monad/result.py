from typing import Any, Callable, Generic, TypeVar, Literal, NoReturn, TypeAlias

T = TypeVar("T")
E = TypeVar("E", bound=BaseException)

"""
Reference: https://jellis18.github.io/post/2021-12-13-python-exceptions-rust-go/
"""


class Ok(Generic[T]):
    _value: T
    __match_args__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Ok) and self.unwrap == other.unwrap

    def is_ok(self) -> Literal[True]:
        return True

    def is_err(self) -> Literal[False]:
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, func: Callable[[E], T]) -> T:
        return self.unwrap()

    def unwrap_or_else(self, obj: T) -> T:
        return self.unwrap()

    def __repr__(self) -> str:
        return f"Ok({repr(self._value)})"


class Err(Generic[E]):
    _err: E
    __match_args__ = ("_err",)

    def __init__(self, err: E):
        self._err = err

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Err) and self.unwrap == other.unwrap

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
        return True

    def propagate(self) -> E:
        return self._err

    def get_error_message(self) -> str:
        return self._err.args[0]

    def unwrap(self) -> NoReturn:
        raise self._err

    def unwrap_or(self, func: Callable[[E], T]) -> T:
        return func(self._err)

    def unwrap_or_else(self, obj: T) -> T:
        return obj

    def __repr__(self) -> str:
        return f"Err({repr(self._err)})"


Result: TypeAlias = Ok[T] | Err[E]
