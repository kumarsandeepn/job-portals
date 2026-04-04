from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError

# 🔐 Config
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


# ============================
# ✅ Get Token from Header
# ============================
def get_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    # Bearer TOKEN → TOKEN
    return authorization.split(" ")[1]


# ============================
# ✅ Verify Token
# ============================
def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ============================
# ✅ Role Based Access
# ============================
def role_required(role: str):
    def checker(user = Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user
    return checker