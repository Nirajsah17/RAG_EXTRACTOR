import datetime
from pathlib import Path

def path_to_name(path):
    return Path(path).stem


def timestamped_name(name: str):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_{timestamp}"


def file_to_timestamp_file(path):
    path = Path(path)
    name = path.stem
    return timestamped_name(name)