from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from xasd.api import dependencies

from xasd.api.services.auth import Auth
from xasd.database import schemas


user_router = APIRouter(
    # prefix="/",
    tags=["User"],
    # dependencies=[Depends(db)],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/user/me", response_model=schemas.User)
async def read_users_me(current_user: dependencies.current_user):
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


@user_router.post("/token", response_model=schemas.Token)
async def login(
    auth: dependencies.auth, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = auth.create_access_token(data={"sub": user.name})

    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/user", response_model=schemas.User, status_code=201)
async def create_user(user: schemas.UserCreate, auth: dependencies.auth):
    # "registering" a user is more of a "crud" task. We will probably move that.
    # creating of the token still requires `auth`.
    db_user = auth.register_user(user)
    if db_user:
        # [TODO] also return a token
        # access_token = auth.create_access_token(data={"sub": user.name})
        # return {"user": user, "jwt": {"access_token": access_token, "token_type": "bearer"}}

        return db_user
    else:
        raise HTTPException(status_code=409, detail="User already registered")


@user_router.options("/user", response_model=schemas.User)
async def options_user():
    return Response(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS, POST",
            "Access-Control-Allow-Headers": "accept, Content-Type, Authorization",
        },
    )
