from fastapi import FastAPI , Query, Path,Body,status,HTTPException,Depends,APIRouter
from typing import List
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from ..database import engine,get_db

router=APIRouter(
    prefix="/vote"
    ,
    tags=['Votes']
)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    vote_query=db.query(models.Votes).filter(models.Votes.post_id==vote.post_id,models.Votes.user_id==current_user.id)
    found_vote=vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"The post has been voted")
        new_vote=models.Votes(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Sucessfully added post"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found vote")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"sucess deleted vote"}


    