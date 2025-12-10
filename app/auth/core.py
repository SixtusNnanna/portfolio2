from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC

from passlib.context import CryptContext

from pwdlib import PasswordHash

from app.database.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


pwd_context = PasswordHash.recommended()



def verify_pw(paln_pw, hash_pw):
    return pwd_context.verify(paln_pw, hash_pw)


def hash_pw(plain_pw):
    return pwd_context.hash(plain_pw)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.now(UTC) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
