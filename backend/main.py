# region IMPORT
from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import posts, users, auth

# endregion IMPORT

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
