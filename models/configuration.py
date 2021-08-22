class Configuration:

    def __init__(self, args):
        self.device = args.device
        self.interval = args.interval
        self.device_type = args.type
        self.logstash_host = args.logstash_host
        self.logstash_port = args.logstash_port
