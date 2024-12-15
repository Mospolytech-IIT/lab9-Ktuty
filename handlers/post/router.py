from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models.models import Post
from handlers.post.schema import PostRead, PostWrite

post_router = APIRouter(
    prefix="/post"
)


@post_router.get("/set_default")
async def add_posts(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ]
) -> str:
    try:
        posts = [
            Post(id=0, title="Post 1", content="Content 1", user_id=0),
            Post(id=1, title="Post 2", content="Content 2", user_id=1),
            Post(id=2, title="Post 3", content="Content 3", user_id=2),
        ]

        session.add_all(posts)
        await session.commit()

        return "Added secsessfuly"
    except Exception as e:
        return HTTPException(status_code=500, detail=e)


@post_router.get("/all")
async def get_all(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ]
):
    query = select(Post)
    result = await session.scalars(query)
    return result.all()


@post_router.get("/{user_id}")
async def get_all(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ],
        user_id: int
):

    query = select(Post).filter(Post.user_id == user_id)
    result = await session.scalars(query)
    print(result)
    return result.all()


@post_router.put("/content")
async def email_update(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ],
        post_id: Annotated[int, Form()],
        content: Annotated[str, Form()],
) -> PostRead:
    result = await session.execute(select(Post).filter(Post.id == post_id))
    post = result.scalars().first()
    print(post)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    post.content = content
    await session.commit()
    return post


@post_router.delete("del", response_model=dict)
async def delete_posts(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ],
        user_id: int,
):
    result = await session.execute(select(Post).filter(Post.user_id == user_id))
    post = result.scalars().all()
    print(post)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    for i in post:
        session.delete(i)
    await session.commit()
    return {"message": "Post deleted successfully"}