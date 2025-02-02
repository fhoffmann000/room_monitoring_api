from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from . import models
from .database import engine

from .routers import data, user, auth


# models.Base.metadata.create_all(bind=engine)

app = FastAPI(redoc_url=None) #docs_url=None,

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hi, I'm your air quality, humidity and temperature logger."}



