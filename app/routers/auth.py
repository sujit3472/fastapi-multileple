from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserRegister, UserLogin
from ..utils.auth import hash_password, verify_password, create_token
from ..utils.response import api_response

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