from typing import List, Dict

import pyautogui

from src.domain.entities.role import Role
from src.shared.helper.faker_helper import get_fake_instance, generate_unique_cpf
from src.shared.helper.pyautogui_helper import write_multiple_lines

used_candidates_number: Dict[Role, List[int]] = {
    Role.PRESIDENT: [-2, -1],
    Role.GOVERNOR: [-2, -1],
    Role.MAYOR: [-2, -1],
}

fake = get_fake_instance()


def open_and_run_main_py():
    pyautogui.press(["shift", "shift"])
    pyautogui.PAUSE = 2.5

    pyautogui.write("main.py")
    pyautogui.PAUSE = 1

    pyautogui.press("enter")
    pyautogui.hotkey("ctrl", "shift", "f10")
    pyautogui.PAUSE = 1.5

    # Abrir o terminal onde o programa está sendo executado
    pyautogui.hotkey("alt", "4")


def register_candidates(n: int):
    pyautogui.write("1")
    pyautogui.press("enter")

    for i in range(1, n + 1):
        candidate_number = fake.unique.random_int(min=1)
        role = list(Role)[fake.random_int(min=0, max=2)]

        if candidate_number not in used_candidates_number[role]:
            used_candidates_number[role].append(candidate_number)

        write_multiple_lines(
            fake.unique.name(),
            candidate_number,
            fake.company(),
            role.value,
        )

        pyautogui.write("NAO" if i == n else "SIM")
        pyautogui.press("enter")

    pyautogui.PAUSE = 0.5


def register_voters(n: int):
    global number_voters
    number_voters = n

    pyautogui.write("2")
    pyautogui.press("enter")

    for i in range(1, n + 1):
        write_multiple_lines(
            fake.name(),
            generate_unique_cpf()
        )

        pyautogui.write("NAO" if i == n else "SIM")
        pyautogui.press("enter")

    pyautogui.PAUSE = 0.5


def voting():
    pyautogui.write("3")
    pyautogui.press("enter")

    for _ in range(number_voters):
        for role in Role:
            rand_index = fake.random_int(min=0, max=len(used_candidates_number[role]) - 1)
            candidate_number = used_candidates_number[role][rand_index]

            pyautogui.write(str(candidate_number))
            pyautogui.press("enter")
            pyautogui.PAUSE = 0.5

            pyautogui.write("SIM")
            pyautogui.press("enter")
            pyautogui.PAUSE = 0.5


def voting_results():
    pyautogui.write("4")
    pyautogui.press("enter")
    pyautogui.PAUSE = 0.5


def report():
    pyautogui.write("5")
    pyautogui.press("enter")
    pyautogui.PAUSE = 0.5


def end():
    pyautogui.write("6")
    pyautogui.press("enter")


if __name__ == '__main__':
    open_and_run_main_py()
    register_candidates(3)
    register_voters(3)
    voting()
    voting_results()
    report()
    end()
