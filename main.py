import asyncio
import sys
import setup.log
import setup.configuration

from time import sleep
from collecting.kasa import KasaCollector

configuration = setup.configuration.get_configuration()
logger = setup.log.get_logger()


async def main() -> None:
    logger.info('Start fetching data.')
    collector = KasaCollector(configuration)
    await collector.setup()

    while True:
        data = await collector.fetch()
        logger.info('Successfully fetched data.', data=data.__dict__)
        sleep(configuration.interval)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        logger.info('Application shutdown requested by interruption.')
        sys.exit(0)
    except Exception as e:
        logger.fatal('Something terrible happened!', exception=e)
        sys.exit(1)
