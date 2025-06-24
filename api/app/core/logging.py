"""
Logging configuration for the application.
"""

import logging
import sys
from typing import List
from loguru import logger
from app.core.config import settings


class InterceptHandler(logging.Handler):
    """
    Default handler from examples of loguru documentation.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(
    *,
    log_file: str = "app.log",
    rotation: str = "20 MB",
    retention: str = "1 months",
    format: str = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level: str = "INFO",
    backtrace: bool = True,
    diagnose: bool = False,
    enqueue: bool = False,
    catch: bool = True,
    serialize: bool = False,
    compression: str = None,
    delay: bool = False,
    **kwargs: dict,
) -> None:
    """
    Setup logging configuration.
    """
    # Remove all existing handlers
    logger.remove()

    # Add stdout handler
    logger.add(
        sys.stdout,
        format=format,
        level=level,
        backtrace=backtrace,
        diagnose=diagnose,
        enqueue=enqueue,
        catch=catch,
        serialize=serialize,
        **kwargs,
    )

    # Add file handler
    logger.add(
        log_file,
        rotation=rotation,
        retention=retention,
        format=format,
        level=level,
        backtrace=backtrace,
        diagnose=diagnose,
        enqueue=enqueue,
        catch=catch,
        serialize=serialize,
        compression=compression,
        delay=delay,
        **kwargs,
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Intercept uvicorn logging
    for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]

    return logger
