from sqlalchemy import Column, String, Table, Text, ForeignKey, Integer
from db import mapper_registry, metadata_obj, engine


user = Table(
    "user",
    metadata_obj,
    Column("id", Integer(), primary_key=True,nullable=False, autoincrement=True),
    Column("username", String(64), nullable=False),
    Column("email", String(64), nullable=False),
    Column("password", String(64), nullable=False),
)


class User:
    pass


mapper_registry.map_imperatively(User, user)

post = Table(
    "post",
    metadata_obj,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("title", String(256), nullable=False),
    Column("content", Text(), nullable=False),
    Column("user_id", Integer(), ForeignKey("user.id"), nullable=False),
)


class Post:
    """ Заглушка для маппинга sql моделей """
    pass


mapper_registry.map_imperatively(Post, post)

# metadata_obj.create_all(engine)