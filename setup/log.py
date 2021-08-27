import json
import logging
import os
import socket
import sys
import time

import structlog
import ecs_logging
import setup.configuration

from typing import Any
from structlog.types import EventDict
from logging import StreamHandler, Handler, LogRecord
from logging.handlers import RotatingFileHandler, SocketHandler

configuration = setup.configuration.get_configuration()

log_dir = 'log'
log_file_name = 'kasa-reporter.log'


class LogstashTcpHandler(SocketHandler):
    def __init__(self, host: str, port: int):
        SocketHandler.__init__(self, host, port)

    def emit(self, record: LogRecord) -> None:
        try:
            s = self.__make_json(record)
            self.send(s)
        except Exception:
            self.handleError(record)

    def __make_json(self, record: LogRecord):
        s = f'{record.getMessage()}\n'.encode('utf-8')
        return s


def __configure_root_logger() -> None:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.addHandler(__get_stream_handler())
    logger.addHandler(__get_rotating_file_handler())
    logger.addHandler(__get_logstash_handler())


def __get_rotating_file_handler() -> logging.Handler:
    return RotatingFileHandler(
        filename=f'{log_dir}/{log_file_name}',
        maxBytes=1024 * 1024,
        backupCount=5
    )


def __get_stream_handler() -> logging.Handler:
    return StreamHandler(sys.stdout)


def __get_logstash_handler() -> logging.Handler:
    return LogstashTcpHandler(configuration.logstash_host, configuration.logstash_port)


def __add_configuration(logger: logging.Logger, method_name: str, event_dict: EventDict) -> EventDict:
    event_dict['configuration'] = configuration.__dict__

    return event_dict


__configure_root_logger()
structlog.configure(
    processors=[
        __add_configuration,
        structlog.stdlib.add_logger_name,
        ecs_logging.StructlogFormatter(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
)


def get_logger(name: str) -> Any:
    return structlog.get_logger(name)
