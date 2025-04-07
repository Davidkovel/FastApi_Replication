from typing import Iterable, List

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.routers.posts.schemas import Post, PostCreate, PostUpdate, PostDelete
from app.data.queries.functions import get_posts_operation, create_post_operation, update_post_operation, \
    delete_post_operation, get_post_by_id

posts_router = APIRouter(prefix="/api/posts")


@posts_router.get("/get_posts", response_model=List[Post])
async def get_posts(request: Request):
    db_session = request.state.db_session
    posts = await get_posts_operation(db_session)
    return posts


@posts_router.post("/create_post", response_model=Post)
async def create_post(request: Request, post_data: PostCreate):
    db_session = request.state.db_session
    new_post = await create_post_operation(db_session, post_data.model_dump())
    return new_post


@posts_router.put("/update_post")
async def update_post(request: Request, post_data: PostUpdate):
    db_session = request.state.db_session

    post = await get_post_by_id(db_session, post_data.id)
    if not post:
        raise JSONResponse(status_code=404, content={"message": "Post not found"})

    updated_post = await update_post_operation(db_session, post_data.id, post_data.model_dump())
    return updated_post


@posts_router.delete("/delete_post")
async def delete_post(request: Request, post_data: PostDelete):
    db_session = request.state.db_session

    post = await get_post_by_id(db_session, post_data.id)
    if not post:
        raise JSONResponse(status_code=404, content={"message": "Post not found"})

    return await delete_post_operation(db_session, post_data.id)
