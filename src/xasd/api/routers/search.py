from fastapi import APIRouter, Depends

from xasd.api.dependencies import db
from xasd.database import schemas
from xasd.database.crud import XasdDB

search_router = APIRouter(
    prefix="/search",
    tags=["Search"],
    dependencies=[Depends(db)],
    responses={404: {"description": "Not found"}},
)


# Search endpoints
@search_router.get(
    "/any/{query}",
    response_model=schemas.SearchListResponse,
)
def search_any(query: str, db: XasdDB = Depends(db)):
    db_results = db.search_all(query)

    return db_results


@search_router.get("/track/{query}", response_model=list[schemas.Track])
def search_track(query: str, db: XasdDB = Depends(db)):
    db_results = db.search_track(query)

    return db_results
