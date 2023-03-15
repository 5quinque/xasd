from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from xasd.api.services.auth import Auth
from xasd.database.crud import XasdDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def db():
    db = XasdDB()
    try:
        yield db
    finally:
        del db


def auth(db: XasdDB = Depends(db)):
    auth = Auth(db)
    try:
        yield auth
    finally:
        del auth


async def get_current_user(
    auth: Auth = Depends(auth), token: str = Depends(oauth2_scheme)
):
    user = auth.user(token)
    if user:
        return user

    return False
