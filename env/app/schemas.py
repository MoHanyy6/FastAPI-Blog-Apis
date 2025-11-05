from pydantic  import BaseModel,EmailStr
from pydantic.types import conint
from datetime import datetime, timezone
from typing import Optional

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):
    pass
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode=True

class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    owner_id:int
    owner:UserOut
    
    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str




class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_Token : str
    token_type : str

class TokenData(BaseModel):
    id:Optional[str]=None

class Vote(BaseModel):
    post_id:int
    dir: int

class PostOut(BaseModel):
    Post:Post
    vote: int
    class Config:
        orm_mode = True
