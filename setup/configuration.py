from argparse import ArgumentParser
from models.configuration import Configuration

# configure argument parser
parser = ArgumentParser()

parser.add_argument('-d', '--device', type=str, required=True)  # device ip or hostname
parser.add_argument('-t', '--type', type=str, choices=['plug'], default='plug')  # device type
parser.add_argument('-i', '--interval', type=int, default=5, required=False)  # fetch interval in seconds
parser.add_argument('--logstash-host', type=str, required=True)  # logstash ip or hostname
parser.add_argument('--logstash-port', type=int, default=5000, required=False)  # logstash port

args = parser.parse_args()
configuration = Configuration(args)


def get_configuration() -> Configuration:
    return configuration
