from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from xasd.api.services.auth import Auth
from xasd.database.crud import XasdDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def _db():
    db = XasdDB()
    try:
        yield db
    finally:
        del db


async def _pagination_parameters(page: int = 1):
    skip = (page - 1) * 50
    limit = 50

    return {"skip": skip, "limit": limit}


def _auth(db: XasdDB = Depends(_db)):
    auth = Auth(db)
    try:
        yield auth
    finally:
        del auth


async def _current_user(
    auth: Auth = Depends(_auth), token: str = Depends(oauth2_scheme)
):
    user = auth.user(token)
    if user:
        return user

    return False


database = Annotated[XasdDB, Depends(_db)]
pagination_parameters = Annotated[dict, Depends(_pagination_parameters)]
auth = Annotated[Auth, Depends(_auth)]
current_user = Annotated[bool, Depends(_current_user)]
