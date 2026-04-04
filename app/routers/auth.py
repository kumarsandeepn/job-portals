from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta

from app.database import get_db
from app import models
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Auth"])

# 🔐 Config
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================
# ✅ Create Token
# ============================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ============================
# ✅ LOGIN (Swagger compatible)
# ============================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================
# ✅ TEST AUTH
# ============================
from app.dependencies import get_current_user

@router.get("/test")
def test_auth(user = Depends(get_current_user)):
    return {
        "message": "Auth working",
        "user": user
    }