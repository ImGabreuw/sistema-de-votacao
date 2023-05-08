from enum import Enum
from typing import Tuple


class Role(Enum):
    PRESIDENT = "presidente"
    GOVERNOR = "governador"
    MAYOR = "prefeito"


def find_role_by_name(role_name: str) -> Tuple[Role | None, Exception | None]:
    for role in Role:
        if role.value == role_name:
            return role, None

    return None, Exception(f"Não existe cargo ({role_name}) para disputa.")
