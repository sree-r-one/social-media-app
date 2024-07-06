# region IMPORT
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

# endregion IMPORT

app = FastAPI()

posts = [
    {"title": "Title of Post 1", "id": 1, "content": "Content of Post 1 "},
    {"title": "Title of Post 2", "id": 2, "content": "Content of Post 2 "},
]


def find_post(id):
    for post in posts:
        if post["id"] == id:
            return post


def find_post_index(id):
    for i, p in enumerate(posts):
        if p["id"] == id:
            return i
    return None


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# region GET
@app.get("/")
async def root():
    return {"message": "hello world again"}


@app.get("/posts")
async def get_posts():
    return {"data": posts}


@app.get("/posts/latest")
async def get_latest_post():
    post = posts[-1]
    return {"post_detail": post}


@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with the id {id} was not found ",
        )
    return {"post_detail": post}


# endregion GET


# region POST
@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, response=Response):
    """
    Create a post
    """
    print(post)
    return {"message": post}


# endregion POST


# region DELETE
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    """
    Delete a post
    """
    index = find_post_index(id)

    # If No index is found
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    posts.pop(index)
    return


# endregion DELETE


# region UPDATE
@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, post: Post):
    """
    Update a post
    """
    index = find_post_index(id)

    # If No index is found
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    updated_post = {**post.model_dump(), "id": id}

    return {"updated_post": "Updated post"}


# endregion UPDATE
