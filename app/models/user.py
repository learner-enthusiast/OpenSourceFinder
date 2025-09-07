from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None


class UserCreate(UserBase):
    google_id: str


class UserResponse(UserBase):
    id: int
    googleId: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

    class Config:
        from_atrributes = True


class OTPRequest(BaseModel):
    identifier: str


class OTPValidates(BaseModel):
    identifier: str
    otp: str
