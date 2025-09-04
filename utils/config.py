import json
from pydantic import BaseModel
from pathlib import Path

class Config(BaseModel):
    output_dir: str
    csv_path: str
    csv_delimiter: str = ","
    threads: int = 1
    contexts_per_browser: int = 5
    headless: bool = True

def load_config(config_file: str = "config.json") -> Config:
    path = Path(config_file)
    with path.open() as f:
        data = json.load(f)
    return Config(**data)
