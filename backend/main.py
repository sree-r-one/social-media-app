# region IMPORT
from fastapi import FastAPI

# endregion IMPORT

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world again"}
