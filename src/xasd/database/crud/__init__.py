import logging
from typing import Tuple, Union

import sqlalchemy

from xasd.database.models import (
    Album,
    Artist,
    File,
    Genre,
    Magnet,
    Track,
    Hash,
)

from xasd.database.crud.table.album import Album as AlbumCRUD
from xasd.database.crud.table.artist import Artist as ArtistCRUD
from xasd.database.crud.table.cover_art import CoverArt as CoverArtCRUD
from xasd.database.crud.table.file import File as FileCRUD
from xasd.database.crud.table.playlist import Playlist as PlaylistCRUD
from xasd.database.crud.table.track import Track as TrackCRUD
from xasd.database.crud.table.user import User as UserCRUD
from xasd.database.crud.table.genre import Genre as GenreCRUD
from xasd.database.crud.table.hash import Hash as HashCRUD

logger = logging.getLogger(__name__)


class XasdDB:
    def __init__(self, session: sqlalchemy.orm.session.Session):
        self._session = session

        self.album = AlbumCRUD(self._session)
        self.artist = ArtistCRUD(self._session)
        self.cover_art = CoverArtCRUD(self._session)
        self.file = FileCRUD(self._session)
        self.genre = GenreCRUD(self._session)
        self.hash = HashCRUD(self._session)
        self.playlist = PlaylistCRUD(self._session)
        self.track = TrackCRUD(self._session)
        self.user = UserCRUD(self._session)

    def search_all(self, query):
        """Search for an entity by name

        Args:
            query (str): String to search for

        Returns:
            dict[str, list[entity]]: List of entities

        n.b.
            This is a very simple search that just looks for the query string anywhere in the title.
            It's not very good, but it's good enough for now.
        """
        return {
            "tracks": self.track.search(query),
            "artists": self.artist.search(query),
            "albums": self.album.search(query),
        }

    def api_get(self, table, filter=[], skip=0, limit=100):
        """Used within the API to get pagination list of entities

        Args:
            table (Table): Table object you want to query
            filter (list): List of filters to apply
            skip (int, optional): Number of entities to skip pass. Defaults to 0.
            limit (int, optional): Number of entities to return. Defaults to 100.

        Returns:
            list[entity]: List of entities
        """
        return (
            self._session.query(table).filter(*filter).offset(skip).limit(limit).all()
        )

    def insert_file(self, filepath, info) -> Tuple[File, Track]:
        """Insert a file into the database,
            creating relevant artist, genre, album, track, and file rows where necessary

        Args:
            filepath (str): _description_
            info (dict): id3 info e.g.
                        {
                            'album': 'Fractures',
                            'title': 'Fractures',
                            'artist': 'Killing the Dream',
                            'tracknumber': '03',
                            'genre': 'Hardcore',
                            'date': '2008'
                        }

        Returns:
            tuple: file and track object
        """
        artist = self.create(Artist, name=info.get("artist"))
        genre = self.create(Genre, name=info.get("genre"))
        album = self.create(
            Album,
            filter=[
                Album.name == info.get("album"),
                Album.artist == artist,
            ],
            name=info.get("album"),
            artist=artist,
        )
        track = self.create(
            Track,
            filter=[
                Track.title == info.get("title"),
                Track.artist == artist,
                Track.album == album,
            ],
            title=info.get("title"),
            tracknumber=info.get("tracknumber"),
            date=info.get("date"),
            album=album,
            artist=artist,
            genre=genre,
        )

        file = self.create(
            File,
            filter=[File.filepath == filepath],
            filepath=filepath,
            track=track,
            hash=info.get("hash"),
        )

        return (file, track)

    def add_unique_hash(self, hash: str) -> Union[bool, Hash]:
        """
        Adds the given hash to the database if it doesn't already exist.

        Parameters:
            hash (str): The hash to add to the database.

        Returns:
            Union[bool, Hash]: False if the hash already exists in the database,
            otherwise returns the entity representing the added hash.
        """
        if self.hash.get(hash):
            return False
        return self.hash.create(hash=hash)

    def add_magnet(self, infohash: str) -> Union[bool, Magnet]:
        """
        Adds the given magnet to the database if it doesn't already exist.

        Parameters:
            infohash (str): The magnet links info hash to add to the database.

        Returns:
            Union[bool, Magnet]: False if the infohash already exists in the database,
            otherwise returns the entity representing the added magnet.
        """
        if self.get(
            Magnet,
            filter=[
                Magnet.infohash == infohash,
            ],
        ):
            return False
        return self.create(
            Magnet,
            filter=[
                Magnet.infohash == infohash,
            ],
            infohash=infohash,
        )
