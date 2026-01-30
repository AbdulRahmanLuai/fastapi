from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, status
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/vote",
    tags=['vote']
                   )


@router.post('', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    
    vote_row = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id).first()
    
    if vote_row and vote.dir == 0:
        
        db.delete(vote_row)
        db.commit()
        return {"message": "vote removed successfuly"}
    
    elif not vote_row and vote.dir == 1:
        
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added successfuly"}
        
    else:
        if vote_row:
            detail = "vote already exists"
        else:
            detail = "vote cannot be found"
            
        raise  HTTPException(status.HTTP_409_CONFLICT, detail=detail)
        
    