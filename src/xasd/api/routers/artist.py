from fastapi import APIRouter, HTTPException

from xasd.api import dependencies
from xasd.database import schemas, models

artist_router = APIRouter(
    prefix="/artist",
    tags=["Artist"],
    responses={404: {"description": "Not found"}},
)


@artist_router.get("/{artist_name}/albums", response_model=list[schemas.Album])
def read_albums(artist: dependencies.artist, db: dependencies.database):
    db_albums = db.api_get(models.Album, filter=[models.Album.artist == artist])

    if not db_albums:
        raise HTTPException(status_code=404, detail="Albums not found")
    return db_albums


@artist_router.get("/{artist_name}/tracks", response_model=list[schemas.Track])
def read_tracks(artist: dependencies.artist, db: dependencies.database):
    db_tracks = db.api_get(models.Track, filter=[models.Track.artist == artist])

    if not db_tracks:
        raise HTTPException(status_code=404, detail="Tracks not found")
    return db_tracks
