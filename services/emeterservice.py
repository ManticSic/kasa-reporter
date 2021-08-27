from time import sleep
from kasa import SmartDevice
from models.SmartDeviceSpare import SmartDeviceSpare
from models.customeemterstatus import CustomEmeterStatus
from services.backgroundservice import BackgroundService
from services.discoveryservice import DiscoveryService
from setup.log import get_logger

logger = get_logger('EmeterService')


class EmeterService(BackgroundService):
    def __init__(self, discovery_service: DiscoveryService):
        super().__init__(self.__job_implementation)
        self.discovery_service = discovery_service

    async def __job_implementation(self):
        while not self.cancellation_token.is_cancellation_requested:
            devices = self.discovery_service.devices
            for device in devices:
                try:
                    data = await self.__fetch(device)
                    logger.info('Fetched data.', data=data.__dict__, device=SmartDeviceSpare(device).__dict__)
                except Exception:
                    # todo log and format exception
                    logger.error('Failed to fetch data.', device=SmartDeviceSpare(device).__dict__)
            sleep(5)

        self.cancellation_token = None

    async def __fetch(self, device: SmartDevice) -> CustomEmeterStatus:
        await device.update()

        emeter_status = await device.get_emeter_realtime()
        today = device.emeter_today
        this_month = device.emeter_this_month

        return CustomEmeterStatus(
            emeter_status['voltage_mv'],
            emeter_status['power_mw'],
            emeter_status['current_ma'],
            emeter_status['total_wh'],
            today,
            this_month
        )
