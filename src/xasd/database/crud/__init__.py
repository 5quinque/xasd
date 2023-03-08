import os
import functools
import logging
import time
from typing import Optional, Tuple, Union

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_, exc as sqlalchemy_exc

from xasd.database import Base
from xasd.database.models import Album, Artist, File, Genre, Magnet, Track, Hash

logger = logging.getLogger(__name__)


class XasdDB:
    def __init__(self, db_url: Optional[str] = None):
        self._db_url = db_url
        if self._db_url is None:
            self._db_url = os.environ.get("DATABASE_URL")
        if self._db_url is None:
            raise ValueError(
                "Provide a valid database URL by setting the `DATABASE_URL` environment variable."
            )

        self._db_connect()

    def _db_connect(self):
        """Connect to the database and create all relevant tables if they don't exist"""
        self.__engine = create_engine(self._db_url)

        connection_attempts = 0
        while True:
            try:
                connection_attempts += 1
                logger.info(
                    f"[{connection_attempts}] Attempting to connect to database"
                )
                Base.metadata.create_all(self.__engine)
                logger.info(
                    f"[{connection_attempts}] Successfully connected to database"
                )
                break
            except sqlalchemy_exc.OperationalError as e:
                if connection_attempts == 300:
                    logger.error(
                        f"Failed to connect to database after {connection_attempts} attempts. Exiting."
                    )
                    raise e
                logger.warning(f"Failed to connect to base. Retrying in 5 seconds.")
                time.sleep(5)

        Session = sessionmaker(bind=self.__engine)
        self._session = Session()

    def get(self, table, filter=False, create=False, **kwargs):
        """Get an entity if one doesn't exist with the given name (or by given filter)
        Args:
            table (Table): Table object you want to look/create the row
            filter (bool, optional): Optional `where` list . Defaults to False which is filter by `name` column.
            create (bool, optional): Create an entity if one doesn't exist

        Returns:
            (object, None): pre-existing or newly created entity object, or `None` if no entity is found and `create=False`

        n.b.
            I don't think there is a single transitive verb that can be used to describe both "getting" and "creating" at the same time.
            The verb "get" can be used to mean "acquire" something that already exists.
            The verb "create" can be used to mean "bring into existence" or "cause to exist" something that did not previously exist.
            Hopefully "get" isn't too confusing for what this method actually does.
        """
        if not filter:
            filter = [table.name == kwargs["name"]]

        entity = self._session.query(table).filter(*filter).first()

        if entity:
            return entity

        if not create:
            return None

        new_entity = table(**kwargs)
        self._session.add(new_entity)
        self._session.commit()

        return new_entity

    create = functools.partialmethod(get, create=True)

    def search_track(self, query):
        """Search for a track by name

        Args:
            query (str): String to search for

        Returns:
            list[Track]: List of tracks
        """
        return self.search(Track, query, Track.title)

    def search_artist(self, query):
        """Search for an artist by name

        Args:
            query (str): String to search for

        Returns:
            list[Artist]: List of artists
        """
        return self.search(Artist, query, Artist.name)

    def search_album(self, query):
        """Search for an album by name

        Args:
            query (str): String to search for

        Returns:
            list[Album]: List of albums
        """
        return self.search(Album, query, Album.name)

    def search(self, table, query, query_column):
        """Search for an entity by name

        Args:
            table (Table): Table object you want to query
            query (str): String to search for

        Returns:
            list[entity]: List of entities

        n.b.
            This is a very simple search that just looks for the query string anywhere in the title.
            It's not very good, but it's good enough for now.
        """

        return self._session.query(table).filter(query_column.ilike(f"%{query}%")).all()

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
            "tracks": self.search_track(query),
            "artists": self.search_artist(query),
            "albums": self.search_album(query),
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
        if self.get(
            Hash,
            filter=[
                Hash.hash == hash,
            ],
        ):
            return False
        return self.create(
            Hash,
            filter=[
                Hash.hash == hash,
            ],
            hash=hash,
        )

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
