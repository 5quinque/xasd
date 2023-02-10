import asyncio
import logging
import time

import libtorrent as lt

logger = logging.getLogger(__name__)


def create_lt_session():
    return lt.session()


async def download(session, magnet_link, download_path):
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
    logger.info(f"downloading <{magnet_link}>")

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
        logger.info("DHT: %.1f%%" % (s.dht_download_rate / 10**6))

    # print information about the download
    print(
        f"Downloading {handle.name()} from {handle.num_seeds()} seeds with {handle.num_peers()} peers."
    )

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
                await asyncio.sleep(1)

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
            ),
            end="\r",
        )
        await asyncio.sleep(1)

    return True
