from kasa import SmartDevice


class SmartDeviceSpare:
    def __init__(self, device: SmartDevice):
        self.host = device.host
        self.device_id = device.device_id
        self.alias = device.alias

    def __repr__(self):
        return self.__dict__.__repr__()
