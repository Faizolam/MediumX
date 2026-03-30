from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# UserBase: The foundation containing fields shared by almost all other user schemas (username and email).
# EmailStr: A special Pydantic type that ensures the string is a valid email format.
class UserBase(BaseModel):
    username: str
    email: EmailStr
    
# UserCreate: Inherits from UserBase and adds a password field, which is required when creating a new user.
class UserCreate(UserBase):
    password: str

#
class UserUpdate(UserBase):
    password: Optional[str] = None

# UserInDBBase: Extends UserBase by adding fields that are stored in the database (id and created_at). The Config class with from_attributes=True allows Pydantic to create instances of this model from ORM objects, which is useful when retrieving data from the database.
class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    # updated_at: datetime
    class Config:
        from_attributes =True

# The Filter: Since UserRead does not have a password field, Pydantic simply ignores the password hash from the database object.
class UserRead(UserInDBBase):
    pass

# UserInDB: Inherits from UserInDBBase and adds the password_hash field, which is used internally to store the hashed password in the database but is not exposed in API responses.
class UserOut(BaseModel):
    id: int
    username: str
    # created_at: datetime
    
    class Config:
        from_attributes = True

# class UserInDB(UserInDBBase):
#     password_hash: str

# Token schemas for authentication
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token: Represents the structure of the JWT token that will be returned to the client upon successful authentication, containing the access token and its type.
class Token(BaseModel):
    access_token: str
    token_type: str

# TokenData: Represents the data contained within the JWT token, specifically the user ID. This is used when decoding the token to identify the user making a request.
class TokenData(BaseModel):
    id: int | Optional[str]=None