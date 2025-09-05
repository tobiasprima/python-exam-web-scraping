import re
from utils.file_manager import FileManager

def test_file_manager_creates_case_dir(fs):
    output_dir = "/fake/out"
    fs.create_dir(output_dir)

    fm = FileManager(output_dir, "case_name", "123")
    assert fm.case_dir.exists()
    assert re.match(r"case_name_123$", fm.case_dir.name)
    
def test_get_filename_returns_path(fs):
    output_dir = "/fake/out"
    fs.create_dir(output_dir)

    fm = FileManager(output_dir, "case", "id")
    path = fm.get_filename("results", "csv")

    assert path.parent == fm.case_dir
    assert path.suffix == ".csv"
    assert str(path).startswith(str(fm.case_dir))
