from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app import models
from app.schemas import UserCreate
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])


# ✅ REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}


# ✅ LOGIN
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_access_token({
        "user_id": user.id,
        "role": user.role   # 🔥 IMPORTANT
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }