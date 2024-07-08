from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False
    rating: Optional[int] = None


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
