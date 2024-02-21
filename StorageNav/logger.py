from __future__ import annotations

import os
import sys
import typing as ty

from loguru import logger


if ty.TYPE_CHECKING:
    from config import Config


try:  # Removing default logger settings
    logger.remove(0)
except ValueError:
    pass

logger.level("TRACE", color="<lk>")  # TRACE - blue
logger.level("DEBUG", color="<w>")  # DEBUG - white
logger.level("INFO", color="<c><bold>")  # INFO - turquoise


def formatter(record) -> str:
    record["extra"]["VERSION"] = os.environ["VERSION"]
    return (
        "<lvl><n>[{level.name} </n></lvl>"
        "<g>{time:YYYY-MM-DD HH:mm:ss.SSS}</g> "
        "<lg>v{extra[VERSION]}</lg>"
        "<lvl><n>]</n></lvl> "
        "<w>{module}.{function}</w>: "
        "<lvl><n>{message}</n></lvl>\n{exception}"
    )


def init_logger(config: Config) -> None:
    logger.add(
        sys.stdout,
        colorize=config.logger.colorize,
        format=formatter,
        level=config.logger.level,
    )

    if config.logger.file:
        logger.add(
            config.logger.file,
            colorize=False,
            format=formatter,
            level=config.logger.level,
        )
