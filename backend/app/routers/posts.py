# region IMPORT
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, SessionLocal, Base, get_db

# endregion IMPORT

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


# region GET


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse]
)
async def get_posts(db: Session = Depends(get_db)):
    """
    Get all the posts from the Posts table
    """
    posts = db.query(models.Post).all()
    return posts


@router.get("/latest", status_code=status.HTTP_200_OK)
async def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return latest_post


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse
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
@router.post(
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.put(
    "/{id}",
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
