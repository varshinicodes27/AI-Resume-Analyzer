from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user_schema import (
    UserRegister,
    UserLogin
)
from app.services.auth_service import (
    register_user,
    login_user
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# ======================================================
# REGISTER
# ======================================================

@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    return register_user(
        user,
        db
    )


# ======================================================
# LOGIN
# ======================================================

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    return login_user(
        user.email,
        user.password,
        db
    )