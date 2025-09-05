from utils.helpers import normalize_key

def test_normalize_key_basic():
    assert normalize_key("Date received") == "date_received"
    assert normalize_key("Application number") == "application_number"

def test_normalize_key_symbols():
    assert normalize_key("Objections Received!") == "objections_received"
    assert normalize_key("Decision (Final)") == "decision_final"

def test_normalize_key_strip_and_lower():
    assert normalize_key("  Status  ") == "status"
    assert normalize_key("STATUS") == "status"