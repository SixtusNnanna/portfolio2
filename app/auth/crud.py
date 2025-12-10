from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.core import hash_pw
from app.models import User
from app.schemas.user import UserCreate


async def get_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UserCreate):
    user = await get_by_username(db, user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_pw(user_in.password),
    )
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    await db.commit()
    return new_user
