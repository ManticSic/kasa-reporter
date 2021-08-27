from kasa import SmartPlug
from models.configuration import Configuration
from models.customeemterstatus import CustomEmeterStatus


class KasaCollector:

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.device = None

    async def setup(self) -> None:
        self.device = await self.__get_device()

        await self.device.update()

        if not self.device.has_emeter:
            raise Exception(f'{self.configuration.device} has no emeter.')

    async def fetch(self) -> CustomEmeterStatus:
        await self.device.update()

        emeter_status = await self.device.get_emeter_realtime()
        today = self.device.emeter_today
        this_month = self.device.emeter_this_month

        return CustomEmeterStatus(
            emeter_status['voltage_mv'],
            emeter_status['current_ma'],
            emeter_status['power_mw'],
            emeter_status['total_wh'],
            today,
            this_month
        )

    async def __get_device(self) -> SmartPlug:
        if self.configuration.device_type is 'plug':
            return SmartPlug(self.configuration.device)
        else:
            raise Exception(f'Unsupported device type: {self.configuration.device_type}.')
