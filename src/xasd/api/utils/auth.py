from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional

from jose import JWTError, jwt

from xasd.database import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TODO: move to config
# Generate with: openssl rand -hex 32
SECRET_KEY = "179b0aa3d69230a452524996326029bac028438a71ed93ab64ff913170342321"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)


def password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = db.get(models.User, filter=[models.User.name == username])

    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
