import logging


def get_logger(name: str, level: int | None = None):
    logger = logging.getLogger(name)

    if level is None:
        level = 20

    logger.setLevel(level)

    return logger
