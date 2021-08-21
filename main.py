import asyncio
import structlog
import ecs_logging

from argparse import ArgumentParser
from time import sleep

from collecting.kasa import KasaCollector
from models.configuration import Configuration

structlog.configure(
    processors=[ecs_logging.StructlogFormatter()],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

parser = ArgumentParser()

# device ip or hostname
parser.add_argument(
    '-d', '--device',
    type=str,
    required=True,
)

# device type
parser.add_argument(
    '-t', '--type',
    type=str,
    choices=['plug'],
    default='plug'
)

# fetch interval in seconds
parser.add_argument(
    '-i', '--interval',
    type=int,
    default=5,
    required=False
)


async def main():
    args = parser.parse_args()
    configuration = Configuration(args)

    logger = structlog.get_logger("kasa-reporter")
    logger = logger.bind(**{
        'configuration': {
            'device': configuration.device,
            'device_type': configuration.device_type,
            'interval': configuration.interval,
        },
    })

    # print(f'Start fetching emeter data for {configuration.device} as {configuration.device_type} in {configuration.interval}s interval.')
    logger.info('Start fetching data.')
    collector = KasaCollector(configuration)
    await collector.setup()

    while True:
        data = await collector.fetch()
        logger.info('Successfully fetched data.', data=data)
        sleep(configuration.interval)


if __name__ == '__main__':
    asyncio.run(main())
