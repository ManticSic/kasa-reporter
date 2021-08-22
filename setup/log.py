import logging
import os
import sys
import structlog
import ecs_logging
import setup.configuration

from logging import StreamHandler
from logging.handlers import RotatingFileHandler

log_dir = 'log'
log_file_name = 'kasa-reporter.log'


def __configure_root_logger():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.addHandler(__get_stream_handler())
    logger.addHandler(__get_rotating_file_handler())


def __get_rotating_file_handler():
    return RotatingFileHandler(
        filename=f'{log_dir}/{log_file_name}',
        maxBytes=1024 * 1024,
        backupCount=5
    )


def __get_stream_handler():
    return StreamHandler(sys.stdout)


def __add_configuration(logger, method_name, event_dict):
    event_dict['configuration'] = setup.configuration.get_configuration().__dict__

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


def get_logger():
    return structlog.getLogger('kasa-reporter')
