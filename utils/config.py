import json
from pydantic import BaseModel
from pathlib import Path

class Config(BaseModel):
    base_url: str
    output_dir: str
    csv_path: str
    csv_delimiter: str = ","
    date_from: str
    date_to: str
    threads: int = 1

def load_config(config_file: str = "config.json") -> Config:
    path = Path(config_file)
    with path.open() as f:
        data = json.load(f)
    return Config(**data)
