# Entry point for FastAPI app
from typing import Union

from fastapi import FastAPI

from app.routes import router

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


app.include_router(router)
