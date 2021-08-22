from kasa import SmartPlug, EmeterStatus
from models.configuration import Configuration


class KasaCollector:

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.device = None

    async def setup(self) -> None:
        self.device = await self.__get_device()

        await self.device.update()

        if not self.device.has_emeter:
            raise Exception(f'{self.configuration.device} has no emeter.')

    async def fetch(self) -> EmeterStatus:
        await self.device.update()

        return await self.device.get_emeter_realtime()

    async def __get_device(self) -> SmartPlug:
        if self.configuration.device_type is 'plug':
            return SmartPlug(self.configuration.device)
        else:
            raise Exception(f'Unsupported device type: {self.configuration.device_type}.')
