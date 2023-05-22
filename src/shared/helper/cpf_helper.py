import random


def is_valid_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    p = sum(int(cpf[i]) * (10 - i) for i in range(9)) % 11
    digit_1 = 0 if 11 - p > 9 else 11 - p

    q = sum(int(cpf[i]) * (11 - i) for i in range(10)) % 11
    digit_2 = 0 if 11 - q > 9 else 11 - q

    return int(cpf[-2]) == digit_1 and int(cpf[-1]) == digit_2


def generate_cpf():
    cpf = [random.randint(0, 9) for _ in range(9)]

    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11

        cpf.append(11 - val if val > 1 else 0)

    return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)


def format_cpf(cpf: str) -> str:
    cpf = ''.join(filter(str.isdigit, cpf))
    return cpf[:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:]
