# tests/test_logger_standalone.py
"""
Standalone test: verify that setup_logging() creates a file handler and writes logs.

This does NOT depend on FastAPI app.main.
We defensively remove any pre-existing root handlers (pytest adds some),
so our setup_logging() can install the expected handlers reliably.
"""

import logging
from pathlib import Path
from app.logging_config import setup_logging


def test_logger_writes_file(tmp_path, monkeypatch):
    #temporary file for log
    log_file = tmp_path / "standalone_test.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    # Remove any pre-existing handlers on the root logger
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)

    # Call setup to add console and rotating file handlers
    setup_logging()

    # Use a test logger and make sure it isn't filtering out DEBUG/INFO
    logger = logging.getLogger("testlogger")
    logger.setLevel(logging.DEBUG)
    logger.debug("debug message")
    logger.info("info message")

    # Flush root handlers (handlers are attached to root in setup_logging)
    for h in logging.getLogger().handlers:
        if hasattr(h, "flush"):
            h.flush()

    # Assert file exists and contains the messages
    assert log_file.exists(), f"log file {log_file} not created"
    content = log_file.read_text(encoding="utf-8")
    assert "debug message" in content or "info message" in content
