"""
xasd_uploader

Usage:
    xasd_uploader watch [<dir>] [--consumers=CONSUMERS] [--producer=[inotify|amqp]] [options]
    xasd_uploader <path> [options]

Options:
    --consumers=CONSUMERS           Number of consumers that will upload files asynchronously [default: 2]
    --log-level=LEVEL               Set logger level, one of DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
    --producer=[inotify|amqp]       Which producer to use to monitor files to upload [default: inotify]
"""

import asyncio
import json
import logging
import os
from docopt import docopt
from pathlib import Path
from typing import Optional

import aio_pika

# import aio_pika.abc

from xasd.uploader.asyncinotifyrecurse import InotifyRecurse, Mask
from xasd.uploader.b2_upload import B2Bucket
from xasd.database.crud import XasdDB
from xasd.uploader.dejavu import file_hash
from xasd.uploader.track_info import track_info
from xasd.uploader import fileinfo

logger = logging.getLogger(__name__)


class Uploader:
    def __init__(
        self, amqp_url: Optional[str] = None, producer_method: Optional[str] = "inotify"
    ):
        """
        A class for uploading songs and storing the information in the database.

        Args:
            amqp_uri (str, optional): The AMQP URI to use for connecting to the broker.

        Attributes:
            _amqp_uri (str): The AMQP connection URI.
            amqp_consume_queue (str): The name of the AMQP queue to consume from.
            b2 (B2Bucket): An instance of the B2Bucket class for interacting with Backblaze B2 storage.
            db (XasdDB): An instance of the XasdDB class for storing and retrieving data.
            producer_method (str): tbd
            running (bool): A flag indicating whether the application is running or not.
        """
        self._amqp_url = amqp_url
        if self._amqp_url is None:
            self._amqp_url = os.environ.get("AMQP_URL")
        self.amqp_consume_queue = "download_complete"

        self.b2 = B2Bucket(
            os.environ.get("B2_BUCKETNAME"),
            os.environ.get("B2_KEY"),
            os.environ.get("B2_SECRET"),
        )

        self.db = XasdDB()

        self.producer_method = producer_method

        self.running = True

    def _pre_upload_tasks(
        self, local_filepath: str, cloud_filepath: str, mimetype: str
    ):
        hash = file_hash(self.db, local_filepath, mimetype)
        if hash is False:
            return False

        info = track_info(local_filepath)
        info["hash"] = hash
        self.db.insert_file(cloud_filepath, info)

        return True

    async def upload(self, path: str):
        logger.debug(f"Processing <{path}>")
        p = Path(path)

        if p.is_dir():
            for x in p.iterdir():
                await self.upload(str(x))
        elif p.is_file():
            mimetype = fileinfo.mimetype(path)

            logger.info(f"[{mimetype}]<{path}> needs uploading")

            cloud_filepath = fileinfo.generate_uuid_filename()
            if self._pre_upload_tasks(path, cloud_filepath, mimetype):
                self.b2.upload_file(path, cloud_filepath)
            else:
                logger.info(f"Pre upload tasks failed for <{path}>, not uploading")
        else:
            logger.info(f"<{path}> Not found")

    async def watch(self, opts: dict):
        """
        Watch either a directory or AMQP queue and upload files to a b2 bucket and insert it into the database.

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

    async def consume(self, name: int, asyncio_queue: asyncio.Queue) -> None:
        """
        Consumes messages from the asyncio queue and processes them.

        Args:
            name (int): The name/id of the consumer.
            asyncio_queue (asyncio.Queue): The queue from which messages will be consumed.
        """
        logger.debug(f"Warming up consumer <{name}>")
        while True:
            item = await asyncio_queue.get()

            if self.producer_method == "amqp":
                message_dict = json.loads(item.body)
                local_filepath = message_dict["download_path"]
                # loop over the path and upload each file

            # local_filepath = await asyncio_queue.get()
            logger.debug(f"Consumer {name} got element <{item}>")

            await self.upload(local_filepath)
            asyncio_queue.task_done()

            logger.info(
                f"Finished processing item <{local_filepath}>"  # , sending ack"
            )

            if self.producer_method == "amqp":
                await item.ack()

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
            async for event in inotify:
                local_filepath = str(event.path)

                # Watch newly created dirs
                if (
                    Mask.CREATE in event.mask
                    and event.path is not None
                    and event.path.is_dir()
                ):
                    inotify.load_tree(event.path)

                if (
                    (Mask.MOVED_TO | Mask.CLOSE_WRITE) & event.mask
                    and event.path is not None
                    and event.path.is_file()
                ):
                    await asyncio_queue.put(local_filepath)

    async def amqp_producer(self, asyncio_queue: asyncio.Queue) -> None:
        """
        Asynchronously consume messages from a RabbitMQ queue and put them in an asyncio queue.

        Args:
        asyncio_queue (asyncio.Queue): An asyncio queue to put the messages in.

        Returns:
        None
        """
        connection = await aio_pika.connect_robust(self._amqp_uri)

        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.amqp_consume_queue)

            await queue.consume(asyncio_queue.put)

            while self.running:
                logger.debug(f"Queue size: {asyncio_queue.qsize()}")

                await asyncio.sleep(1)


def setup_logging(opts):
    logging.basicConfig(
        level=opts["--log-level"],
        format="[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s",
        force=True,
    )


def main():
    opts = docopt(__doc__)

    if opts["--producer"] not in ["inotify", "amqp"]:
        raise ValueError("--producer argument must be either 'inotify' or 'amqp'")
    if opts["--producer"] == "inotify" and opts["<dir>"] is None:
        print(__doc__)
        raise ValueError("If using inotify producer, you need to provide a directory.")

    setup_logging(opts)

    uploader = Uploader(producer_method=opts["--producer"])

    if opts["watch"]:
        asyncio.run(uploader.watch(opts))
    else:
        # Will only upload synchronously
        asyncio.run(uploader.upload(opts["<path>"]))


if __name__ == "__main__":
    main()
