from fastapi import APIRouter, Depends, Request
from app.controllers.auth import AuthController
from app.models.user import UserResponse, TokenResponse
from app.auth.dependencies import get_current_user
from app.models.user import OTPRequest, OTPValidates

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/login")
async def login(request: Request):
    """Initiate Google OAuth login"""
    return await AuthController.initiate_login(request)


@router.get("/callback")
async def auth_callback(request: Request):
    """Handle Google OAuth callback"""
    return await AuthController.handle_callback(request)


@router.post("/token", response_model=TokenResponse)
async def get_token_info(token: str):
    """Get user info from token (for frontend to call after redirect)"""
    return await AuthController.get_token_info(token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Get current user information"""
    return await AuthController.get_current_user_info(current_user)


@router.post("/identifier-login")
async def identifierLogin(payload: OTPRequest):
    # OTP login

    return await AuthController.generate_and_send_otp(payload.identifier)


@router.post("/verify-otp")
async def verify_otp(request: OTPValidates):
    return await AuthController.verify_login_otp(request.identifier, request.otp)
