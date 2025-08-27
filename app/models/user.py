from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr
    name:str
    picture:Optional[str]=None
class UserCreate:
    google_id:str

class UserResponse(UserBase):
    id:int
    google_id:str
    created_at:datetime
    updated_at:datetime

    class config:
        from_attributes=True

class TokenResponse(BaseModel):
    acces_token:str
    token_type:str="bearer"
    user:UserResponse