import asyncio

from argparse import ArgumentParser
from time import sleep

from collecting.kasa import KasaCollector
from models.configuration import Configuration

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

    print(f'{repr(configuration)}')

    print(f'Start fetching emeter data for {configuration.device} as {configuration.device_type} in {configuration.interval}s interval.')
    collector = KasaCollector(configuration)
    await collector.setup()

    while True:
        data = await collector.fetch()
        print(f'{data}')
        sleep(configuration.interval)


if __name__ == '__main__':
    asyncio.run(main())
