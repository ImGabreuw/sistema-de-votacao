from src.shared.monad.result import Result, Err, Ok


def is_int(raw_int: str) -> bool:
    try:
        int(raw_int)
        return True
    except ValueError:
        return False


def parse_int(raw_int: str) -> Result[int, ValueError]:
    if not is_int(raw_int):
        return Err(ValueError(f"{raw_int} não é um número inteiro."))

    return Ok(int(raw_int))


def format_number(number: float, digits: int = 2) -> str:
    return f"{number:.{digits}f}".replace(".", ",")
