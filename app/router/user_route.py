from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.crud import create_user
from app.auth.deps import authenticate
from app.auth.core import create_access_token

from app.database.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.user import Token, UserResponse, UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.database.core import get_db

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


user_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@user_router.post("/signup", response_model=UserResponse)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user_in)  


@user_router.post("/token")
async def login_for_access_token(request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
        },
        expires_delta=access_token_expires,
    )
    token = Token(access_token=access_token, token_type="bearer")

    return templates.TemplateResponse(
        request=request, name="login.html", context={"token":token}
    )
