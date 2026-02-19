import logging
import sys


def setup_logger(name: str = "daimon", level: int = logging.INFO) -> logging.Logger:
    """
    Create and configure a simple console logger.

    Args:
        name: Logger name (usually your package name)
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger