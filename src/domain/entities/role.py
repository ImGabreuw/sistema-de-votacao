from enum import Enum

from src.app.service.errors.illegal_argument_exception import IllegalArgumentException
from src.shared.monad.result import Result, Ok, Err


class Role(Enum):
    PRESIDENT = "presidente"
    GOVERNOR = "governador"
    MAYOR = "prefeito"


def find_role_by_name(role_name: str) -> Result[Role, IllegalArgumentException]:
    for role in Role:
        if role.value == role_name:
            return Ok(role)

    return Err(
        IllegalArgumentException(f"Não existe cargo ({role_name}) para disputa.")
    )
