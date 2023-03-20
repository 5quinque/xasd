from fastapi import APIRouter

from xasd.api import dependencies
from xasd.database import schemas

search_router = APIRouter(
    prefix="/search",
    tags=["Search"],
    # dependencies=[Depends(db)],
    responses={404: {"description": "Not found"}},
)


# Search endpoints
@search_router.get(
    "/any/{query}",
    response_model=schemas.SearchListResponse,
)
def search_any(query: str, db: dependencies.database):
    db_results = db.search_all(query)

    return db_results


@search_router.get("/track/{query}", response_model=list[schemas.Track])
def search_track(query: str, db: dependencies.database):
    db_results = db.track.search(query)

    return db_results
