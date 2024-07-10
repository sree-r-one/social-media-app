from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False
    rating: Optional[int] = None

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
