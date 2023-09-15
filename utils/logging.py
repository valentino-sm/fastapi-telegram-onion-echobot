# pyright: basic

import logging
import sys
from logging import Logger as LoggingLogger
from typing import Any

from utils.settings import settings


class Logger:
    loggers: dict[str, LoggingLogger] = dict()
    level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(format="%(levelname)s: %(name)s: %(message)s")

    @classmethod
    def _log(cls, level: int, message: Any) -> None:
        module_name = sys._getframe(2).f_globals["__name__"]
        if not (logger := cls.loggers.get(module_name)):
            logger = logging.getLogger(module_name)
            cls.loggers[module_name] = logger
            logger.setLevel(cls.level)
        logger.log(level, message)

    def debug(self, message: Any) -> None:
        self._log(logging.DEBUG, message)

    def info(self, message: Any) -> None:
        self._log(logging.INFO, message)

    def warning(self, message: Any) -> None:
        self._log(logging.WARNING, message)

    def error(self, message: Any) -> None:
        self._log(logging.ERROR, message)


logger = Logger()
