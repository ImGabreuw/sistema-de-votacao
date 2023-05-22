import pyautogui

from src.domain.entities.role import Role
from src.shared.helper.faker_helper import get_fake_instance, generate_unique_cpf
from src.shared.helper.pyautogui_helper import write_multiple_lines

fake = get_fake_instance()


def open_and_run_main_py():
    pyautogui.press(["shift", "shift"])
    pyautogui.PAUSE = 1.5

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
        write_multiple_lines(
            fake.unique.name(),
            fake.unique.random_int(min=1),
            fake.company(),
            list(Role)[fake.random_int(min=0, max=2)].value,
        )

        pyautogui.write("NAO" if i == n else "SIM")
        pyautogui.press("enter")

    pyautogui.PAUSE = 0.5


def register_voters(n: int):
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


if __name__ == '__main__':
    open_and_run_main_py()
    register_candidates(3)
    register_voters(3)
