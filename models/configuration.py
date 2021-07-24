class Configuration:

    def __init__(self, args):
        self.device = args.device
        self.interval = args.interval
        self.device_type = args.type

    def __repr__(self):
        return f'Configuration("{self.device}", "{self.device_type}", "{self.interval}")'
