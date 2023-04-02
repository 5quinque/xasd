"""
xasd_downloader

Usage:
    xasd_downloader [--consumers=CONSUMERS] [options]

Options:
    --consumers=CONSUMERS           Number of consumers that will download torrents asynchronously [default: 2]
    --log-level=LEVEL               Set logger level, one of DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
"""

import asyncio
import logging
import json
from docopt import docopt
from typing import Optional

import aio_pika

from xasd.abc import AbstractWorker
from xasd.database.crud import XasdDB
from xasd.database.session import Session
from xasd.downloader.torrent import (
    create_lt_session,
    download,
    get_displayname,
    get_infohash,
)
from xasd.utils import setup_logging

logger = logging.getLogger(__name__)


class Downloader(AbstractWorker):
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
            _amqp_url (str): The AMQP URI to use for connecting to the broker.
            lt_session (lt.session): The libtorrent session.
            lt_queue (list): The download queue for libtorrent.
            running (bool): A flag indicating whether the application is running or not.
        """
        self.download_path = download_path
        self.amqp_complete_queue = "download_complete"
        self.amqp_retry_queue = "download_retry"

        # create a session
        self.lt_session = create_lt_session()
        # set session settings
        self.lt_session.listen_on(6881, 6891)
        self.lt_queue = []

        session = Session()
        self.db = XasdDB(session=session.get_session())

        super().__init__(
            producer_method="amqp", amqp_url=amqp_url, amqp_consume_queue="download"
        )

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
            logger.info(f"Consumer {name} got message <{message.delivery_tag}>")

            async with message.process():
                logger.info(f"Processing message <{message.delivery_tag}>")
                message_dict = json.loads(message.body)

                # check if the infohash is in the database already
                infohash = get_infohash(message_dict["magnet_uri"])
                if not self.db.add_magnet(infohash):
                    logger.info(f"Info hash {infohash} already in database, skipping")
                    asyncio_queue.task_done()
                    continue

                download_success = await download(
                    self.lt_session,
                    message_dict["magnet_uri"],
                    download_path=self.download_path,
                )
                dn = get_displayname(message_dict["magnet_uri"])
                logger.info(f"Downloading {dn}")

                if download_success:
                    logger.info(f"Successfully downloaded {dn}")
                    message_dict["download_path"] = self.download_path
                    await self.publish_message(
                        self.amqp_complete_queue, json.dumps(message_dict)
                    )
                else:
                    logger.info(f"Failed to download {dn}")
                    await self.publish_message(self.amqp_retry_queue, message.body)

                logger.info(f"Finished processing message for {dn}")
                asyncio_queue.task_done()

    async def publish_message(self, queue_name: str, message_body: str):
        """
        Publishes a message to a queue on a RabbitMQ server.

        Args:
            queue_name (str): The name of the queue to publish the message to.
            message_body (str): The body of the message to publish.
        """
        # connection = await aio_pika.connect_robust(self._amqp_url)

        # async with connection:
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

    downloader = Downloader()
    asyncio.run(downloader.watch(opts))


if __name__ == "__main__":
    main()
