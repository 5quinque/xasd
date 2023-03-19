from fastapi import APIRouter, Depends, HTTPException

from xasd.api.dependencies import db
from xasd.database import schemas, models
from xasd.database.crud import XasdDB

artist_router = APIRouter(
    prefix="/artist",
    tags=["Artist"],
    dependencies=[Depends(db)],
    responses={404: {"description": "Not found"}},
)


# get albums by artist
@artist_router.get("/{artist_name}/albums", response_model=list[schemas.Album])
def read_albums(artist_name: str, db: XasdDB = Depends(db)):
    artist = db.artist.get(artist_name)
    db_albums = db.api_get(models.Album, filter=[models.Album.artist == artist])

    if not db_albums:
        raise HTTPException(status_code=404, detail="Albums not found")
    return db_albums


# get tracks by artist
@artist_router.get("/{artist_name}/tracks", response_model=list[schemas.Track])
def read_tracks(artist_name: str, db: XasdDB = Depends(db)):
    artist = db.artist.get(artist_name)
    db_tracks = db.api_get(models.Track, filter=[models.Track.artist == artist])

    if not db_tracks:
        raise HTTPException(status_code=404, detail="Tracks not found")
    return db_tracks
