from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from Database.db import db
from app.auth.oauth import oauth
from app.auth.jwt_handler import create_access_token
from app.models.user import UserCreate, TokenResponse, UserResponse
from app.config.settings import settings
import httpx
import logging
from typing import Tuple
import re
import pyotp
from datetime import datetime, timedelta, timezone
from app.utils.utils import utils

logger = logging.getLogger("uvicorn.error")


class AuthController:
    @staticmethod
    async def initiate_login(request: Request):
        try:
            redirect_uri = request.url_for("auth_callback")
            logger.info(f"Initiating OAuth login with redirect_uri: {redirect_uri}")
            return await oauth.google.authorize_redirect(request, redirect_uri)
        except Exception as e:
            logger.error(f"Error initiating Oauth login: {e}")
            raise HTTPException(status_code=500, detail="Failed to initiate Login")

    @staticmethod
    async def handle_callback(request: Request):
        try:
            token = await oauth.google.authorize_access_token(request)
            if token:
                logger.info("Succesfully recieved Oauth token from google")

            user_info = token.get("userinfo")

            if not user_info:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        "https://www.googleapis.com/oauth2/v2/userinfo",
                        headers={"Authorization": f"Bearer {token['access_token']}"},
                    )

                    user_info = response.json()
            logger.info(f"Full user info from google: {user_info}")
            logger.info(f"Retrieved user info for: {user_info.get('email', 'unknown')}")

            google_user_id = user_info.get("sub") or user_info.get("id")

            if not google_user_id:
                logger.error(f"No user Id found in user_info : {user_info}")
                raise HTTPException(400, "Unable to get user ID from Google")

            existing_user = await db.user.find_unique(
                where={"googleId": google_user_id}
            )

            if existing_user:
                logger.info(f"Existing user found:{existing_user.email}")
                user = await db.user.update(
                    where={"id": existing_user.id},
                    data={
                        "name": user_info.get("name", ""),
                        "email": user_info.get("email", ""),
                        "picture": user_info.get("picture"),
                    },
                )
            else:
                logger.info(f"Creating new user: {user_info.get('email', 'unknown')}")

                user_data = UserCreate(
                    email=user_info.get("email", ""),
                    name=user_info.get("name", ""),
                    picture=user_info.get("picture") if user_info.picture else None,
                    google_id=google_user_id,
                )
                user = await db.user.create(
                    data={
                        "email": user_data.email,
                        "name": user_data.name,
                        "picture": user_data.picture,
                        "googleId": user_data.google_id,
                    }
                )
            logger.info(user.id)
            access_token = create_access_token(data={"sub": str(user.id)})
            logger.info(f"Created JWT token for user ID: {user.id}")

            frontend_url = f"{settings.FRONTEND_URL}/auth/success?token={access_token}"
            logger.info("Success Redirecting to Frontend")
            return RedirectResponse(url=frontend_url)
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            error_url = (
                f"{settings.FRONTEND_URL}/auth/error?error=authentication_failed"
            )
            return RedirectResponse(url=error_url)

    @staticmethod
    async def get_token_info(token: str) -> TokenResponse:
        from app.auth.dependencies import get_current_user

        class MockToken:
            def __init__(self, credentials):
                self.credentials = credentials

        try:
            user = await get_current_user(MockToken(token))
            logger.info(f"Token validated for user :{user.email}")
            return TokenResponse(access_token=token, user=user)
        except HTTPException:
            logger.error("Invalid token provided")
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    async def get_current_user_info(current_user: UserResponse) -> UserResponse:
        logger.info(f"User info requested for: {current_user.email}")
        try:
            fresh_user = await db.user.find_unique(where={"id": current_user.id})

            if not fresh_user:
                logger.error(f"User {current_user.id} not found in db")
                raise HTTPException(status_code=404, detail="User not found")
            logger.info("User details fetched succesfully")
            return UserResponse.model_validate(fresh_user)
        except Exception as e:
            logger.error(f"error fetching user info :{e}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch user information"
            )

    @staticmethod
    def _validate_identifier(identifier: str) -> Tuple[str, bool]:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        phone_pattern = r"^\+?1?\d{9,15}$"

        if re.match(email_pattern, identifier):
            return ("email", True)
        if re.match(phone_pattern, identifier):
            return ("phone", True)
        return (None, False)

    @staticmethod
    async def generate_and_send_otp(identifier: str):
        """Generate and send OTP based on identifier type"""
        try:
            identifierType, is_valid = AuthController._validate_identifier(identifier)

            if not is_valid:
                raise HTTPException(
                    status_code=400, detail="Invalid email or phone number Format"
                )

            # Generate OTP

            otp = pyotp.random_base32()[:6]
            otp_hash = utils.hash_otp_hmac(otp)
            current_time = datetime.now()
            expiry_time = current_time + timedelta(minutes=2)

            """Try to find user first"""

            user = await db.user.find_unique(
                where={"email" if identifierType == "email" else "phone": identifier}
            )

            if user:
                await db.user.update(
                    where={"id": user.id},
                    data={
                        "otp_hash": otp_hash,
                        "otp_identifier": identifier,
                        "otp_type": identifierType,
                        "otp_attempts": 0,
                        "otp_expires_at": expiry_time,
                        "otp_created_at": current_time,
                        "is_otp_used": False,
                    },
                )
            else:
                user = await db.user.create(
                    data={
                        "email" if identifierType == "email" else "phone": identifier,
                        "otp_hash": otp_hash,
                        "otp_identifier": identifier,
                        "otp_type": identifierType,
                        "otp_attempts": 0,
                        "otp_expires_at": expiry_time,
                        "otp_created_at": current_time,
                        "is_otp_used": False,
                        "name": "",
                    }
                )
                sent = True
            if identifierType == "email":
                sent = await utils._send_email_otp(identifier, otp)

            else:
                sent = await utils._send_sms_otp(identifier, otp)
            if not sent:
                raise Exception(f"OTP Not sent for {identifier}")
        except Exception as e:
            logger.error(f"Failed to send OTP email: {e}")
            raise HTTPException(status_code=500, detail="Failed to send OTP")

    @staticmethod
    async def _clear_otp_fields(user_id: int):
        """Clear All otp related fields in userid"""

        try:
            await db.user.update(
                where={"id": user_id},
                data={
                    "otp_hash": None,
                    "otp_identifier": None,
                    "otp_type": None,
                    "otp_attempts": 0,
                    "otp_expires_at": None,
                    "otp_created_at": None,
                    "is_otp_used": False,
                },
            )
            logger.info(f"Cleared OTP fields for user {user_id}")
        except Exception as e:
            logger.error(f"Error clearing OTP fields for user {user_id}:{e}")

    @staticmethod
    async def verify_login_otp(identifier: str, otp: str):
        try:
            user = await db.user.find_unique(where={"otp_identifier": identifier})

            if not user or not user.otp_hash:
                raise HTTPException(status_code=400, detail="Invalid OTP")

            if datetime.now(timezone.utc) > user.otp_expires_at:
                await AuthController._clear_otp_fields(user.id)
                raise HTTPException(status_code=400, detail="otp expired")

            if user.otp_attempts >= user.otp_max_retries:
                await AuthController._clear_otp_fields(user.id)
                raise HTTPException(status_code=401, detail="Maximum attempts reached")

            if not utils.verify_otp_hmac(otp, user.otp_hash):
                await db.user.update(
                    where={"id": user.id}, data={"otp_attempts": user.otp_attempts + 1}
                )
                raise HTTPException(status_code=400, detail="Invalid OTP")

            access_token = create_access_token(data={"sub": str(user.id)})
            await AuthController._clear_otp_fields(user.id)
            return TokenResponse(
                access_token=access_token, user=UserResponse.model_validate(user)
            )
        except Exception as e:
            logger.error(f"Error verifying OTP :{e}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, details="Failed to verify OTP")

    # logout controller not written yet
