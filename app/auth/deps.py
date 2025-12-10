from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.crud import get_by_username
from app.database.config import SECRET_KEY, ALGORITHM
from app.models import User
from app.database.core import get_db
from sqlalchemy import select
from app.schemas.user import TokenData

from app.auth.core import verify_pw


oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth_2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    
    except JWTError:
        raise credentials_exception
    
    user = await get_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


def get_active_user(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db) ):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorised to open this endpoint",
        )
    return current_user


async def authenticate(db: AsyncSession, username: str, password: str):
    user = await get_by_username(db, username)
    if not user:
        return False
    
    if not verify_pw(password, user.hashed_password):
        return False
    else:
        return user 
