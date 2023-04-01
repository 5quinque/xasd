from fastapi import APIRouter

from xasd.api import dependencies
from xasd.database import schemas, models

track_router = APIRouter(
    prefix="/track",
    tags=["Track"],
    responses={404: {"description": "Not found"}},
)


@track_router.get("", response_model=list[schemas.Track])
def read_tracks(
    pagination: dependencies.pagination_parameters, db: dependencies.database
):
    db_tracks = db.api_get(models.Track)

    return db_tracks


@track_router.get("/{track_id}", response_model=schemas.Track)
def read_track(track: dependencies.track):
    return track


@track_router.get("/{track_id}/file", response_model=schemas.File)
def read_file(file: dependencies.file):
    return file
