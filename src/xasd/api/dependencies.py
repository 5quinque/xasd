from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from xasd.api.utils.auth import ALGORITHM, SECRET_KEY
from xasd.database import models
from xasd.database.schemas import User, TokenData
from xasd.database.crud import XasdDB

from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def db():
    db = XasdDB()
    try:
        yield db
    finally:
        del db


async def get_current_user(
    db: XasdDB = Depends(db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.get(models.User, filter=[models.User.name == username])
    if user is None:
        raise credentials_exception
    return user
