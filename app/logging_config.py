

import logging
import os

from logging.handlers import RotatingFileHandler
from os.path import exists


def setup_logging():
    """
      Configure application-wide logging.
        """

    level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_file = os.getenv("LOG_FILE","./logs/cellmapai.log")

    #ensure that log folder exists

    os.makedirs(os.path.dirname(log_file),exist_ok=True)

    fmt = "%(asctime)s %(levelname)s [%(name)s:%(lineno)d] - %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    # Console handler (prints to stdout)
    handler_console = logging.StreamHandler()
    handler_console.setFormatter(logging.Formatter(fmt, datefmt=datefmt))

    # File handler (with rotation, max 5 MB each, keep 3 backups)
    handler_file = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    handler_file.setFormatter(logging.Formatter(fmt, datefmt=datefmt))

    root = logging.getLogger()
    root.setLevel(level)

    if not root.handlers:
        root.addHandler(handler_console)
        root.addHandler(handler_file)






