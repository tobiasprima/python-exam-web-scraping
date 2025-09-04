import csv
import json
import pandas as pd
from pathlib import Path
from typing import Any

def save_results(results: list[dict[str, Any]], output_dir: str, filename: str):
    case_dir = Path(output_dir) / filename
    case_dir.mkdir(parents=True, exist_ok=True)

    # Save CSV
    csv_file = case_dir / f"{filename}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "url", "date_collected"])
        writer.writeheader()
        writer.writerows(results)

    # Save JSON
    json_file = case_dir / f"{filename}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Save XLSX
    xlsx_file = case_dir / f"{filename}.xlsx"
    df = pd.DataFrame(results)
    df.to_excel(xlsx_file, index=False)