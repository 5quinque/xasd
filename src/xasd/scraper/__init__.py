"""
xasd_scraper

asyncronous daemon that will scrape urls from an asyncio queue

Usage:
    xasd_scraper [--concurrency=AMOUNT] [options]

Options:
    --concurrency=AMOUNT           Number of concurrent URLs to scrape at a time [default: 2]
    --log-level=LEVEL              Set logger level, one of DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
"""


import asyncio
import logging
import os
from datetime import datetime
from docopt import docopt
from typing import Optional

import aio_pika

from xasd.utils import setup_logging

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(
        self,
        amqp_url: Optional[str] = None,
        amqp_publish_queue: Optional[str] = None,
    ):
        """
        Abstract worker class.

        Args:
            amqp_uri (str, optional): The AMQP URI to use for connecting to the broker.
            amqp_consume_queue (str, optional): The name of the AMQP queue to consume from.

        Attributes:
            _amqp_url (str): The AMQP connection URI.
            amqp_publish_queue (str): The name of the AMQP queue to publish links.
            running (bool): A flag indicating whether the application is running or not.
        """
        self._amqp_url = amqp_url
        if self._amqp_url is None:
            self._amqp_url = os.environ.get("AMQP_URL")
        self.amqp_publish_queue = amqp_publish_queue

        self.running = True

        self.__amqp = None

        # Dictionary containing the base urls for each site and last time we scraped it
        self.base_urls = {
            "url1": None,
            "url2": None,
            "url3": None,
            "url4": None,
            "url5": None,
            "url6": None,
            "url7": None,
        }

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
        producer = asyncio.create_task(self.producer(asyncio_queue))
        consumers = [
            asyncio.create_task(self.consume(n, asyncio_queue))
            for n in range(int(opts["--concurrency"]))
        ]
        await asyncio.gather(producer)
        await asyncio_queue.join()  # Implicitly awaits consumers, too
        for c in consumers:
            c.cancel()

    async def producer(self, asyncio_queue: asyncio.Queue) -> None:
        while self.running:
            for base_url in self.base_urls:
                if (
                    not self.base_urls.get(base_url)
                    or (datetime.now() - self.base_urls[base_url]).total_seconds()
                    > 86400
                ):
                    await asyncio_queue.put(base_url)
                    self.base_urls[base_url] = datetime.now()

            await asyncio.sleep(10)

    async def consume(self, name: int, asyncio_queue: asyncio.Queue) -> None:
        """
        Consumes messages from the asyncio queue and processes them.

        Args:
            name (int): The name/id of the consumer.
            asyncio_queue (asyncio.Queue): The queue from which messages will be consumed.

        Returns: None
        """
        consumer_log_prefix = f"Consumer <{name}>"
        logger.info(f"{consumer_log_prefix} Warming up")
        while True:
            item = await asyncio_queue.get()
            logger.info(f"{consumer_log_prefix} got element <{item}>")

            asyncio_queue.task_done()

            logger.info(f"{consumer_log_prefix} Finished processing item {item}")

    async def publish_message(self, queue_name: str, message_body: str):
        """
        Publishes a message to a queue on a RabbitMQ server.

        Args:
            queue_name (str): The name of the queue to publish the message to.
            message_body (str): The body of the message to publish.
        """
        connection = await self._AbstractWorker__amqp_connection
        channel = await connection.channel()

        message = aio_pika.Message(
            message_body.encode("utf-8"),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        # Sending the message
        await channel.default_exchange.publish(
            message,
            routing_key=queue_name,
        )


def main():
    opts = docopt(__doc__)

    setup_logging(opts)

    scraper = Scraper()
    asyncio.run(scraper.watch(opts))


if __name__ == "__main__":
    main()
