import os
from tempfile import NamedTemporaryFile

import pytest
from fastapi.testclient import TestClient

from xasd.api import app
from xasd.api.dependencies import Auth
from xasd.database import models
from xasd.database.crud import XasdDB
from xasd.database.session import Session


@pytest.fixture(scope="function")
def client(env):
    yield TestClient(app)


@pytest.fixture(scope="function")
def db(env):
    pool = Session()
    db_session = pool.get_session()

    db = XasdDB(session=db_session)
    try:
        yield db
    finally:
        db_session.close()
        del db


@pytest.fixture(scope="function")
def env():
    os.environ["JWT_SECRET_KEY"] = "secret"
    # create a temporary file to use as the database
    with NamedTemporaryFile() as temp:
        os.environ["DATABASE_URL"] = f"sqlite:///{temp.name}"
        yield


# fixture to create a new file in the database
@pytest.fixture(scope="function")
def create_track(db):
    artist = db.artist.create(name="artist_name")
    genre = db.genre.create(name="genre_name")
    album = db.album.create(
        filter=[
            models.Album.name == "album_name",
            models.Album.artist == artist,
        ],
        name="album_name",
        artist=artist,
    )
    track = db.track.create(
        filter=[
            models.Track.title == "track_title",
            models.Track.artist == artist,
            models.Track.album == album,
        ],
        title="track_title",
        tracknumber="1",
        date="2023",
        album=album,
        artist=artist,
        genre=genre,
    )

    file = db.file.create(
        filter=[models.File.filepath == "filepath"],
        filepath="filepath",
        track=track,
        hash=db.add_unique_hash("hash"),
    )


@pytest.fixture(scope="function")
def create_user(db):
    yield db.user.create(
        name="username",
        password_hash="$2b$12$Tlj5xnuVKIWlE319Bu81ce8YRsWt5.Q/dkiQMgkdBbTJSFNPtzlzy",
        email_address="user@example.com",
    )


# create jwt access token for user
@pytest.fixture(scope="function")
def create_token(db, create_user):
    user = db.user.get("username")
    auth = Auth(db)
    token = auth.create_access_token(data={"sub": user.name})
    return token


@pytest.fixture(scope="function")
def create_playlist(db, create_token, create_track):
    user = db.user.get("username")
    track = db.track.get(filter=[models.Track.title == "track_title"])

    playlist = db.playlist.create(
        filter=[models.Playlist.name == "playlist_name"],
        name="playlist_name",
        owner=user,
        tracks=[track],
    )

    yield {"token": create_token, "playlist": playlist}


# @pytest.fixture(scope="function")
# def mp3_file():
#     with open("tests/fixtures/track.mp3", "rb") as f:
#         yield f
