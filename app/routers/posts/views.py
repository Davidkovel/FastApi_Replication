from typing import Iterable, List

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.routers.posts.schemas import Post
from app.data.queries.functions import get_posts_operation

posts_router = APIRouter(prefix="/api/posts")


@posts_router.get("/get_posts", response_model=List[Post])
async def get_posts(request: Request):
    db_session = request.state.db_session

    posts = await get_posts_operation(db_session)

    return JSONResponse(status_code=200, content=posts)


@posts_router.post("/create_post")
async def create_post():
    return {"message": "Post created successfully"}


@posts_router.put("/update_post")
async def update_post():
    return {"message": "Post updated successfully"}


@posts_router.delete("/delete_post")
async def delete_post():
    return {"message": "Post deleted successfully"}
