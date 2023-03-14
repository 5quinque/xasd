from fastapi import FastAPI
from datetime import datetime

from xasd.api.routers import track, artist, search, user


tags_metadata = [
    {
        "name": "Track",
        "description": "Endpoints related to tracks.",
    },
    {
        "name": "Artist",
        "description": "Endpoints related to artists.",
    },
    {
        "name": "Search",
        "description": "Endpoints for searching for tracks.",
    },
    {
        "name": "Health",
        "description": "Endpoint for checking the health of the API.",
    },
]

app = FastAPI(
    title="XASD API",
    description="...",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

app.include_router(track.track_router)
app.include_router(artist.artist_router)
app.include_router(search.search_router)
app.include_router(user.user_router)


@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "OK", "time": str(datetime.utcnow())}
