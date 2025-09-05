import logging
from pathlib import Path
from utils.logger import get_logger

def test_logger_creates_log_file(fs):
    logger = get_logger("TestLogger", "case1")

    handler = logger.handlers[0]
    log_file = handler.baseFilename
    assert "case1" in log_file
    assert log_file.endswith("TestLogger.log")

    logger.info("hello")
    handler.flush()

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "hello" in content

def test_logger_reuses_same_instance(fs):
    fs.create_dir("/fake/logs")
    logger1 = get_logger("TestLogger", "case2")
    logger2 = get_logger("TestLogger", "case2")
    assert logger1 is logger2  # no duplicate handlers