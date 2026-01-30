from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/user",
    tags=['user']
                   )



@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    retrieved = db.query(models.User).filter(models.User.id == id).first()
    print(retrieved)  
    if not retrieved:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no user with id: {id} exists")

    return retrieved
    
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    if db.query(models.User).filter(models.User.email == user.email).all():
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user already exists")
    
    
    hashed_password = utils.hash(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user



    