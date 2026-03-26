from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models.user import User
from ..schemas.user import UserRegister, UserLogin, ForgotPasswordRequest, ResetPasswordRequest
from ..utils.auth import hash_password, verify_password, create_token
from ..utils.response import api_response
from ..utils.email import send_email
from ..utils.token import create_reset_token
from datetime import datetime, timedelta


router = APIRouter(
    prefix="/auth", 
    tags=["Auth"]
)


@router.post("/register")
def register(
    data: UserRegister,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if user:
        return api_response(400, "Email exists", None, False)
        
    hashed = hash_password(data.password)

    new_user = User(
        name=data.name,
        email=data.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return api_response(200, "User Registered successfully", None, True)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        return api_response(400, "Invalid email", None, False)

    if not verify_password(
        form_data.password,
        user.password
    ):
        return api_response(400, "Invalid password", None, False)

    token = create_token({
        "id": user.id,
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #  Generate token
    token = create_reset_token(user.email)

    # Reset link (frontend URL)
    reset_link = f"http://localhost:3000/reset-password?token={token}"

    # Email content
    subject = "Reset Your Password"
    body = f"""
    <p>Hello,</p>
    <p>Click below link to reset your password:</p>
    <a href="{reset_link}">Reset Password</a>
    <p>This link will expire in 30 minutes.</p>
    """

    send_email(user.email, subject, body)

    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        return api_response(400, "Database error",None,False)

    return {
        "status": True,
        "message": "Password reset email sent successfully"
    }



@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):

    # 🔍 Find user by token
    user = db.query(User).filter(User.reset_token == request.token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    # ⏰ Check token expiry
    if not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    # 🔐 Update password
    user.password = hash_password(request.new_password)

    # ❌ Clear token after use
    user.reset_token = None
    user.reset_token_expiry = None

    db.commit()

    return {
        "status": True,
        "message": "Password reset successfully"
    }