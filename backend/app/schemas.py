from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False
    rating: Optional[int] = None

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False

    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True
