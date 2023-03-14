from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from xasd.api.dependencies import db, get_current_user
from xasd.api.utils.auth import (
    authenticate_user,
    create_access_token,
    password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from xasd.database import schemas, models
from xasd.database.crud import XasdDB


user_router = APIRouter(
    # prefix="/",
    tags=["User"],
    dependencies=[Depends(db)],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/user/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


# preflight options req for /user/me
@user_router.options("/user/me", response_model=schemas.User)
async def options_user_me():
    return Response(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "accept, Authorization",
        }
    )


@user_router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: XasdDB = Depends(db)
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# register
@user_router.post("/user", response_model=schemas.User, status_code=201)
async def create_user(user: schemas.UserCreate, db: XasdDB = Depends(db)):
    # [TODO] move user creation to auth module
    #        also return a token
    db_user = db.get(models.User, filter=[models.User.name == user.name])
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return db.create(
        models.User,
        name=user.name,
        password_hash=password_hash(user.plaintext_password),
        email_address=user.email_address,
    )


@user_router.options("/user", response_model=schemas.User)
async def options_user():
    return Response(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "accept, Content-Type, Authorization",
        }
    )
