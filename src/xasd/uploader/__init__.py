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
from typing import Any, Optional

from xasd.abc import AbstractWorker
from xasd.uploader.b2_upload import B2Bucket
from xasd.database.crud import XasdDB
from xasd.uploader.dejavu import file_hash
from xasd.uploader.track_info import track_info
from xasd.uploader import fileinfo
from xasd.utils import setup_logging
from xasd.utils.constants import SUPPORTED_MIMETYPES

logger = logging.getLogger(__name__)


class Uploader(AbstractWorker):
    def __init__(
        self, amqp_url: Optional[str] = None, producer_method: Optional[str] = "inotify"
    ):
        """
        A class for uploading songs and storing the information in the database.

        Args:
            amqp_uri (str, optional): The AMQP URI to use for connecting to the broker.

        Attributes:
            _amqp_url (str): The AMQP connection URI.
            amqp_consume_queue (str): The name of the AMQP queue to consume from.
            b2 (B2Bucket): An instance of the B2Bucket class for interacting with Backblaze B2 storage.
            db (XasdDB): An instance of the XasdDB class for storing and retrieving data.
            producer_method (str): tbd
            running (bool): A flag indicating whether the application is running or not.
        """

        self.b2 = B2Bucket(
            os.environ.get("B2_BUCKETNAME"),
            os.environ.get("B2_KEY"),
            os.environ.get("B2_SECRET"),
        )

        self.db = XasdDB()

        super().__init__(
            producer_method=producer_method,
            amqp_url=amqp_url,
            amqp_consume_queue="download_complete",
        )

    def _pre_upload_tasks(
        self, local_filepath: str, cloud_filepath: str, mimetype: str
    ) -> bool:
        if mimetype not in SUPPORTED_MIMETYPES:
            logger.warning(f"{local_filepath} does not have a valid mimetype")
            return False

        hash = file_hash(self.db, local_filepath, mimetype)
        if hash is False:
            logger.warning(f"{local_filepath} already exists in database")
            return False

        info = track_info(local_filepath)
        info["hash"] = hash
        self.db.insert_file(cloud_filepath, info)

        return True

    async def upload(self, path: str) -> None:
        """
        Upload a file to B2 and store the information in the database.

        Args:
            path (str): The path to the file to upload.
        """
        logger.info(f"Processing <{path}>")
        p = Path(path)

        if p.is_dir():
            for x in p.iterdir():
                await self.upload(str(x))
        elif p.is_file():
            mimetype = fileinfo.mimetype(path)

            cloud_filepath = fileinfo.generate_uuid_filename()
            if self._pre_upload_tasks(path, cloud_filepath, mimetype):
                logger.info(f"[{mimetype}]<{path}> uploading...")
                self.b2.upload_file(path, cloud_filepath)
                logger.info(f"[{mimetype}]<{path}> upload complete.")
            else:
                logger.info(f"Pre upload tasks failed for <{path}>, not uploading")
            logger.info(f"removing file {path}")
            p.unlink()
        else:
            logger.info(f"<{path}> Not found")

    async def upload_task(self, item: Any) -> None:
        """
        Make sense of the asynco queue item, if it's from amqp, loop over the dir to upload each relevant file
        else, assume it's a file we've been given from inotify and upload the individual file

        Args:
            item (Any): The item representing a file to be uploaded. If `self.producer_method` is equal to "amqp", `item` should be an instance of `aiormq.Message` and contains a JSON-encoded string with the key "download_path" representing the file path. If `self.producer_method` is not equal to "amqp", `item` should be the file path string.

        Returns: None
        """
        if self.producer_method == "amqp":
            message_dict = json.loads(item.body)
            local_filepath = message_dict["download_path"]
            async with item.process():
                await self.upload(local_filepath)
        else:
            await self.upload(item)

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
            logger.info(f"{consumer_log_prefix} got element <>")

            await self.upload_task(item)

            asyncio_queue.task_done()

            logger.info(f"{consumer_log_prefix} Finished processing item {item}")


def main() -> None:
    """xasd-uploader"""
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
