from fastapi import HTTPException,Request
from fastapi.responses import RedirectResponse
from Database.db import db
from app.auth.oauth import oauth
from app.auth.jwt_handler import create_access_token
from app.models.user import UserCreate,TokenResponse,UserResponse
from app.config.settings import settings
import httpx
import logging

logger=logging.getLogger("uvicorn.error")

class AuthController:

    @staticmethod
    async def initiate_login(request:Request):

        try:
            redirect_uri=request.url_for('auth_callback')
            logger.info(f"Initiating OAuth login with redirect_uri: {redirect_uri}")
            return await oauth.google.authorize_redirect(request,redirect_uri)
        except Exception as e:
            logger.error(f"Error initiating Oauth login: {e}")
            raise HTTPException(status_code=500,detail="Failed to initiate Login")
        
    @staticmethod
    async def handle_callback(request:Request):
        try:
            token=await oauth.google.authorize_access_token(request)
            logger.info("Succesfully recieved Oauth token from google")

            user_info=token.get('userinfo')

            if not user_info:
                async with httpx.AsyncClient() as client:
                    response=await client.get(
                        'https://www.googleapis.com/oauth2/v2/userinfo',
                        headers={'Authorization':f'Bearer{token['acess_token']}'}
                    )

                    user_info=response.json()
            logger.info(f"Retrieved user info for: {user_info.get('email', 'unknown')}")

            existing_user=await db.user.find_unique(where={'googleId':user_info['id']})

            if existing_user:
                logger.info(f"Existing user found:{existing_user.email}")
                user = await db.user.update(
                    where={"id": existing_user.id},
                    data={
                        "name": user_info.get("name", ""),
                        "email": user_info.get("email", ""),
                        "picture": user_info.get("picture")
                    }
                )
            else:
                 logger.info(f"Creating new user: {user_info.get('email', 'unknown')}")

                 user_data = UserCreate(
                    email=user_info.get("email", ""),
                    name=user_info.get("name", ""),
                    picture=user_info.get("picture"),
                    google_id=user_info["id"]
                )
                 user = await db.user.create(
                    data={
                        "email": user_data.email,
                        "name": user_data.name,
                        "picture": user_data.picture,
                        "googleId": user_data.google_id
                    }
                )
                 access_token = create_access_token(data={"sub": str(user.id)})
                 logger.info(f"Created JWT token for user ID: {user.id}")

                 frontend_url = f"{settings.FRONTEND_URL}/auth/success?token={access_token}"
                 return RedirectResponse(url=frontend_url)
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            error_url = f"{settings.FRONTEND_URL}/auth/error?error=authentication_failed"
            return RedirectResponse(url=error_url)
    
    @staticmethod
    async def get_token_info(token:str)-> TokenResponse:
        from app.auth.dependencies import get_current_user

        class MockToken:
            def __init__(self,credentials):
                self.credentials=credentials
        
        try:
            user=await get_current_user(MockToken(token))
            logger.info(f'Token validated for user :{user.email}')
            return TokenResponse(acces_token=token,user=user)
        except HTTPException as e:
            logger.error(f"Invalid token provided")
            raise HTTPException(status_code=401,detail='Invalid token')
    @staticmethod
    async def get_current_user_info(current_user:UserResponse)->UserResponse:
        logger.info(f"User info requested for: {current_user.email}")
        try:
            fresh_user=await db.user.find_unique(where={'id':current_user.id})

            if not fresh_user:
                logger.error(f"User {current_user.id} not found in db")
                raise HTTPException(status_code=404,detail='User not found')
            logger.info("User details fetched succesfully")
            return UserResponse.model_validate(fresh_user)
        except Exception as e:
            logger.error(f'error fetching user info :{e}')
            raise HTTPException(status_code=500,detail="Failed to fetch user information")
    #logout controller not written yet


            