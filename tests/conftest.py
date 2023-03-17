import os
from tempfile import NamedTemporaryFile

import pytest
from fastapi.testclient import TestClient

from xasd.api import app
from xasd.api.dependencies import Auth
from xasd.database import models
from xasd.database.crud import XasdDB


@pytest.fixture(scope="function")
def client(env):
    yield TestClient(app)


@pytest.fixture(scope="function")
def env():
    os.environ["JWT_SECRET_KEY"] = "secret"
    # create a temporary file to use as the database
    with NamedTemporaryFile() as temp:
        os.environ["DATABASE_URL"] = f"sqlite:///{temp.name}"
        yield


# fixture to create a new file in the database
@pytest.fixture(scope="function")
def create_track(env):
    db = XasdDB()

    artist = db.create(models.Artist, name="artist_name")
    genre = db.create(models.Genre, name="genre_name")
    album = db.create(
        models.Album,
        filter=[
            models.Album.name == "album_name",
            models.Album.artist == artist,
        ],
        name="album_name",
        artist=artist,
    )
    track = db.create(
        models.Track,
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

    file = db.create(
        models.File,
        filter=[models.File.filepath == "filepath"],
        filepath="filepath",
        track=track,
        hash=db.add_unique_hash("hash"),
    )


@pytest.fixture(scope="function")
def create_user(env):
    db = XasdDB()

    yield db.create(
        models.User,
        name="username",
        password_hash="$2b$12$Tlj5xnuVKIWlE319Bu81ce8YRsWt5.Q/dkiQMgkdBbTJSFNPtzlzy",
        email_address="user@example.com",
    )


# create jwt access token for user
@pytest.fixture(scope="function")
def create_token(create_user):
    db = XasdDB()
    user = db.get(models.User, filter=[models.User.name == "username"])
    auth = Auth(db)
    token = auth.create_access_token(data={"sub": user.name})
    return token
