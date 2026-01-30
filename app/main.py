from fastapi import FastAPI
from . import models, config
from .database import engine
from sqlalchemy.orm import Session
from .routers import auth, post, user, vote



with engine.begin() as conn:
    models.Base.metadata.create_all(bind=conn)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
async def root():
    return {"message": "hello worrrld"}


    