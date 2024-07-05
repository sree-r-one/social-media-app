# region IMPORT
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

# endregion IMPORT

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "hello world again"}


@app.get("/posts")
async def get_posts():
    return {"data": "This is your posts"}


@app.post("/create")
async def create_post(post: Post):
    print(post)
    return {"message": post}
