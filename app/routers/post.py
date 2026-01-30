from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List




router = APIRouter(
    prefix="/posts",
    tags=['posts']
)



# @routeel=List[schemas.PostResponse])r.get('', response_mod
@router.get('', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post, func.count(models.Vote.user_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    print(posts)
    return posts.all()


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post, func.count(models.Vote.user_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
           
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
                
    return post
    
        


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):

    post_data = post.model_dump()
    post_data["user_id"] = user.id
    new_post = models.Post(**post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    
    
    
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"no post with id: {id} was found") 

    
    owner_id = post.user_id
    
    if owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete others' posts")
    
    db.delete(post)   
    db.commit()    
    return Response(status_code = status.HTTP_204_NO_CONTENT) 
        
        
    


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    
    owner_id = db.query(models.Post).filter(models.Post.id == id).first().user_id

    if owner_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Cannot update others' posts")
        
    
    rows_updated = db.query(models.Post).filter(models.Post.id == id).update(post.model_dump())
       
    if not rows_updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"no post with id: {id} was found") 
        
    db.commit()
    updated_post = db.query(models.Post).filter(models.Post.id==id).first()
    return updated_post
    
            
             