from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=False)
    username = Column(String, unique=True, nullable=False, index=False)
    password_hash = Column(String, nullable=False, index=False)
