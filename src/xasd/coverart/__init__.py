"""
xasd_coverart

Usage:
    xasd_coverart [options]

Options:
    --artist=ARTIST                Artist name
    --album=ALBUM                  Album name
    --log-level=LEVEL              Set logger level, one of DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
"""

import os
import logging
import requests
from tempfile import NamedTemporaryFile
from docopt import docopt

from xasd.database.models import CoverArt as CoverArtModel
from xasd.database.models import Album as AlbumModel
from xasd.database.crud import XasdDB
from xasd.database.session import Session
from xasd.uploader.b2_upload import B2Bucket
from xasd.utils import setup_logging


logger = logging.getLogger(__name__)


class CoverArt:
    # set the API endpoint URLs
    # TODO: https ?
    cover_art_endpoint_url = "http://coverartarchive.org/release"
    musicbrainz_endpoint_url = "http://musicbrainz.org/ws/2/release"

    def __init__(self, artist, album):
        self.b2 = B2Bucket(
            os.environ.get("B2_BUCKETNAME"),
            os.environ.get("B2_KEY"),
            os.environ.get("B2_SECRET"),
        )

        self.artist = artist
        self.album = album
        self.cloud_path = None

    def search_release_id(self) -> str:
        # set the API endpoint URL and search parameters
        params = {
            "query": f"artist:{self.artist} AND release:{self.album}",
            "fmt": "json",
        }

        # send a GET request to the API with the search parameters
        response = requests.get(self.musicbrainz_endpoint_url, params=params)

        # parse the JSON response to retrieve the release ID for the first result
        if response.status_code == 200:
            data = response.json()
            if "releases" in data and len(data["releases"]) > 0:
                release_id = data["releases"][0]["id"]
                return release_id
            else:
                logger.info(
                    f"No release found for search term '{self.artist} {self.album}'"
                )
        else:
            logger.error(
                f"Failed to retrieve release ID for '{self.artist} {self.album}'"
            )

    def get_cover_art(self) -> str:
        release_id = self.search_release_id()

        # send a GET request to the API with the release ID as a parameter
        response = requests.get(f"{self.cover_art_endpoint_url}/{release_id}")

        # parse the JSON response to retrieve the image URL for the front cover
        if response.status_code == 200:
            data = response.json()
            image_url = data["images"][0]["thumbnails"]["small"]

            # download the image and save it to a file
            response = requests.get(image_url)
            if response.status_code == 200:
                # cloud_path should be c/first two characters of release_id/realease_id.jpg
                self.cloud_path = f"c/{release_id[:2]}/{release_id}.jpg"
                with NamedTemporaryFile() as f:
                    f.write(response.content)
                    self.b2.upload_file(f.name, self.cloud_path)
                logger.info(f"Cover art for '{self.artist} {self.album}' saved to file")

                return self.cloud_path
            else:
                logger.error(
                    f"Failed to download cover art for '{self.artist} {self.album}'"
                )
        else:
            logger.error(
                f"Failed to retrieve cover art for '{self.artist} {self.album}'"
            )


def main():
    opts = docopt(__doc__)
    setup_logging(opts)

    artist = opts["--artist"]
    album = opts["--album"]

    session = Session()
    db = XasdDB(session=session.get_session())

    album_entity = db.album.get(
        filter=[AlbumModel.name == album and AlbumModel.artist == artist]
    )

    cover_art = CoverArt(artist=artist, album=album)
    cover_art.get_cover_art()
    db.cover_art.create(
        filter=[CoverArtModel.album == album_entity],
        album=album_entity,
        filepath=cover_art.cloud_path,
    )


if __name__ == "__main__":
    main()
