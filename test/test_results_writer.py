import json
import pandas as pd
from utils.file_manager import FileManager
from utils.results_writer import ResultsWriter

def sample_results():
    return [
        {"id": "1", "name": "Alice"},
        {"id": "2", "name": "Bob"},
    ]

def test_save_all_creates_all_files(tmp_path):
    fm = FileManager(output_dir=tmp_path, case_name="case", unique_id="id")
    writer = ResultsWriter(fm)

    results = sample_results()
    writer.save_all(results, "results")

    # Check file existence
    csv_files = list(fm.case_dir.glob("results_*.csv"))
    json_files = list(fm.case_dir.glob("results_*.json"))
    xlsx_files = list(fm.case_dir.glob("results_*.xlsx"))

    assert len(csv_files) == 1
    assert len(json_files) == 1
    assert len(xlsx_files) == 1

    # Check JSON contents
    with open(json_files[0], "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == results

    # Check XLSX contents
    df = pd.read_excel(xlsx_files[0])
    assert list(df.columns) == ["id", "name"]
    assert df.iloc[0]["name"] == "Alice"
