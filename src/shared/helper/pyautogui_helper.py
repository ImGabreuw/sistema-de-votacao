import pyautogui


def write_multiple_lines(*args) -> None:
    for i in range(len(args)):
        pyautogui.write(str(args[i]))
        pyautogui.press("enter")
        pyautogui.PAUSE = 0.5
