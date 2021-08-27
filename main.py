import asyncio
import sys
import setup.log
import setup.configuration
from services.discoveryservice import DiscoveryService
from services.emeterservice import EmeterService

configuration = setup.configuration.get_configuration()
logger = setup.log.get_logger('main')

discovery_service = DiscoveryService()
emeter_service = EmeterService(discovery_service)


async def main() -> None:
    logger.info('Start fetching data.')

    discovery_service.start()
    emeter_service.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        logger.info('Application shutdown requested by interruption.')
        sys.exit(0)
    except Exception as e:
        logger.fatal('Something terrible happened!', exception=e)
        sys.exit(1)
