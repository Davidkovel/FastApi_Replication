# app/schemas/post.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    likes_count: int
    dislikes_count: int

    class Config:
        from_attributes = True