import logging
from typing import Dict, Optional, Union

import colorlog

__all__ = (
    "LOG_LEVELS",
    "setup_logging",
)


LOG_LEVELS = (
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
)

LOG_FORMAT_BASIC = "%(log_color)s%(message)s"
LOG_FORMAT_DETAILED = "%(log_color)s%(asctime)s %(levelname)-8s [%(name)s] %(message)s"

LOG_COLORS = {
    LOG_LEVELS[0]: "cyan",
    LOG_LEVELS[1]: "green",
    LOG_LEVELS[2]: "yellow",
    LOG_LEVELS[3]: "red",
    LOG_LEVELS[4]: "red,bg_white",
}


def setup_logging(
    level: Union[int, str] = logging.WARNING,
    detailed: bool = False,
    log_format: Optional[str] = None,
    log_colors: Dict[str, str] = LOG_COLORS,
):
    log_format = log_format or (LOG_FORMAT_DETAILED if detailed else LOG_FORMAT_BASIC)
    formatter = colorlog.ColoredFormatter(fmt=log_format, log_colors=log_colors)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[log_handler])
