from collections.abc import Iterable

from sqlalchemy import select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.auth.model import User
from app.routers.auth.schemas import UserModel
from app.routers.posts.models import Post
from app.utils.scripts import Hasher


async def get_posts_operation(db_session: AsyncSession) -> Post:
    query = select(Post)
    result = await db_session.execute(query)
    posts = result.scalars().all()

    return [post.__dict__ for post in posts]


async def get_post_by_id(db_session: AsyncSession, post_id: int) -> Post:
    result = await db_session.execute(select(Post).where(Post.id == post_id))
    return result.scalars().first()


async def create_post_operation(db_session: AsyncSession, post_data: dict):
    new_post = Post(**post_data)
    db_session.add(new_post)
    await db_session.commit()
    await db_session.refresh(new_post)
    return new_post


async def update_post_operation(db_session: AsyncSession, post_id: int, updated_data: dict):
    stmt = update(Post).where(Post.id == post_id).values(**updated_data)
    await db_session.execute(stmt)
    await db_session.commit()
    return await get_post_by_id(db_session, post_id)


async def delete_post_operation(db_session: AsyncSession, post_id: int):
    stmt = delete(Post).where(Post.id == post_id)
    await db_session.execute(stmt)
    await db_session.commit()
    return {"message": "Post deleted successfully"}


# User Auth Sql Operation

async def get_user_by(db_session: AsyncSession, user_data: UserModel):
    query = select(User).where(
        or_(User.login == user_data.login, User.email == user_data.email, User.phone == user_data.phone)
    )

    result = await db_session.execute(query)
    user = result.scallars().all()

    return user


async def add_new_user(db_session: AsyncSession, user_data: UserModel):
    user_data.password = Hasher.get_password_hash(password=user_data.password)

    new_user = User(
        name=user_data.name,
        login=user_data.login,
        email=user_data.email,
        password=user_data.password,
        phone=user_data.phone,
        image=user_data.image,
    )

    db_session.add(new_user)
    await db_session.commit()

    return new_user
