
from fastapi import FastAPI , Query, Path,Body,status,HTTPException,Depends,APIRouter
from typing import List,Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from ..database import engine,get_db
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# ,response_model=List[schemas.Post]
@router.get("/")
async def get_posts(db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user),
                    limit:int=2,skip:int =0,search:Optional[str]=""):
    posts=db.query(models.Post).filter(models.Post.owner_id==get_current_user.id).all()
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # result=db.query(models.Post,func.count(models.Votes.post_id.label("Votes"))).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    # result=db.query(models.Post).join(
    #      models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    # cursor.execute("SELECT * FROM posts")
    # posts=cursor.fetchall()
    # return posts
    result = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")) \
    .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True) \
    .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # ===Note make return like this because db.query() contain more than 1
    return [{"Post": post, "Votes": votes} for post, votes in result]


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    print(get_current_user.email)
    post = models.Post(owner_id=get_current_user.id,**new_post.dict())  # Convert from Pydantic to ORM model
    db.add(post)                           # ✅ Add to session
    db.commit()                            # ✅ Save changes
    db.refresh(post)                       # ✅ Load new data (id, defaults)
    return post             # ✅ Return ORM instance

# @router.get("/posts/latest",response_model=schemas.Post)
# async def get_latest_post():
#     cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
#     latest_post = cursor.fetchone()
#     if not latest_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
#     return latest_post
#     #post=my_posts[-1]
#     # post=my_posts[len(my_posts)-1]
#     #return {"Latest post":post}


@router.get("/{id}",response_model=schemas.PostOut)
async def get_post(id:int,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # post=db.query(models.Post).filter(models.Post.id==id).first()

    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
    # post=cursor.fetchone()

    result= db.query(models.Post, func.count(models.Votes.post_id).label("Votes")) \
    .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True) \
    .group_by(models.Post.id).filter(models.Post.id==id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # if post.owner_id != get_current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform action")
    # return post

    #  i dont make for loop in it because .all ()  and .first() . all retutn list of tuples: while .first return one 
    post, vote = result
    return {"Post": post, "vote": vote}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int,db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted=cursor.fetchone()
    # conn.commit()
    # if deleted is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id {id} not found"
    #     )
    # return {"deleted_post":deleted}
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message":"Post deleted successfully"}

@router.put("/{id}",response_model=schemas.Post)
async def updated_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post ==None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"postwith {id} not found")
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post
