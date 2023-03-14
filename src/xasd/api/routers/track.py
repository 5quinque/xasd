from fastapi import APIRouter, Depends, HTTPException

from xasd.api.dependencies import db
from xasd.database import schemas, models
from xasd.database.crud import XasdDB

track_router = APIRouter(
    prefix="/track",
    tags=["Track"],
    dependencies=[Depends(db)],
    responses={404: {"description": "Not found"}},
)


# Tracks endpoints
@track_router.get("/", response_model=list[schemas.Track])
def read_track(skip: int = 0, limit: int = 100, db: XasdDB = Depends(db)):
    db_tracks = db.api_get(models.Track)

    return db_tracks


@track_router.get("/{track_id}", response_model=schemas.Track)
def read_track(track_id: int, db: XasdDB = Depends(db)):
    db_track = db.get(models.Track, filter=[models.Track.track_id == track_id])

    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")

    return db_track


# get file info by track
@track_router.get("/{track_id}/file", response_model=schemas.File)
def read_file(track_id: int, db: XasdDB = Depends(db)):
    track = db.get(models.Track, filter=[models.Track.track_id == track_id])
    db_file = db.get(models.File, filter=[models.File.track == track])

    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file
