import json
import pandas as pd
from utils.file_manager import FileManager
from utils.results_writer import ResultsWriter

def sample_results():
    return [
        {"id": "1", "name": "Alice"},
        {"id": "2", "name": "Bob"},
    ]

def test_save_all_creates_all_files(fs):
    fs.create_dir("/fake/out")
    fm = FileManager("/fake/out", "case", "id")
    writer = ResultsWriter(fm)

    results = [{
        "id": "123", 
        "url": "http://example.com", 
        "date_collected": "today"
    }]
    writer.save_all(results, "results")

    # Verify CSV
    csv_files = list(fm.case_dir.glob("results_*.csv"))
    assert csv_files, "CSV file not created"

    # Verify JSON
    json_files = list(fm.case_dir.glob("results_*.json"))
    assert json_files
    data = json.loads(open(json_files[0], encoding="utf-8").read())
    assert data[0]["id"] == "123"

    # Verify XLSX
    xlsx_files = list(fm.case_dir.glob("results_*.xlsx"))
    assert xlsx_files
    df = pd.read_excel(xlsx_files[0])
    assert "id" in df.columns
