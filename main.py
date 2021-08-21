import asyncio
import sys

import structlog
import ecs_logging

from argparse import ArgumentParser
from time import sleep

from collecting.kasa import KasaCollector
from models.configuration import Configuration

# configure logger
structlog.configure(
    processors=[ecs_logging.StructlogFormatter()],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)
__logger = structlog.get_logger("kasa-reporter")

# configure argument parser
parser = ArgumentParser()

parser.add_argument('-d', '--device', type=str, required=True)  # device ip or hostname
parser.add_argument('-t', '--type', type=str, choices=['plug'], default='plug')  # device type
parser.add_argument('-i', '--interval', type=int, default=5, required=False)  # fetch interval in seconds


async def main():
    args = parser.parse_args()
    configuration = Configuration(args)

    logger = __logger.bind(**{
        'configuration': {
            'device': configuration.device,
            'device_type': configuration.device_type,
            'interval': configuration.interval,
        },
    })

    logger.info('Start fetching data.')
    collector = KasaCollector(configuration)
    await collector.setup()

    while True:
        data = await collector.fetch()
        logger.info('Successfully fetched data.', data=data)
        sleep(configuration.interval)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        __logger.info('Application shutdown requested by interruption.')
        sys.exit(0)
    except Exception as e:
        __logger.fatal('Something terrible happened!', exception=e)
        sys.exit(1)
