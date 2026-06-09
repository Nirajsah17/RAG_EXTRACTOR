from pathlib import Path


def is_file_exist(path: str) -> bool:
    return Path(path).is_file()


def is_dir_exist(path: str) -> bool:
    return Path(path).is_dir()


def is_pdf(path: str) -> bool:
    return Path(path).suffix.lower() == ".pdf"


def is_dir_contains_pdf(path: str) -> bool:
    p = Path(path)

    if not p.is_dir():
        return False

    return any(
        file.is_file() and file.suffix.lower() == ".pdf"
        for file in p.iterdir()
    )