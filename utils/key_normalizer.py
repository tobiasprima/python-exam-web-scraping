import re

def normalize_key(key: str) -> str:
    """Convert field names to snake_case with no caps."""
    key = key.strip().lower()
    key = re.sub(r"[^a-z0-9]+", "_", key)
    key = re.sub(r"_+", "_", key)
    return key.strip("_")
