import asyncio
import logging
import os
from abc import ABC, abstractmethod
from typing import Optional

import aio_pika

from xasd.utils.asyncinotifyrecurse import InotifyRecurse, Mask

logger = logging.getLogger(__name__)


class AbstractWorker(ABC):
    def __init__(
        self,
        producer_method: Optional[str] = "inotify",
        amqp_url: Optional[str] = None,
        amqp_consume_queue: Optional[str] = None,
    ):
        """
        Abstract worker class.

        Args:
            amqp_uri (str, optional): The AMQP URI to use for connecting to the broker.
            amqp_consume_queue (str, optional): The name of the AMQP queue to consume from.

        Attributes:
            _amqp_url (str): The AMQP connection URI.
            amqp_consume_queue (str): The name of the AMQP queue to consume from.
            db (XasdDB): An instance of the XasdDB class for storing and retrieving data.
            producer_method (str): tbd
            running (bool): A flag indicating whether the application is running or not.
        """
        self._amqp_url = amqp_url
        if self._amqp_url is None:
            self._amqp_url = os.environ.get("AMQP_URL")
        self.amqp_consume_queue = amqp_consume_queue

        self.producer_method = producer_method

        self.running = True

        self.__amqp = None

    @property
    async def __amqp_connection(self):
        if self.__amqp:
            return self.__amqp

        connection_attempts = 0
        while True:
            try:
                connection_attempts += 1
                logger.info(f"[{connection_attempts}] Attempting to connect to AMQP")
                self.__amqp = await aio_pika.connect_robust(self._amqp_url, timeout=60)
                logger.info(f"[{connection_attempts}] Successfully connected to AMQP")
                return self.__amqp
            except ConnectionError as e:
                if connection_attempts == 300:
                    logger.error(
                        f"Failed to connect to AMQP after {connection_attempts} attempts. Exiting."
                    )
                    raise e
                logger.warning(f"Failed to connect to AMQP. Retrying in 5 seconds.")
                await asyncio.sleep(5)

    async def watch(self, opts: dict):
        """
        Create a producer instance (using either inotify or amqp) to send tasks to an asysncio queue
        That is then processed by consumers

        Args:
            opts (dict): A dictionary of options specifying the number of consumers to use.
        """
        asyncio_queue = asyncio.Queue()
        if self.producer_method == "inotify":
            producer = asyncio.create_task(
                self.inotify_producer(asyncio_queue, path=opts["<dir>"])
            )
        else:
            producer = asyncio.create_task(self.amqp_producer(asyncio_queue))

        consumers = [
            asyncio.create_task(self.consume(n, asyncio_queue))
            for n in range(int(opts["--consumers"]))
        ]
        await asyncio.gather(producer)
        await asyncio_queue.join()  # Implicitly awaits consumers, too
        for c in consumers:
            c.cancel()

    async def amqp_producer(self, asyncio_queue: asyncio.Queue) -> None:
        """
        Asynchronously consume messages from a RabbitMQ queue and put them in an asyncio queue.

        Args:
        asyncio_queue (asyncio.Queue): An asyncio queue to put the messages in.

        Returns:
        None
        """
        logger.info("amqp_producer start")

        connection = await self.__amqp_connection

        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.amqp_consume_queue)

            await queue.consume(asyncio_queue.put)

            while self.running:
                logger.debug(f"Queue size: {asyncio_queue.qsize()}")

                await asyncio.sleep(1)

    async def inotify_producer(self, asyncio_queue: asyncio.Queue, path: str) -> None:
        """
        A producer function that watches the given path.

        This function monitors the given `path` for file changes, and places the changed file paths in the provided `asyncio_queue`.
        If a new directory is created,
        it will be added to the watch list.

        Args:
        - asyncio_queue (asyncio.Queue): An asyncio queue to hold the changed file paths.
        - path (str): The path to monitor for changes.

        Returns:
        None
        """
        with InotifyRecurse(
            path, mask=Mask.MOVED_TO | Mask.CLOSE_WRITE | Mask.CREATE
        ) as inotify:
            logger.info(f"Watching {path} for new files")
            async for event in inotify:
                local_filepath = str(event.path)

                # Watch newly created dirs
                if (
                    Mask.CREATE in event.mask
                    and event.path is not None
                    and event.path.is_dir()
                ):
                    logger.info(f"Watching {event.path} for new files")
                    inotify.load_tree(event.path)

                if (
                    (Mask.MOVED_TO | Mask.CLOSE_WRITE) & event.mask
                    and event.path is not None
                    and event.path.is_file()
                ):
                    logger.info(f"New file: {local_filepath}")
                    await asyncio_queue.put(local_filepath)

    @abstractmethod
    async def consume(self, name: int, asyncio_queue: asyncio.Queue) -> None:
        """
        Consumes messages from the asyncio queue and processes them.

        Args:
            name (int): The name/id of the consumer.
            asyncio_queue (asyncio.Queue): The queue from which messages will be consumed.
        """
        raise NotImplementedError("[TODO] write a better not implemented message here")
