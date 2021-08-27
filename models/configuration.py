class Configuration:

    def __init__(self, args):
        self.fetch_interval = args.fetch_interval
        self.discover_interval = args.discover_interval
        self.logstash_host = args.logstash_host
        self.logstash_port = args.logstash_port
