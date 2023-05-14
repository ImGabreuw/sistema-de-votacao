def normalize_person_name(name: str) -> str:
    return " ".join([i.lower().capitalize() for i in name.split()])
