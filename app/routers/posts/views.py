from fastapi import APIRouter

posts_router = APIRouter(prefix="/api/posts")


@posts_router.get("/get_posts")
async def get_posts():
    return [{"title": "Post 1"}, {"title": "Post 2"}]


@posts_router.post("/create_post")
async def create_post():
    return {"message": "Post created successfully"}


@posts_router.put("/update_post")
async def update_post():
    return {"message": "Post updated successfully"}


@posts_router.delete("/delete_post")
async def delete_post():
    return {"message": "Post deleted successfully"}
