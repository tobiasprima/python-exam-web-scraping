import re
from utils.file_manager import FileManager

def test_file_manager_creates_case_dir(tmp_path):
    fm = FileManager(output_dir=tmp_path, case_name="2025-01-01_to_2025-01-15", unique_id="case123")
    
    # Directory should exist
    assert fm.case_dir.exists()
    assert re.match(r".*2025-01-01_to_2025-01-15_case123$", str(fm.case_dir))

def test_get_filename_returns_unique_path(tmp_path):
    fm = FileManager(output_dir=tmp_path, case_name="case", unique_id="id")
    file1 = fm.get_filename("results", "csv")
    file2 = fm.get_filename("results", "csv")

    # Both should be inside the case_dir
    assert str(fm.case_dir) in str(file1)
    assert str(fm.case_dir) in str(file2)

    # Filenames should have proper extensions
    assert file1.suffix == ".csv"
    assert file2.suffix == ".csv"
