import asyncio
from threading import Thread
from typing import Union


class CancellationToken:
    is_cancellation_requested: bool = False

    def request_cancellation(self):
        self.is_cancellation_requested = True


class BackgroundService:
    cancellation_token: Union[CancellationToken, None] = None
    thread: Union[Thread, None] = None

    def __init__(self, job):
        self.job = job

    def start(self):
        if self.cancellation_token is not None:
            raise Exception('Service is already started.')

        self.cancellation_token = CancellationToken()
        self.thread = Thread(target=self.__run)
        self.thread.start()

    def stop(self):
        if self.cancellation_token is None:
            raise Exception('Service is not running.')

        self.cancellation_token.request_cancellation()

    def __run(self):
        asyncio.run(self.__job())

    async def __job(self):
        if self.job is None:
            raise Exception('No job defined.')

        await self.job()
