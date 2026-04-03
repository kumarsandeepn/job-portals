from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ IMPORTANT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth_utils import create_access_token
from app.auth import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)

    new_user = models.User(
        email=user.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_access_token({"user_id": db_user.id})

    return {"access_token": token}