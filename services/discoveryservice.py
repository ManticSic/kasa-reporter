from typing import List
from kasa import SmartDevice
from kasa import Discover
from time import sleep

from models.SmartDeviceSpare import SmartDeviceSpare
from services.backgroundservice import BackgroundService
from setup.log import get_logger

logger = get_logger('DiscoveryService')


class DiscoveryService(BackgroundService):
    devices: List[SmartDevice] = []

    def __init__(self):
        super().__init__(self.__job_implementation)

    async def __job_implementation(self):
        while not self.cancellation_token.is_cancellation_requested:
            result = await Discover.discover()

            device_dict = dict(filter(lambda device: device[1].has_emeter, result.items()))
            self.devices = list(map(lambda device: device[1], device_dict.items()))

            devices_spare = list(map(lambda device: SmartDeviceSpare(device).__dict__, self.devices))
            logger.info(f'Devices discovered.', devices=devices_spare)

            sleep(10)

        self.cancellation_token = None

    def get_devices(self):
        return self.devices
