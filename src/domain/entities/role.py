from enum import Enum

from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.shared.monad.result import Result, Ok, Err


class Role(Enum):
    MAYOR = "prefeito"
    GOVERNOR = "governador"
    PRESIDENT = "presidente"


def find_role_by_name(role_name: str) -> Result[Role, IllegalArgumentException]:
    for role in Role:
        if role.value == role_name:
            return Ok(role)

    return Err(
        IllegalArgumentException(f"Não existe cargo ({role_name}) para disputa.")
    )


def format_roles() -> str:
    return " / ".join([role.value for role in Role])
