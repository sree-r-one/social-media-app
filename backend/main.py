# region IMPORT
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base, get_db
from app import models, schemas
from app.utils import hash_password

# endregion IMPORT


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# region GET
@app.get("/")
async def root():
    return {"message": "hello world again"}


@app.get(
    "/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse]
)
async def get_posts(db: Session = Depends(get_db)):
    """
    Get all the posts from the Posts table
    """
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/latest", status_code=status.HTTP_200_OK)
async def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return latest_post


@app.get(
    "/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse
)
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
    return post


# endregion GET


# region POST
@app.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    Create a post
    """

    db_post = models.Post(**post.model_dump())  # Unpack the model
    db.add(db_post)  # Add the post to the database
    db.commit()  # Commit to the database
    db.refresh(db_post)
    return db_post


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
@app.put(
    "/posts/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostResponse,
)
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

    return post_to_update


# endregion UPDATE


# region USER
@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a User
    """
    user_check = db.query(models.User).filter(models.User.email == user.email).first()

    if user_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Exists!")

    # Hash the password
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    db_user = models.User(**user.model_dump())  # Unpack the model
    db.add(db_user)  # Add the post to the database
    db.commit()  # Commit to the database
    db.refresh(db_user)
    return db_user


# endregion USER
