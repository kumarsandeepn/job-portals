from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

# 🔐 CONFIG
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================
# ✅ CREATE TOKEN
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
    # 👇 username = email
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
@router.get("/test")
def test_auth(user = Depends(get_current_user)):
    return {
        "message": "Auth working",
        "user": user
    }

from app import schemas

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # check user exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}