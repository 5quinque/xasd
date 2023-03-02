import asyncio
import logging
import time
import urllib.parse
from typing import Optional

import libtorrent as lt

logger = logging.getLogger(__name__)


def create_lt_session():
    return lt.session()


async def download(session, magnet_link: str, download_path: str) -> bool:
    """
    Download the torrent associated with the specified magnet link.
    This method waits for the torrent download to complete.

    Args:
    session (lt.session)
    magnet_link (str): The magnet link of the torrent to download.
    download_path (str): Path to save the torrent

    Returns:
    bool: True if the torrent was downloaded successfully, False otherwise.
    """
    # logger.info(f"downloading <{magnet_link}>")

    handle = session.add_torrent({"url": magnet_link, "save_path": download_path})

    # Download the metadata
    # If there's no progress after 10 minutes, return
    session.start_dht()
    start_dht_time = time.time()
    while not handle.has_metadata():
        if time.time() - start_dht_time > 600:  # 10 minutes
            logger.info("Metadata download timed out")
            return False

        await asyncio.sleep(1)
        s = handle.status()
        logger.info("DHT: %.1f%%" % (s.download_rate / 10**6))

    # print information about the download
    # breakpoint()
    # print(
    #     f"Downloading {handle.name()} from {handle.num_seeds()} seeds with {handle.num_peers()} peers."
    # )

    # wait for the download to complete
    # while handle.status().state != lt.torrent_status.seeding:
    while not s.is_seeding:
        s = handle.status()
        if s.num_peers == 0 or s.download_rate == 0:
            no_progress_start_time = time.time()
            while s.num_peers == 0 or s.download_rate == 0:
                if time.time() - no_progress_start_time > 3600:  # 1 hour
                    logger.info("Torrent download progress timed out")
                    return False
                s = handle.status()
                logger.info(
                    f"Attempting to find peers for {s.name}",
                )
                await asyncio.sleep(1)
        # logger.info(
        #     f"Downloading {s.name} {s.download_rate}, from seeds {s.num_seeds}, peers {s.num_peers}",
        # )

        state_str = [
            "queued",
            "checking",
            "downloading metadata",
            "downloading",
            "finished",
            "seeding",
            "allocating",
        ]
        logger.info(
            "%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s"
            % (
                s.progress * 100,
                s.download_rate / 1000,
                s.upload_rate / 1000,
                s.num_peers,
                state_str[s.state],
            )
        )
        await asyncio.sleep(1)

    return True


def get_infohash(magnet_link: str) -> Optional[str]:
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
            return xt[9:]
    return None


def get_displayname(magnet_link: str) -> Optional[str]:
    """
    Parse the magnet link and return the display name if it exists.

    Args:
    magnet_link (str): The magnet link to parse.

    Returns:
    Optional[str]: The display name if it exists in the magnet link, None otherwise.
    """
    parsed = urllib.parse.urlparse(magnet_link)
    params = urllib.parse.parse_qs(parsed.query)
    if "dn" in params:
        return params["dn"][0]
    return None
