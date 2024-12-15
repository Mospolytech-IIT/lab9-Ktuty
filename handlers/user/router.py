from fastapi import APIRouter, Depends, Form, HTTPException
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models.models import User
from handlers.user.schema import UserWrite, UserRead
from handlers.post.router import delete_posts

user_router = APIRouter(
    prefix="/user"
)


@user_router.get("/set_default")
async def add_users(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ]
):
    users = [
        User(id=0, username="user1", email="user1@example.com", password="password1"),
        User(id=1, username="user2", email="user2@example.com", password="password2"),
        User(id=2, username="user3", email="user3@example.com", password="password3"),
    ]

    session.add_all(users)

    await session.commit()


@user_router.get("/all")
async def get_all(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ]
):
    query = select(User)
    result = await session.scalars(query)
    return result.all()


@user_router.put("/email")
async def email_update(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ],
        user_id: Annotated[int, Form()],
        email: Annotated[str, Form()],
) -> UserRead:
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = email
    await session.commit()
    return user


@user_router.delete("del", response_model=dict)
async def delete_user(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ],
        user_id: int,
):
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}


@user_router.delete("del_with_posts", response_model=dict)
async def delete_user_with_posts(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ],
        user_id: int,
):
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await delete_posts(session=session, user_id=user_id)
    session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}