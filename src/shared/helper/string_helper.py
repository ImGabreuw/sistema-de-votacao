def normalize_person_name(name: str) -> str:
    return " ".join([i.lower().capitalize() for i in name.split()])


def has_column(line: str) -> bool:
    return line.count("|") != 0


def count_white_spaces_until_not_blank_char(text: str) -> int:
    count = 0

    for i in text:
        if not i.isspace():
            break

        count += 1

    return count
