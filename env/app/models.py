from .database import Base
from sqlalchemy import Column, Integer, String, Boolean,TIMESTAMP, text,ForeignKey
from sqlalchemy.orm import Relationship



class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, nullable=False)
    owner_id= Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,)
    owner=Relationship("User")
    

class User(Base):
    __tablename__="users"
    id=Column(Integer,nullable=False,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Votes(Base):
    __tablename__="votes"

    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)