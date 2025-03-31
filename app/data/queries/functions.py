from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.posts.models import Post


async def get_posts_operation(db_session: AsyncSession) -> Post:
    query = select(Post)
    result = await db_session.execute(query)
    posts = result.scalars().all()

    return posts
