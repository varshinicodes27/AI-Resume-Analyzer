from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserRegister


# ======================================================
# PASSWORD CONFIGURATION
# ======================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ======================================================
# JWT CONFIGURATION
# ======================================================

SECRET_KEY = "resumeiq-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ======================================================
# PASSWORD FUNCTIONS
# ======================================================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ======================================================
# REGISTER USER
# ======================================================

def register_user(
    user: UserRegister,
    db: Session
):

    print("========== REGISTER START ==========")

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    print("Existing user:", existing_user)

    if existing_user:
        print("Email already exists")

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password)
    )

    print("Before add")

    db.add(new_user)

    print("Before commit")

    db.commit()

    print("After commit")

    db.refresh(new_user)

    print("New User ID:", new_user.id)

    return {
        "message": "User registered successfully"
    }


# ======================================================
# CREATE JWT TOKEN
# ======================================================

def create_access_token(user_id: int):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ======================================================
# LOGIN USER
# ======================================================

def login_user(
    email: str,
    password: str,
    db: Session
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    # User not found
    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Password verification
    if not verify_password(
        password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Generate JWT
    token = create_access_token(
        user.id
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "full_name": user.full_name
    }