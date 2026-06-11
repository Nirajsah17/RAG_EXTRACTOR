import yaml
from dataclasses import dataclass

@dataclass
class Config:
    input_dir: str
    output_dir: str
    chunk_size: int
    chunk_overlap: int 
    enable_ocr: bool
    enable_tables: bool
    heading_font_size_threshold: float


def load_config(path="configs/config.yml") -> Config:
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    return Config(**data)