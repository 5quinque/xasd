from fastapi import Depends, FastAPI, HTTPException, Request
from datetime import datetime

from xasd.database import schemas, models
from xasd.database.crud import XasdDB


app = FastAPI()


# Dependency
def get_db():
    db = XasdDB()
    try:
        yield db
    finally:
        del db


@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# Tags
tags_metadata = [
    {
        "name": "Tracks",
        "description": "Endpoints related to tracks.",
    },
    {
        "name": "Health",
        "description": "Endpoint for checking the health of the API.",
    },
    {
        "name": "Search",
        "description": "Endpoints for searching for tracks.",
    },
]

# Search endpoints
@app.get(
    "/search/any/{query}",
    response_model=schemas.SearchListResponse,
    tags=["Search"],
)
def search_any(query: str, db: XasdDB = Depends(get_db)):
    db_results = db.search_all(query)

    return db_results


@app.get("/search/track/{query}", response_model=list[schemas.Track], tags=["Search"])
def search_track(query: str, db: XasdDB = Depends(get_db)):
    db_results = db.search_track(query)

    return db_results


# Tracks endpoints
@app.get("/track", response_model=list[schemas.Track], tags=["Tracks"])
def read_track(skip: int = 0, limit: int = 100, db: XasdDB = Depends(get_db)):
    db_tracks = db.api_get(models.Track)

    return db_tracks


@app.get("/track/{track_id}", response_model=schemas.Track, tags=["Tracks"])
def read_track(track_id: int, db: XasdDB = Depends(get_db)):
    db_track = db.get(models.Track, filter=[models.Track.track_id == track_id])

    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")

    return db_track


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "OK", "time": str(datetime.utcnow())}


# get file info by track
@app.get("/tracks/{track_id}/file", response_model=schemas.File)
def read_file(track_id: int, db: XasdDB = Depends(get_db)):
    track = db.get(models.Track, filter=[models.Track.track_id == track_id])
    db_file = db.get(models.File, filter=[models.File.track == track])

    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file
