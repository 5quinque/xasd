from fastapi import APIRouter, HTTPException

from xasd.api import dependencies
from xasd.database import schemas, models

track_router = APIRouter(
    prefix="/track",
    tags=["Track"],
    responses={404: {"description": "Not found"}},
)


@track_router.get("/", response_model=list[schemas.Track])
def read_tracks(
    pagination: dependencies.pagination_parameters, db: dependencies.database
):
    print(pagination)
    db_tracks = db.api_get(models.Track)

    return db_tracks


@track_router.get("/{track_id}", response_model=schemas.Track)
def read_track(track_id: int, db: dependencies.database):
    db_track = db.track.get(filter=[models.Track.track_id == track_id])

    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")

    return db_track


@track_router.get("/{track_id}/file", response_model=schemas.File)
def read_file(track_id: int, db: dependencies.database):
    track = db.track.get(filter=[models.Track.track_id == track_id])
    db_file = db.file.get(track)

    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file


# # map track parameter to entity
# @track_router.get("/{track_id}/file", response_model=schemas.File)
# def read_file(track: models.Track = Depends(db.get_entity(models.Track))):
#     db_file = db.get(models.File, filter=[models.File.track == track])

#     if db_file is None:
#         raise HTTPException(status_code=404, detail="File not found")
#     return db_file
