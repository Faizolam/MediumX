from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    

class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    # updated_at: datetime
    class Config:
        from_attributes =True


class UserRead(UserInDBBase):
    pass

class UserOut(BaseModel):
    id: int
    username: str
    # created_at: datetime
    
    class Config:
        from_attributes = True

# class UserInDB(UserInDBBase):
#     password_hash: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | Optional[str]=None