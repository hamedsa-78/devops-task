import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Base, User
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash


# DataBase Creation
sqlite3.connect("database.db")
engin = create_engine(
    "sqlite:///database.db", connect_args={"check_same_thread": False}
)
Base.metadata.create_all(bind=engin)

# FastApi app definition
app = FastAPI()

# SQLite database connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engin)


# Defining get_db for correct testing without changing main database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "green"


@app.get("/health/")
async def check_health():
    return HealthCheck(status="green")


# type of data from request.post coming
class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # db = SessionLocal()
    user = User(
        username=user.username, password_hash=generate_password_hash(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
    )


# Get User endpoint
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(username=user.username, id=user.id)
