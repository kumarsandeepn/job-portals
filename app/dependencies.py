from fastapi import Depends, HTTPException
from app.auth import oauth2_scheme, verify_access_token



# 👤 Current User
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


# 🔐 Role Based Access

# 👇 पहले ये define करो
def get_current_user():
    return {"role": "admin"}   # temporary test (later JWT लगाएँगे)


# 👇 फिर role_required
def role_required(role: str):
    def role_checker(user = Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user
    return role_checker