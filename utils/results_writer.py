import csv
import json
import pandas as pd
from pathlib import Path
from typing import Any
from datetime import datetime

def save_results(results: list[dict[str, Any]], output_dir: str, case_name: str, dataset_type: str, unique_id: str | None = None):
    """
    Save results to CSV, JSON, XLSX in a case-specific folder.
    
    - case_name: typically "date_from_to_date_to"
    - dataset_type: "results" or "details"
    - unique_id: optional extra identifier (e.g., case_id, suburb).
                 If None, falls back to timestamp.
    """
    # Build unique folder name
    safe_id = unique_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    case_dir = Path(output_dir) / f"{case_name}_{safe_id}"
    case_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base_filename = f"{dataset_type}_{timestamp}"

    # Save CSV
    csv_file = case_dir / f"{base_filename }.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "url", "date_collected"])
        writer.writeheader()
        writer.writerows(results)

    # Save JSON
    json_file = case_dir / f"{base_filename }.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Save XLSX
    xlsx_file = case_dir / f"{base_filename }.xlsx"
    df = pd.DataFrame(results)
    df.to_excel(xlsx_file, index=False)