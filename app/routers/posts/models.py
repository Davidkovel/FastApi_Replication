from datetime import datetime

from sqlalchemy import Column, Integer, String, ARRAY, DATETIME, DateTime

from app.db.base_class import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    tags = Column(ARRAY(String(20)), nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    likes_count = Column(Integer, nullable=True, default=0)
    dislikes_count = Column(Integer, nullable=True, default=0)