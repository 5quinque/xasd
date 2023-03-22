from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from xasd.api.services.auth import Auth
from xasd.database.crud import XasdDB
from xasd.database import schemas, models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def _db():
    db = XasdDB()
    try:
        yield db
    finally:
        del db


async def _pagination_parameters(page: int = 1):
    skip = (page - 1) * 50
    limit = 50

    return {"skip": skip, "limit": limit}


def _auth(db: XasdDB = Depends(_db)):
    auth = Auth(db)
    try:
        yield auth
    finally:
        del auth


async def _current_user(
    auth: Auth = Depends(_auth), token: str = Depends(oauth2_scheme)
):
    user = auth.user(token)
    if user:
        return user

    raise HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _track(track_id: int, db: XasdDB = Depends(_db)):
    db_track = db.track.get(filter=[models.Track.track_id == track_id])

    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")

    return db_track


def _file(track: schemas.Track = Depends(_track), db: XasdDB = Depends(_db)):
    db_file = db.file.get(track)

    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")

    return db_file


def _artist(artist_name: str, db: XasdDB = Depends(_db)):
    db_artist = db.artist.get(artist_name)

    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")

    return db_artist


def _playlist(playlist_id: int, db: XasdDB = Depends(_db)):
    """
    We could add `current_user` as a dependency to `_playlist` and check
    if the user is the owner of the playlist
    """
    db_playlist = db.playlist.get(filter=[models.Playlist.playlist_id == playlist_id])

    if db_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")

    return db_playlist


artist = Annotated[schemas.Artist, Depends(_artist)]
auth = Annotated[Auth, Depends(_auth)]
current_user = Annotated[bool, Depends(_current_user)]
database = Annotated[XasdDB, Depends(_db)]
file = Annotated[schemas.File, Depends(_file)]
pagination_parameters = Annotated[dict, Depends(_pagination_parameters)]
playlist = Annotated[schemas.Playlist, Depends(_playlist)]
track = Annotated[schemas.Track, Depends(_track)]
