"""sqlalchemy models
"""
from sqlalchemy.orm import relationship
from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    Integer,
    String,
)

from xasd.database import Base

playlist_association_table = Table(
    "playlist_association_table",
    Base.metadata,
    Column("left_id", ForeignKey("playlist.playlist_id"), primary_key=True),
    Column("right_id", ForeignKey("track.track_id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(32))
    email_address = Column(String(128))
    password_hash = Column(String(128))
    playlists = relationship("Playlist", back_populates="owner")


class File(Base):
    __tablename__ = "file"

    file_id = Column(Integer, primary_key=True)
    filepath = Column(String(64), nullable=False)
    track = relationship("Track", uselist=False, back_populates="file")

    hash_id = Column(ForeignKey("hash.hash_id"))
    hash = relationship("Hash", back_populates="file")


class Track(Base):
    __tablename__ = "track"

    track_id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=True)
    tracknumber = Column(String(32), nullable=True)
    date = Column(String(32), nullable=True)

    file_id = Column(ForeignKey("file.file_id"))
    file = relationship("File", back_populates="track")

    album_id = Column(ForeignKey("album.album_id"))
    album = relationship("Album", back_populates="tracks")

    artist_id = Column(ForeignKey("artist.artist_id"))
    artist = relationship("Artist", back_populates="tracks")

    genre_id = Column(ForeignKey("genre.genre_id"))
    genre = relationship("Genre", back_populates="tracks")

    playlists = relationship(
        "Playlist", secondary=playlist_association_table, back_populates="tracks"
    )


class Artist(Base):
    __tablename__ = "artist"

    artist_id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    albums = relationship("Album", back_populates="artist")
    tracks = relationship("Track", back_populates="artist")


class Album(Base):
    __tablename__ = "album"

    album_id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    artist_id = Column(Integer, ForeignKey("artist.artist_id"))
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album")


class Genre(Base):
    __tablename__ = "genre"

    genre_id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    tracks = relationship("Track", back_populates="genre")


class Playlist(Base):
    __tablename__ = "playlist"

    playlist_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.user_id"))
    owner = relationship("User", back_populates="playlists")
    name = Column(String(64), nullable=False)
    tracks = relationship(
        "Track", secondary=playlist_association_table, back_populates="playlists"
    )


class Hash(Base):
    __tablename__ = "hash"

    hash_id = Column(Integer, primary_key=True)
    hash = Column(String(32), nullable=False)
    file = relationship("File", uselist=False, back_populates="hash")


class Magnet(Base):
    __tablename__ = "magnet"

    magnet_id = Column(Integer, primary_key=True)
    infohash = Column(String(64))
