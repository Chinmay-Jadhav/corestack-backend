from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime
from typing import List

from src.db import models
from src.reviews.schemas import ReviewModel

class UserCreateModel(BaseModel) :
    username : str = Field(max_length=16)
    email : EmailStr
    password : str = Field(min_length=8)
    first_name : str = Field(max_length=25)
    last_name : str = Field(max_length=25)

class UserModel(BaseModel) :
    uid : uuid.UUID 
    username : str
    # password_hash : str = Field(nullable=False, exclude=True)
    email : str
    first_name : str
    last_name : str
    is_verified : bool 
    created_at : datetime 
    updated_at : datetime

class UserBooksModel(UserModel) :
    books : List[models.Book] 
    reviews : List[ReviewModel]

class UserLoginModel(BaseModel) :
    email : EmailStr
    password : str = Field(min_length=8)