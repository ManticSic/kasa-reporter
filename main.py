import subprocess
import platform
import asyncio

from argparse import ArgumentParser
from time import sleep
from kasa import SmartPlug
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

    device = get_emeter_device(configuration)
    await device.update()

    if not device.has_emeter:
        raise Exception(f'{configuration.device} has no emeter.')

    print(f'Start fetching emeter data for {configuration.device} as {configuration.device_type} in {configuration.interval}s interval.')

    while True:
        await fetch_emeter_data(device)
        sleep(configuration.interval)


async def fetch_emeter_data(emeter_device):
    await emeter_device.update()
    emeter = await emeter_device.get_emeter_realtime()
    print(f'{emeter}')


def get_emeter_device(configuration):
    if configuration.device_type is 'plug':
        return SmartPlug(configuration.device)
    else:
        raise Exception(f'Unsupported device type: {configuration.device_type}.')


if __name__ == '__main__':
    asyncio.run(main())
