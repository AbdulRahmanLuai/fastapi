from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    password: str
    
class UserResponse(UserBase):
    
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
    

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    title: str
    content: str
    published: bool = True
    
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse
    
    class Config:
        from_attributes = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        from_attributes = True
    
class Token(BaseModel):
    
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    
    id: Optional[int] = None
    
    
    

class Vote(BaseModel):
    
    post_id: int
    dir: Literal[0, 1]