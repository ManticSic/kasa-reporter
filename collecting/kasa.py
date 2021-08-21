from kasa import SmartPlug


class KasaCollector:

    def __init__(self, configuration):
        self.configuration = configuration
        self.device = None

    async def setup(self):
        self.device = await self.__get_device()

        await self.device.update()

        if not self.device.has_emeter:
            raise Exception(f'{self.configuration.device} has no emeter.')

    async def fetch(self):
        await self.device.update()

        return await self.device.get_emeter_realtime()

    async def __get_device(self):
        if self.configuration.device_type is 'plug':
            return SmartPlug(self.configuration.device)
        else:
            raise Exception(f'Unsupported device type: {self.configuration.device_type}.')
