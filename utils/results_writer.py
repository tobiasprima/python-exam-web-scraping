import csv
import json
import pandas as pd
from typing import Any
from utils.file_manager import FileManager

class ResultsWriter:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

    def save_all(self, results: list[dict[str, Any]], dataset_type: str) -> None:
        if not results:
            return
        keys = sorted({k for row in results for k in row.keys()})
        self._save_csv(results, dataset_type, keys)
        self._save_json(results, dataset_type)
        self._save_xlsx(results, dataset_type)

    def _save_csv(self, results: list[dict[str, Any]], dataset_type: str, keys: list[str]) -> None:
        path = self.file_manager.get_filename(dataset_type, "csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)

    def _save_json(self, results: list[dict[str, Any]], dataset_type: str) -> None:
        path = self.file_manager.get_filename(dataset_type, "json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    def _save_xlsx(self, results: list[dict[str, Any]], dataset_type: str) -> None:
        path = self.file_manager.get_filename(dataset_type, "xlsx")
        df = pd.DataFrame(results)
        df.to_excel(path, index=False)
