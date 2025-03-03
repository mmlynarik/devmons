import logging
import os
import sys


def get_logger(name=None, level: int | None = None):
    logger = logging.getLogger(name)

    if level is None:
        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
        level = logging.getLevelName(log_level)

        if not isinstance(level, int):
            print(
                f"Unknown log level: {log_level}, fallback to INFO",
                file=sys.stderr,
            )
            level = 20

    logger.setLevel(level)

    return logger
