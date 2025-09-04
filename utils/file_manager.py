from pathlib import Path
from datetime import datetime

class FileManager:
    def __init__(self, output_dir: str, case_name: str, unique_id: str | None = None):
        self.base_dir = Path(output_dir)
        safe_id = unique_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.case_dir = self.base_dir / f"{case_name}_{safe_id}"
        self.case_dir.mkdir(parents=True, exist_ok=True)

    def get_filename(self, dataset_type: str, extension: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        base_filename = f"{dataset_type}_{timestamp}.{extension}"
        return self.case_dir / base_filename
