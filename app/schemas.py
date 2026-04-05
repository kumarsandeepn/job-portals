from pydantic import BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str
    


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str
    company: str

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    company: str

    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    role: str

    class Config:
        orm_mode = True

from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6, max_length=72)] = None
    phone: Optional[str] = None

class ApplyJob(BaseModel): job_id:int