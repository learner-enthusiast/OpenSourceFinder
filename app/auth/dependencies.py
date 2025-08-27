from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer
from app.auth.jwt_handler import verify_token
from Database.db import db
from app.models.user import UserResponse

security=HTTPBearer()

async def get_current_user(token:str=Depends(security))->UserResponse:
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate credentials',headers={"WWW-Authenticate":"Bearer"}
    )

    user_id=verify_token(token.credentials)
    if user_id is None:
        raise credentials_exception
    user= await db.user.find_unique(where={"id":user_id})
    if user is None:
        raise credentials_exception
    return UserResponse.model_validate(user)
