# region IMPORT
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, SessionLocal, Base, get_db
from app.utils import hash_password

# endregion IMPORT

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# region USER
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
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


@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} was not found ",
        )

    return db_user


# endregion USER
