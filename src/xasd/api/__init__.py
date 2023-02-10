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


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: XasdDB = Depends(get_db)):
    users = db.get_users(skip=skip, limit=limit)
    return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: XasdDB = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.get("/track", response_model=list[schemas.Track])
def read_track(skip: int = 0, limit: int = 100, db: XasdDB = Depends(get_db)):
    db_tracks = db.api_get(models.Track)

    # if db_track is None:
    #     raise HTTPException(status_code=404, detail="Track not found")
    return db_tracks


@app.get("/tracks/{track_id}", response_model=schemas.Track)
def read_track(track_id: int, db: XasdDB = Depends(get_db)):
    db_track = db.get(models.Track, filter=[models.Track.track_id == track_id])

    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return db_track


@app.get("/health")
async def health_check():
    return {"status": "OK", "time": str(datetime.utcnow())}
