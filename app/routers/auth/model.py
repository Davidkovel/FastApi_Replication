from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)

    name = Column(String(50), nullable=False)
    login = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)

    phone = Column(String(20), nullable=True)
    image = Column(String(200), nullable=True)
