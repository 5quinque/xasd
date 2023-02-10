"""
xasd_downloader

Usage:
    xasd_downloader [--consumers=CONSUMERS] [options]

Options:
    --consumers=CONSUMERS           Number of consumers that will download torrents asynchronously [default: 2]
    --log-level=LEVEL               Set logger level, one of DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
"""

import asyncio
import base64
import logging
import json
import os
import urllib.parse
from docopt import docopt
from typing import Optional

import aio_pika
import aio_pika.abc

from xasd.downloader.torrent import create_lt_session, download

logger = logging.getLogger(__name__)


class Downloader:
    def __init__(
        self,
        download_path: Optional[str] = "./downloads",
        amqp_url: Optional[str] = None,
    ):
        """
        Initialize a new instance of the class.

        Args:
            download_path (str, optional): Where to download files. Defaults to ./downloads
            amqp_uri (str, optional): The AMQP URI to use for connecting to the broker.

        Attributes:
            download_path (str): Path to save downloads
            _amqp_uri (str): The AMQP URI to use for connecting to the broker.
            lt_session (lt.session): The libtorrent session.
            lt_queue (list): The download queue for libtorrent.
            running (bool): A flag indicating whether the application is running or not.
        """
        self.download_path = download_path
        self._amqp_url = amqp_url
        if self._amqp_url is None:
            self._amqp_url = os.environ.get("AMQP_URL")

        self.amqp_consume_queue = "download"
        self.amqp_complete_queue = "download_complete"
        self.amqp_retry_queue = "download_retry"

        # create a session
        self.lt_session = create_lt_session()
        # set session settings
        self.lt_session.listen_on(6881, 6891)
        self.lt_queue = []

        self.running = True

    def parse_magnet_link(self, magnet_link):
        """
        Parse the magnet link and return the hexadecimal representation of the BitTorrent infohash.

        Args:
        magnet_link (str): The magnet link to parse.

        Returns:
        str: The hexadecimal representation of the BitTorrent infohash if the magnet link is valid, None otherwise.
        """
        parsed = urllib.parse.urlparse(magnet_link)
        params = urllib.parse.parse_qs(parsed.query)
        if "xt" in params:
            xt = params["xt"][0]
            if xt.startswith("urn:btih:"):
                b32_hash = xt[9:]
                decoded_hash = base64.b32decode(b32_hash)
                hex_hash = decoded_hash.hex()
                return hex_hash
        return None

    async def watch(self, opts: dict):
        """
        Watch the amqp download queue and download new torrents as they become available.

        Args:
        opts (dict): A dictionary of options specifying the number of consumers to use.
        """
        asyncio_queue = asyncio.Queue()
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

        connection = await aio_pika.connect_robust(self._amqp_uri)

        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.amqp_consume_queue)

            await queue.consume(asyncio_queue.put)

            while self.running:
                logger.debug(f"Queue size: {asyncio_queue.qsize()}")

                await asyncio.sleep(1)

    async def consume(self, name: int, asyncio_queue: asyncio.Queue) -> None:
        """
        Consumes messages from the asyncio queue and processes them.

        Args:
            name (int): The name/id of the consumer.
            asyncio_queue (asyncio.Queue): The queue from which messages will be consumed.
        """
        logger.info(f"Warming up consumer <{name}>")
        while True:
            message = await asyncio_queue.get()
            logger.info(
                f"Consumer {name} got message <{message.delivery_tag}>, body: <{message.body}>"
            )
            message_dict = json.loads(message.body)
            # await asyncio.sleep(2)
            download_success = await download(
                message_dict["magnet_uri"], download_path=self.download_path
            )

            if download_success:
                logger.info(f"Successfully downloaded {message_dict['name']}")
                message_dict["download_path"] = self.download_path
                self.publish_complete(
                    self.amqp_complete_queue, json.dumps(message_dict)
                )
            else:
                logger.info(f"Failed to download {message_dict['name']}")
                self.publish_complete(self.amqp_retry_queue, message.body)

            logger.info(
                f"Finished processing message <{message.delivery_tag}>, sending ack"
            )
            await message.ack()
            asyncio_queue.task_done()

    async def publish_complete(self, queue, message_body):
        """
        Publishes a message to a queue on a RabbitMQ server.

        Args:
            queue (str): The name of the queue to publish the message to.
            message_body (str): The body of the message to publish.
        """
        connection = await aio_pika.connect_robust(self._amqp_uri)

        async with connection:
            # Creating a channel
            channel = await connection.channel()

            message = aio_pika.Message(
                message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )

            await channel.default_exchange.publish(
                message,
                routing_key=queue,
            )


def setup_logging(opts):
    logging.basicConfig(
        level=opts["--log-level"],
        format="[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s",
        force=True,
    )


def main():
    opts = docopt(__doc__)

    setup_logging(opts)

    downloader = Downloader()
    asyncio.run(downloader.watch(opts))


if __name__ == "__main__":
    main()
