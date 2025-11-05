from fastapi import FastAPI , Query, Path,Body,status,HTTPException,Depends
from typing import List
from random import randrange

from . import models,schemas,utils
from sqlalchemy.orm import Session
from .database import engine,get_db
from .routers import posts , users,auth,vote



models.Base.metadata.create_all(bind=engine)
print("✅ Tables should now be created if they don’t exist.")

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)
    






