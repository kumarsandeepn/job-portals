rom fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# 🔐 Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 JWT Config
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ✅ Router
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# 🔐 Hash Password
def hash_password(password: str):
    return pwd_context.hash(password)

# 🔐 Verify Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 🔐 Create Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ============================
# ✅ SIGNUP
# ============================
@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # check user exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # create new user
    new_user = models.User(
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}


# ============================
# ✅ LOGIN
# ============================
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token(
        data={"user_id": db_user.id, "role": db_user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ============================
# ✅ TEST ROUTE
# ============================
@router.get("/test")
def test_auth():
    return {"message": "Auth working 🚀"}