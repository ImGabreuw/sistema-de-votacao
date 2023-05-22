from typing import List

from faker import Faker

from src.shared.helper.cpf_helper import generate_cpf

_fake = Faker()


def get_fake_instance():
    return _fake


"""
CPF Provider
"""

_used_cpf: List[str] = []


def generate_unique_cpf():
    while True:
        cpf = generate_cpf()

        if is_cpf_unique(cpf):
            _used_cpf.append(cpf)
            return cpf


def is_cpf_unique(cpf):
    return cpf not in _used_cpf
