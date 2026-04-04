from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# ✅ token extractor
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ✅ verify token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")


# ✅ get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ✅ role check
def role_required(role: str):
    def checker(user = Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user
    return checker