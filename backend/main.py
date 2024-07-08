# region IMPORT
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base, get_db
from app import models, schemas

# endregion IMPORT

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# region GET
@app.get("/")
async def root():
    return {"message": "hello world again"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    """
    Get all the posts from the Posts table
    """
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/latest", status_code=status.HTTP_200_OK)
async def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return {"post_detail": latest_post}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):
    """
    Get a post using ID
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with the id {id} was not found ",
        )
    return {"post_detail": post}


# endregion GET


# region POST
@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    Create a post
    """

    db_post = models.Post(**post.model_dump())  # Unpack the model
    db.add(db_post)  # Add the post to the database
    db.commit()  # Commit to the database
    return {"message": post}


# endregion POST


# region DELETE
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    """
    Delete a post
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    db.delete(post)
    db.commit()
    return


# endregion DELETE


# region UPDATE
@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    """
    Update a post
    """
    post_to_update = db.query(models.Post).filter(models.Post.id == id).first()

    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    post_to_update.title = post.title
    post_to_update.content = post.content
    post_to_update.published = post.published

    db.commit()

    return {"updated_post": post_to_update}


# endregion UPDATE
